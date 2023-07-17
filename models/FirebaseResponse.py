from pydantic import BaseModel


class FirebaseResponse(BaseModel):
    date: str
    humidity_above: float
    humidity_below: float
    lux: float
    temperature: float
    status: str
    product_key: str
