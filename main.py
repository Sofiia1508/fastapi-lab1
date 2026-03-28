from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Lab 1 is finished!", "branch": "dev"}