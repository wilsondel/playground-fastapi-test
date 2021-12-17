# Python
from typing import Optional
from enum import Enum
# Enum allows to just accept the values that we define in 
# the type of data we are creating. "Exotic" data and those can
# be also imported from optional.

# Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field
# Field allows to do validations over the models

#Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path
# Body allows to do validations over body request
# Query allows to do validations over query parameters
# Path allows to do validations over path parameters 


app = FastAPI()


# Models

class HairColor(Enum):
    white= "white"
    brown= "brown"
    black= "black"
    red= "red"
    blonde= "blonde"

class Country(Enum):
    colombia = "colombia"
    argentina= "argentina"
    brazil= "brazil"
    united_states = "united_states"
    mexico= "mexico"
    spain= "spain"


class Location(BaseModel):
    city: str = Field(
        ..., 
        example = "bogota"
    )
    state: str = Field(
        ..., 
        example = "cundinamarca"
    )
    country: Country = Field(
        ..., 
        example = "colombia"
    )


class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example= "Alirio"
        )
    last_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example = "Hernandez"
        )
    age: int = Field(
        ...,
        gt=0,
        le= 120,
        example = 20
    )
    email: EmailStr
    hair_color: Optional[HairColor] = Field(deault=None, example = "red")
    is_married: Optional[bool] = Field(deault = None, example = True)
    password: str = Field(..., min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example":{
    #             "first_name": "Wilson",
    #             "last_name": "Delgado",
    #             "age": 19,
    #             "email": "wilsondelgado.her@gmail.com",
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }


class PersonOut(BaseModel):
    first_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example= "Alirio"
        )
    last_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example = "Hernandez"
        )
    age: int = Field(
        ...,
        gt=0,
        le= 120,
        example = 20
    )
    email: EmailStr
    hair_color: Optional[HairColor] = Field(deault=None, example = "red")
    is_married: Optional[bool] = Field(deault = None, example = True)

@app.get("/")
def home():
    return {"Hello": "World!"}

# Resquest and Response Body

# Response model: response_model= PersonOut
@app.post("/person/new", response_model=Person, response_model_exclude={"password"})
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
        description = "This is the person name. It is between 1 and 50 characters",
        example = "Sofia"
        ),
    age: str = Query(
        ..., 
        title = "Person Age",
        description = "This is the age of the person. It is required.",
        example = 11
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
        description="This is the detailed person information",
        example= 123
        )
):
    return {person_id: "Succeed!"}

# validaciones: request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person updated",
        description = "This is the person id updated",
        example = 123
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
    #return person