from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI

from deploy_chatbot_python.core.index_manager import IndexManager
from deploy_chatbot_python.config import constants


class Query(BaseModel):
    text: str

@asynccontextmanager
async def lifespan(api_: FastAPI):
    """This is used to instantiate `IndexManager` once for the entire lifespan of the API"""
    api_.state.index_manager = IndexManager()
    yield

api = FastAPI(lifespan=lifespan)

@api.get("/")
async def read_root():
    return {"response": "This is a chatbot"}

@api.post(f"/{constants.API_POST_ENDPOINT}")
async def post_query(query: Query):
    response = api.state.index_manager.query(query.text)
    return {"response": response}
