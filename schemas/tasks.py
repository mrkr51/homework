from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Task description"
    )
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_only_spaces(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title must not be empty or only spaces")
        return cleaned

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_only_spaces(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title must not be empty or only spaces")
        return cleaned

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
