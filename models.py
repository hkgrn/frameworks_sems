from pydantic import BaseModel
from datetime import datetime

# Модели Pydantic
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int