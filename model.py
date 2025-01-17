from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form

class Todo(BaseModel):
    id: Optional[int] = None  # 기본값은 None
    item: str

    @classmethod
    def as_form(
        cls,
        item: str = Form(...)
    ):
        return cls(item=item)  # 오타 수정: retrun -> return

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Example Schema"
            }
        }

class TodoItem(BaseModel):
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "item": "TEST TEST"
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]  # todos로 일관성 유지

    class Config:
        schema_extra = {
            "example": {
                "todos": [  # 오타 수정: "todo" -> "todos"
                    {
                        "item": "Example schema 1"
                    },
                    {
                        "item": "Example schema 2"
                    }
                ]
            }
        }
