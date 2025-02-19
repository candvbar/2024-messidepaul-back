from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Goal(BaseModel):
    title: str
    description: str
    color: str
    icon: str
    date: str
    expectedIncome: int
    actualIncome: int
    categoryId: Optional[str]
