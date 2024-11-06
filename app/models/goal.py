from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Goal(BaseModel):
    title: str
    description: str
    color: str
    icon: str
    date: date
    expected_income: int
    actual_income: int
    category_id: Optional[str]
