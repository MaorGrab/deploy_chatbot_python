from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn


class Item(BaseModel):
    number_1: int
    number_2: int
    
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/sum")
async def sum(item: Item):
    result = item.number_1 + item.number_2
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run("fastapi_try:app", host="127.0.0.1", port=8000, reload=True)
