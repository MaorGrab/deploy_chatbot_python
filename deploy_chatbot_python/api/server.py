from pydantic import BaseModel
from fastapi import FastAPI

from deploy_chatbot_python.chatbot.index_manager import IndexManager
from deploy_chatbot_python.config import constants


class Query(BaseModel):
    text: str

api = FastAPI()

@api.get("/")
async def read_root():
    return {"message": "Hello World"}

@api.post(f"/{constants.API_POST_ENDPOINT}")
async def post_query(query: Query):
    index_manager = IndexManager()
    response: str = index_manager.query(query.text)
    return {"response": response}
