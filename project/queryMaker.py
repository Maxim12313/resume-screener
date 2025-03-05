import psycopg
from typing import List
from config import Shared, EMBEDDING_TABLE
from database import retrieve_resumes

from dotenv import load_dotenv
from openai import OpenAI

shared = Shared()

def load_resumes(ids: List[int], resumes: List[str]):
    data = ""
    for i in range(len(ids)):
        add = f"### Applicant ID {ids[i]}\n"
        add += resumes[i]
        data += add
    return data 


def get_top_k(prompt: str, k=10):
    prompt = shared.embed_query(prompt)
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            res = cur.execute(f"""SELECT *, embedding <-> %s::vector AS similarity FROM 
                                {EMBEDDING_TABLE} ORDER BY similarity LIMIT %s""",
                                (prompt, k)).fetchall()
            return [
                {
                "score": record[4],
                "source_id": record[1]
                } 
                for record in res
            ]
class QueryMaker:
    client = OpenAI()

    def query(self, prompt: str, developer_prompt="", k=10, temperature=0, model="gpt-4o-mini"):
        if not len(developer_prompt):
            developer_prompt = "You are an expert in talent acquisition and tasked with analyzing and comparing a set resumes to select the best applicants for hire"

        top_k = get_top_k(prompt, k)
        ids = list(set([vals["source_id"] for vals in top_k])) # just get unique
        resumes = retrieve_resumes(ids)
        context = load_resumes(ids, resumes)

        query_prompt = f"""## Context:\n{context}\n\n## Query: {prompt}"""

        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user", 
                    "content":  query_prompt
                }, # task or main prompt
                {
                    "role": "developer", 
                    "content": developer_prompt
                }, # personality 
            ],
            temperature=temperature, # how creative where 0 is deterministic
        )
        text = completion.choices[0].message.content
        return { "text": text, "ids": ids, "resumes": resumes }


if __name__ == "__main__":
    load_dotenv()
    queryMaker = QueryMaker()
    prompt = "give me applicants with the most web development experience and explain why they would be fit for fast development"
    res = queryMaker.query(prompt)
    print(res)