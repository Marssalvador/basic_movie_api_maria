from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2024)
    rating: float = Field(ge=0, le=10)
    category: str = Field(max_length=15, min_length=5)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Avatar",
                "overview": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
                "year": 2009,
                "rating": 7.8,
                "category": "Action",
            }
        }
