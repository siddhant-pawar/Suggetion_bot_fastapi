from fastapi import FastAPI
import psycopg2
from openai import OpenAI
import os

app = FastAPI()

# Securely load sensitive information from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

GPT_MODEL = "gpt-4-1106-preview"

def comp(PROMPT, MaxToken=50, outputs=3): 
    messages = [
        {"role": "system", "content": PROMPT},
    ]
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message

def convert_tuple_to_str(tup):
    return ', '.join(tup)

@app.get("/api")
async def root():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.user_intrest;")
            results = cur.fetchone()
            if not results:
                return {"message": "No user interests found."}
            tupstr = convert_tuple_to_str(results)
    
    PROMPT = "Create three common questions for these interests: " + tupstr
    output = comp(PROMPT, MaxToken=3000, outputs=3)
    
    return {"message": output}
