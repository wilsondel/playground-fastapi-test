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
from fastapi import Body, Query, Path, Form
# Body allows to do validations over body request
# Query allows to do validations over query parameters
# Path allows to do validations over path parameters 
# Form allows to do validations and indicate over form parameters 
from fastapi import status
# it allows to access different status codes


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

class PersonBase(BaseModel):
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


class Person(PersonBase):
    password: str = Field(
        ..., 
        min_length=8,
        example="superSecreto")

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


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username : str = Field(
        ..., 
        max_length = 20,
        example = "wilson222002")
    message : str = Field(
        default = "Login successful"
    )

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World!"}

# Resquest and Response Body

# Response model: response_model= PersonOut
@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)): # ... -> significa que es obligatorio
    return person

# Validaciones: Query parameters
# /person/detail?name=Miguel%age=25
# Query(...,) -> no es lo ideal, solo se hace para saber que si llega
# a suceder que un query parameter sea obligatorio, y se cambia Optional.
@app.get(
    path="/person/detail",
    status_code = status.HTTP_200_OK
    )
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

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

# Working with forms
@app.post(
    path='/login',
    response_model = LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
): 
    return LoginOut(username=username)

