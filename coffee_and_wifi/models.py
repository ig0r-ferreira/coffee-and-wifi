from pydantic import BaseModel, Field, HttpUrl


class Cafe(BaseModel):
    name: str = Field(..., alias='cafe_name')
    location: HttpUrl = Field(..., alias='cafe_location')
    opening_time: str
    closing_time: str
    coffee_rating: int
    wifi_rating: int
    power_rating: int

    class Config:
        allow_population_by_field_name = True
