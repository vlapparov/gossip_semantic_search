from typing import List

import numpy as np
import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector

from utils.conf import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB_HOST,
    POSTGRES_DB_PORT,
    POSTGRES_DB,
)


class PostgresClient:
    def __init__(self):
        self.params = dict(
            host=POSTGRES_DB_HOST,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_DB_PORT,
        )
        self.enable_vector_extension()

    def enable_vector_extension(self):
        conn = psycopg2.connect(**self.params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def create_table(self):
        conn = psycopg2.connect(**self.params)
        register_vector(conn)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE documents (id bigserial PRIMARY KEY, url text, content text, embedding vector(384));")
                    print("Table 'documents' created")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def drop_table(self):
        conn = psycopg2.connect(**self.params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("DROP TABLE IF EXISTS documents;")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def ingest_embeddings(self, urls: List[str], contents: List[str], embeddings: np.ndarray):
        """
        Ingest embeddings into the database
        :param urls: list of urls
        :param contents: list of strings
        :param embeddings: list of embeddings
        """
        assert len(contents) == len(embeddings), "Content and embeddings should have the same length."
        assert len(urls) == len(contents), "Urls and content should have the same length."
        print(f"Requested to ingest {len(contents)} records into the database.")
        conn = psycopg2.connect(**self.params)
        register_vector(conn)
        try:
            with conn:
                with conn.cursor() as cursor:
                    for url, content, embedding in zip(urls, contents, embeddings):
                        cursor.execute('INSERT INTO documents (url, content, embedding) VALUES (%s, %s, %s)',
                                       (url, content, embedding))
            print(f'Ingested {len(contents)} records into the database.')
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def search_similar_by_embedding(self, embedding: np.ndarray, n_records: int = 5) -> List[List[str]]:
        """
        Search for similar records by embedding
        :param embedding: record embedding (np.ndarray of shape (384,))
        :param n_records: number of records to return
        :return: list of records of format [[url, content]]
        """
        conn = psycopg2.connect(**self.params)
        register_vector(conn)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT url, content FROM documents ORDER BY embedding <=> %s LIMIT %s',
                                   (embedding, n_records,), )
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
