import json
import os
import re
import unicodedata

import pandas as pd


def load_data_as_dataframe(file_name):
    data = []

    # Open the file and read each line
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            # Parse each line as JSON and append it to the data list
            data.append(json.loads(line))

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    return df


# List of French stopwords from NLTK
french_stopwords = {
    "ai",
    "aie",
    "aient",
    "aies",
    "ait",
    "as",
    "au",
    "aura",
    "aurai",
    "auraient",
    "aurais",
    "aurait",
    "auras",
    "aurez",
    "auriez",
    "aurions",
    "aurons",
    "auront",
    "aux",
    "avaient",
    "avais",
    "avait",
    "avec",
    "avez",
    "aviez",
    "avions",
    "avons",
    "ayant",
    "ayante",
    "ayantes",
    "ayants",
    "ayez",
    "ayons",
    "c",
    "ce",
    "ces",
    "d",
    "dans",
    "de",
    "des",
    "du",
    "elle",
    "en",
    "es",
    "est",
    "et",
    "eu",
    "eue",
    "eues",
    "eurent",
    "eus",
    "eusse",
    "eussent",
    "eusses",
    "eussiez",
    "eussions",
    "eut",
    "eux",
    "eûmes",
    "eût",
    "eûtes",
    "furent",
    "fus",
    "fusse",
    "fussent",
    "fusses",
    "fussiez",
    "fussions",
    "fut",
    "fûmes",
    "fût",
    "fûtes",
    "il",
    "ils",
    "j",
    "je",
    "l",
    "la",
    "le",
    "les",
    "leur",
    "lui",
    "m",
    "ma",
    "mais",
    "me",
    "mes",
    "moi",
    "mon",
    "même",
    "n",
    "ne",
    "nos",
    "notre",
    "nous",
    "on",
    "ont",
    "ou",
    "par",
    "pas",
    "pour",
    "qu",
    "que",
    "qui",
    "s",
    "sa",
    "se",
    "sera",
    "serai",
    "seraient",
    "serais",
    "serait",
    "seras",
    "serez",
    "seriez",
    "serions",
    "serons",
    "seront",
    "ses",
    "soient",
    "sois",
    "soit",
    "sommes",
    "son",
    "sont",
    "soyez",
    "soyons",
    "suis",
    "sur",
    "t",
    "ta",
    "te",
    "tes",
    "toi",
    "ton",
    "tu",
    "un",
    "une",
    "vos",
    "votre",
    "vous",
    "y",
    "à",
    "étaient",
    "étais",
    "était",
    "étant",
    "étante",
    "étantes",
    "étants",
    "étiez",
    "étions",
    "été",
    "étée",
    "étées",
    "étés",
    "êtes",
}


def preprocess_french_text(text):
    # lowercase the text
    text = text.lower()
    # remove punctuation and special characters (keep words and spaces)
    text = re.sub(r"[^a-zA-ZàâäéèêëîïôöùûüçœÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŒ\s]", "", text)
    # normalize Unicode (handle accents)
    text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    # remove stopwords
    tokens = [x for x in text.split() if x not in french_stopwords]
    processed_text = " ".join(tokens)
    return processed_text


if __name__ == '__main__':
    DATA_PATH = os.path.dirname(os.path.abspath(__file__))
    article_data_file_names = ["public.txt", "vsd.txt"]
    raw_data_folder = os.path.join(DATA_PATH, "raw")
    processed_data_folder = os.path.join(DATA_PATH, "processed")
    os.makedirs(processed_data_folder, exist_ok=True)
    article_data_file_paths = [os.path.join(raw_data_folder, x) for x in article_data_file_names]
    df = pd.concat([load_data_as_dataframe(x) for x in article_data_file_paths])
    df["processed_text"] = df["raw_text"].apply(preprocess_french_text)
    save_path = os.path.join(processed_data_folder, "processed.csv")
    df.to_csv(save_path, index=False)
