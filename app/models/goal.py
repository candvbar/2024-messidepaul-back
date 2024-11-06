from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Goal(BaseModel):
    title: str
    description: str
    color: str
    icon: str
    date: date
    expected_income: int = Field(..., alias="expectedIncome")
    actual_income: int = Field(..., alias="actualIncome")
    category_id: Optional[int] = Field(None, alias="categoryId")
    progress_value: Optional[int] = None
