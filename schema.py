from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Category(Enum):
    self = 'Self-development'
    business = 'Business'
    literature = 'Literature'
    detective = 'Detective'
    history = 'History'
    romance = 'Romance'
    psychology = 'Psychology'


class Book(BaseModel):
    title: str
    author: str 
    description: str
    language: str
    category: Category
    published: int
    pages: int
    rent_price: int
    price: int
    owner_id: int


class Region(Enum):
    ashgabat = 'ashgabat'
    dashoguz = 'dashoguz'
    lebap = 'lebap'
    mary = 'mary'
    ahal = 'ahal'
    balkan = 'balkan'


class User(BaseModel):
    username: str = Field(max_length=100)
    password : str = Field(max_length=100)
    age: int = Field(ge=5, le=70)
    number: int = Field(ge=60000000, le=65999999)
    email: EmailStr
    region: Region
    address: str = Field(max_length=50)
