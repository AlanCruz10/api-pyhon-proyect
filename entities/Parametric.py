from pydantic import BaseModel


class Parametric(BaseModel):
    id: int
    date: str
    humidity_above: float
    humidity_below: float
    lux: float
    temperature: float
    status: str
    user_id: int
    statistic_id: int | None = None
