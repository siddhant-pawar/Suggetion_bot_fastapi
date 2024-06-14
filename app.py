from fastapi import FastAPI
import psycopg2
from openai import OpenAI
app = FastAPI()

client = OpenAI(api_key="Your key")

conn = psycopg2.connect(database="your-database", user="postgres", password="admin", host="127.0.0.1", port="5432")

GPT_MODEL = "gpt-4-1106-preview" # select GPT MODEL "gpt-3.5-turbo-1106"
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


def convertTuple(tup):
	str = ''
	for item in tup:
		str = str + item + ", "
	return str

cur = conn.cursor()
cur.execute("SELECT * FROM public.user_intrest;")

# Fetch results from database.
results = cur.fetchone()
tupstr= convertTuple(results)
print(tupstr)	
PROMPT = """Create three common questions for this following intrests """

PROMPT += tupstr
print(PROMPT)
out = comp(PROMPT, MaxToken=3000, outputs=3)
print(out)

cur.close()
conn.close()

@app.get("/api")
async def root():
    return {"message": out}