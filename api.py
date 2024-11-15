# api.py 파일
from fastapi import FastAPI
from todo import todo_router  # 파일 이름과 라우터 이름을 todo로 수정

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello World"
    }

app.include_router(todo_router)  # 라우터 이름을 todo_router로 변경
