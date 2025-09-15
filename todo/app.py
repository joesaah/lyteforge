import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="LyteForge Todo App"
)

@app.get("/")
def hello_world():
    return "hello world"

def run():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port="80",
    )
