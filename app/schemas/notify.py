from pydantic import BaseModel


class OrderSampleSchema(BaseModel):
    name: str
    phone: str
    articles: str
    wood_sort: str


class OrderCalculationSchema(BaseModel):
    name: str
    phone: str
    area: str
    article: str | None = None
