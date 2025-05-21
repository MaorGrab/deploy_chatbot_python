from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from llama_indexing import LlamaIndexer


class Query(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/query")
async def post_query(query: Query):
    llama_indexer = LlamaIndexer()
    response = llama_indexer.query(query.text)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
