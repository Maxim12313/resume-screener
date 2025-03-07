from typing import List, Dict
from config import Shared
from database import get_top_k
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
shared = Shared()


def load_resumes(top_k: List[Dict]):
    data = ""
    for record in top_k:
        add = f"### Applicant ID {record['source_id']}\n"
        add += record["resume"]
        data += add
    return data


def get_unique(top_k: List[Dict]):
    res = []
    seen = set()
    for record in top_k:
        if record["source_id"] in seen:
            continue
        res.append(record)
        seen.add(record["source_id"])
    return res


class QueryMaker:
    system_prompt = None
    model = None
    temperature = None
    k = None
    client = OpenAI()

    def __init__(self, k=10, temperature=0, model="gpt-4o-mini", system_prompt=""):
        self.k = k
        self.temperature = temperature
        self.model = model
        self.system_prompt = (
            system_prompt
            if len(system_prompt)
            else (
                "You are an expert in talent acquisition and tasked with analyzing and comparing"
                "a set resumes to select the best applicants for hire"
            )
        )

    def query(
        self,
        prompt: str,
        prev_relevant: List[Dict],
        prev_convo: List[Dict],
    ):
        embedded = shared.embed_query(prompt)

        top_k = get_top_k(embedded, self.k) + prev_relevant
        top_k = get_unique(top_k)

        context = load_resumes(top_k)

        prompt += "Also at the end, return a JSON array of most relevant resume integer ids delimited by ``` on last 3 lines"

        query_prompt = f"""## Context:\n{context}\n\n## Query: {prompt}"""

        messages = prev_convo
        messages += [
            {"role": "user", "content": query_prompt},  # task or main prompt
            {"role": "system", "content": self.system_prompt},  # personality
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,  # how creative where 0 is deterministic
            messages=messages,
            stream=True,
        )

        return {"text": completion, "top_k": top_k}


if __name__ == "__main__":
    queryMaker = QueryMaker()
    prompt = "give me applicants with the most web development experience and explain why they would be fit for fast development"
    res = queryMaker.query(prompt)
    print(res)
