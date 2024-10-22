import asyncio
import json
import os.path

import aiohttp
import requests
from bs4 import BeautifulSoup

from utils.conf import DATA_DIR


def way_back_urls(host: str, with_subs: bool = False) -> list:
    """
    Fetch URLs from the Wayback Machine
    :param host: website host address
    :param with_subs: include subdomains
    :return: list of URLs
    """
    if with_subs:
        url = 'http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey' % host
    else:
        url = 'http://web.archive.org/cdx/search/cdx?url=%s/*&output=json&fl=original&collapse=urlkey' % host
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    # check the status code
    if r.status_code != 200:
        raise Exception(f"Failed to fetch URLs from Wayback Machine: {r.status_code}")
    results = r.json()
    return results[1:]


async def fetch(session, url) -> tuple:
    """
    Fetch the URL asynchronously
    :param session: aiohttp session
    :param url: URL to fetch
    :return: tuple of URL and text
    """
    try:
        async with session.get(url) as response:
            # Return the status code and the URL
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                return url, soup.get_text(separator=" ", strip=True)
            else:
                return url, ""
    except Exception as e:
        return url, f"Error: {e}"


async def fetch_all(urls: list) -> tuple:
    """
    Fetch all URLs asynchronously
    :param urls: list of URLs
    :return: results
    """
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks to fetch all URLs
        tasks = [fetch(session, url) for url in urls]
        # Run the tasks concurrently and collect results
        results = await asyncio.gather(*tasks)
        return results


def split_into_batches(data, batch_size) -> list:
    """Splits the data list into batches of the given batch size."""
    for i in range(0, len(data), batch_size):
        yield data[i: i + batch_size]


async def process_and_save_in_batches(urls, batch_size=10, file_name="data.txt") -> None:
    """Processes URLs in batches, runs fetch_all, and appends results to a file."""
    # Split the URLs into batches
    url_batches = list(split_into_batches(urls, batch_size))

    # Process each batch
    total_batches = len(url_batches)
    for idx, batch in enumerate(url_batches):
        if idx % 10 == 0:
            print(f"Processing batch {idx + 1}/{total_batches}")

        # Fetch the data for the current batch asynchronously
        results = await fetch_all(batch)

        # Save the results to the file
        with open(file_name, "a", encoding="utf-8") as f:
            for url, data in results:
                # Choose your preferred format; here we use JSON to structure the data
                f.write(json.dumps({"url": url, "raw_text": data}) + "\n")


def post_process_urls(urls: list, host: str = "vsd") -> list:
    """
    Post-process the URLs source-wise to filter out unwanted URLs
    :param urls: list of URLs
    :param host: source host (basically a website)
    :return: list of parsed URLs
    """
    assert host in ["vsd", "public"], "Invalid host"
    if host == "vsd":
        # relevant urls extraction for vsd
        clean_urls = [x[0] for x in urls if x[0].endswith("/")]
    else:
        # relevant urls extraction for public
        domain = "http://www.public.fr/"
        public_urls = [x[0] for x in urls]
        clean_urls = []
        for x in public_urls:
            if domain not in x or x.endswith(".jpg") or x.endswith(".html"):
                continue
            _x = x.split(domain)
            clean_urls.append("".join([domain, _x[1]]))

        subdomains_to_keep = {"News", "Bios", "Look", "people"}

        clean_urls = [x for x in clean_urls if x.replace(domain, "").split("/")[0] in subdomains_to_keep]
    return clean_urls


if __name__ == '__main__':
    raw_data_folder = os.path.join(DATA_DIR, "raw")
    os.makedirs(raw_data_folder, exist_ok=True)
    hosts = ["www.vsd.fr", "www.public.fr"]
    for host in hosts:
        print(f"Fetching URLs for {host}...")
        source = host.split(".")[1]
        local_file_name = f"{source}.txt"
        extracted_urls = way_back_urls(host)
        processed_urls = post_process_urls(urls=extracted_urls, host=source)
        save_path = os.path.join(raw_data_folder, local_file_name)
        asyncio.run(process_and_save_in_batches(urls=processed_urls, batch_size=100, file_name=save_path))
