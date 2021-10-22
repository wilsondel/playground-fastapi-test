# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

#Fast API
from fastapi import FastAPI
from fastapi import Body


app = FastAPI()


# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World!"}

# Resquest and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)): # ... -> significa que es obligatorio
    return person