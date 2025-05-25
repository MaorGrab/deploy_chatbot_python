import uvicorn

from src.api.server import app

if __name__ == "__main__":
    uvicorn.run("run:app", host="localhost", port=8000, reload=True)