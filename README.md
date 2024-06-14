# FastAPI with PostgreSQL and OpenAI Integration

This project consists of a FastAPI web server that interacts with a PostgreSQL database and the OpenAI API to generate responses based on user interests.

## Explanation

### Imports and Setup

```python
from fastapi import FastAPI
import psycopg2
from openai import OpenAI

app = FastAPI()
```
- Imports: Importing necessary modules: FastAPI for creating the web server, psycopg2 for connecting to PostgreSQL, and OpenAI for interacting with the OpenAI API.

### OpenAI Client and Database Connection:
```python
client = OpenAI(api_key="Your key")
conn = psycopg2.connect(database="your-database", user="postgres", password="admin", host="127.0.0.1", port="5432")
```
- Initializing the OpenAI client with the provided API key.
- Establishing a connection to the PostgreSQL database using the psycopg2 library.

### GPT Model and Completion Function:
```python
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
```
- Setting the GPT model to be used.
- Defining the comp function which takes a prompt, sends it to the OpenAI API, and returns the generated response.
  
### Utility Function to Convert Tuple to String:

```python
def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item + ", "
    return str
```
- This function converts a tuple of user interests into a comma-separated string.

### Database Query and OpenAI Request:
```python
cur = conn.cursor()
cur.execute("SELECT * FROM public.user_intrest;")
results = cur.fetchone()
tupstr = convertTuple(results)
PROMPT = """Create three common questions for this following intrests """
PROMPT += tupstr
output = comp(PROMPT, MaxToken=3000, outputs=3)
```
- Querying the database to fetch user interests.
- Converting the result tuple into a string and appending it to the prompt.
- Sending the prompt to the OpenAI API to generate questions.

### API Endpoint:
```python
@app.get("/api")
async def root():
    return {"message": output}

```
- Creating an API endpoint '/api' which returns the generated output.

