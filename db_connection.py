import psycopg2
from pgvector.psycopg2 import register_vector

from models.sentence_embeddings import SentenceEmbeddings


# conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
# cur = conn.cursor()
# cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
# register_vector(conn)
#
# cur.execute('DROP TABLE IF EXISTS documents')
# cur.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))')


def create_db(params):
    conn = psycopg2.connect(**params)
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384));")
                # user = cursor.fetchone()
                # return user
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def drop_db(params):
    conn = psycopg2.connect(**params)
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS documents;")
                # user = cursor.fetchone()
                # return user
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def ingest_embeddings(params):
    input = [
        'Eating donuts is fun',
        'I love my dog',
        'I love my cat and donuts',
    ]

    model = SentenceEmbeddings()
    embeddings = model.encode(input)
    print(f"{type(embeddings) = }")
    conn = psycopg2.connect(**params)
    register_vector(conn)
    try:
        with conn:
            with conn.cursor() as cursor:
                for content, embedding in zip(input, embeddings):
                    cursor.execute('INSERT INTO documents (content, embedding) VALUES (%s, %s)', (content, embedding))
                print('Data ingested')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def search_similar(params, query):
    model = SentenceEmbeddings()
    embedding = model.encode(query)
    print(f"{type(embedding) = }")
    # print(f"{embedding = }")
    conn = psycopg2.connect(**params)
    register_vector(conn)
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id FROM documents ORDER BY embedding <=> %s LIMIT 5',
                               (embedding,),)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    parameters = {'dbname': 'postgres', 'user': 'postgres', 'password': 'postgres', 'host': 'localhost', 'port': 5432}
    ingest_embeddings(
        params=parameters
    )
    res = search_similar(params=parameters, query='I love')
    print(res)
