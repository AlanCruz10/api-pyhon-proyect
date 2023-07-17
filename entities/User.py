from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    name: str
    password: str
    product_key: str
