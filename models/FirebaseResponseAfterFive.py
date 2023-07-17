from pydantic import BaseModel


class FirebaseData(BaseModel):
    id: int
    date: str
    humidity_above: float
    humidity_below: float
    lux: float
    temperature: float
    status: str
    product_key: str
    median: float
