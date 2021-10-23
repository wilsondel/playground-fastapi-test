# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

#Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()


# Models
class Location(BaseModel):
    city: str
    state: str
    country: str


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

# Validaciones: Query parameters
# /person/detail?name=Miguel%age=25
# Query(...,) -> no es lo ideal, solo se hace para saber que si llega
# a suceder que un query parameter sea obligatorio, y se cambia Optional.
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title = "Person Name",
        description = "This is the person name. It is between 1 and 50 characters"
        ),
    age: str = Query(
        ..., 
        title = "Person Age",
        description = "This is the age of the person. It is required."
        )
):
    return {name:age}


# Validaciones: Path parameters 

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the detailed person information"
        )
):
    return {person_id: "Succeed!"}

# validaciones: request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person updated",
        description = "This is the person id updated"
    ),
    person: Person = Body(...),
    #pido al cliente que me envie, es decir que nos envia 2 json.
    location: Location = Body(...)
):
    # se convierte json a diccionarios 
    results = person.dict()
    # El update es el "append" de los diccionarios
    results.update(location.dict())
    # json con cada llave siendo cada request body.
    return results