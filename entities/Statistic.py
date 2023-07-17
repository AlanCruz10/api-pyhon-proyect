from pydantic import BaseModel


class Statistic(BaseModel):
    id: int
    median: float
    parameter_id: int
