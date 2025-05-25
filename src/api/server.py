from pydantic import BaseModel
from fastapi import FastAPI

from src.chatbot.index_manager import IndexManager


class Query(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/query")
async def post_query(query: Query):
    index_manager = IndexManager()
    response = index_manager.llama_indexer._query(query.text)
    return {"response": response}
