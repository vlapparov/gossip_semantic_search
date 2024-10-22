import os

import pandas as pd

from models.sentence_embeddings import SentenceEmbeddings
from utils.conf import DATA_DIR
from utils.postgres import PostgresClient


def preprocess_article_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna()
    data = data.drop_duplicates(subset=["url", "raw_text"])
    return data


if __name__ == '__main__':
    data_file_path = os.path.join(DATA_DIR, "processed", "processed.csv")
    df = pd.read_csv(data_file_path)
    df = preprocess_article_data(df)
    db_connector = PostgresClient()
    model = SentenceEmbeddings()

    # Drop and recreate the table to start fresh
    db_connector.drop_table()
    db_connector.create_table()

    batch_size = 1000
    for start_idx in range(0, len(df), batch_size):
        end_idx = min(start_idx + batch_size, len(df))
        print(f"Ingesting batch {start_idx + 1}-{end_idx} (total number of records: {len(df)})...")
        batch_df = df.iloc[start_idx:end_idx]
        embeddings = model.encode(batch_df["processed_text"].tolist())
        urls = batch_df["url"].tolist()
        articles = batch_df["raw_text"].tolist()
        db_connector.ingest_embeddings(urls=urls, contents=articles, embeddings=embeddings)
