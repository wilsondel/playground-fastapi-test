
#Fast API
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World!"}

# Resquest and Response Body

@app.post("/person/new")
def create_person():
    pass
