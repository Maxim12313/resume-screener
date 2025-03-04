import pandas as pd
from typing import List
from datasets import Dataset
from parser import clean

import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from config import RESUME_DOC_TABLE, EMBEDDING_TABLE, EMBEDDING_LENGTH, Shared

shared = Shared()

def embed_chunks_map(sample):
    return {
        "Embeddings" : shared.embed_documents(sample["Chunks"])
    }

def process_data():
    df = pd.read_csv("UpdatedResumeDataSet.csv", encoding="utf-8")
    df.drop_duplicates(subset=["Resume"], keep="first", inplace=True)
    df.reset_index(inplace=True, drop=True)
    df["Clean"] = df["Resume"].apply(clean)
    df["Chunks"] = df["Clean"].apply(shared.chunk)

    ds = Dataset.from_pandas(df)
    ds = ds.map(embed_chunks_map)
    df = ds.to_pandas()
    return df


def embedding_db(df):
    with psycopg.connect("user=postgres") as conn:
        conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {EMBEDDING_TABLE}")
            cur.execute(
                f"""
                CREATE TABLE {EMBEDDING_TABLE}(
                    id serial PRIMARY KEY,
                    source_id integer,
                    chunk text,
                    embedding vector({EMBEDDING_LENGTH})
                )   
                """
            )

            for i, row in df.iterrows():
                embeds = row["Embeddings"]
                chunks = row["Chunks"]
                for j in range(len(embeds)):
                    cur.execute(
                        f"INSERT INTO {EMBEDDING_TABLE} (source_id, chunk, embedding) VALUES (%s, %s, %s)", 
                        (i + 1, chunks[j], embeds[j]) 
                    )
                    # +1 because sql 1 indexed

            for x in cur.execute(f"SELECT id, source_id FROM {EMBEDDING_TABLE}"):
                print(x)

def doc_db(df):
    # going to ignore the embeddings
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {RESUME_DOC_TABLE}")
            cur.execute(
                f"""
                CREATE TABLE {RESUME_DOC_TABLE}(
                    id serial PRIMARY KEY,
                    resume text
                )
                """
            )

            for i, row in df.iterrows():
                cur.execute(f"INSERT INTO {RESUME_DOC_TABLE} (resume) VALUES (%s)", (row["Clean"],))

            for x in cur.execute(f"SELECT * FROM {RESUME_DOC_TABLE}"):
                print(x)            

def add_resume(text):
    cleaned = clean(text)
    chunks = shared.chunk(cleaned)
    embeddings = shared.embed_documents(chunks)
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            length = cur.execute(f"SELECT COUNT (*) FROM  {RESUME_DOC_TABLE}").fetchone()[0]
            cur.execute(f"INSERT INTO {RESUME_DOC_TABLE} (resume) VALUES (%s)", (cleaned,))

            for i in range(len(chunks)):
                cur.execute(
                    f"INSERT INTO {EMBEDDING_TABLE} (source_id, chunk, embedding) VALUES (%s, %s, %s)", 
                    (length, chunks[i], embeddings[i])
                )

def retrieve_resumes(ids: List[int]):
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            data = []
            for id in ids:
                res = cur.execute(f"SELECT resume FROM {RESUME_DOC_TABLE} WHERE id = %s", (id,)).fetchone()[0]
                data.append(res)
            
            return data

if __name__ == "__main__":
    df = process_data()
    embedding_db(df)
    doc_db(df)

    