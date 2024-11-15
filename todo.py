from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter(tags=["todo application"],)

# 메모리 내 리스트로 todo 항목 저장
todo_list = []

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates/")

# 새로운 todo 항목 추가 (POST)
@todo_router.post("/todo", status_code=201)
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse(
        "todo.html",
        {
            "request": request,
            "todo": todo,  # 추가된 단일 todo 항목 렌더링
            "todos": todo_list  # 전체 목록도 제공하여 리스트 갱신 가능
        }
    )

# 전체 todo 항목 조회 (GET)
@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos(request: Request):
    return templates.TemplateResponse(
        "todo.html",  # todo.html 파일로 전체 목록 렌더링
        {
            "request": request,
            "todos": todo_list  # 전체 todo 리스트 전달
        }
    )

# 특정 ID로 todo 항목 조회 (GET)
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(request: Request, todo_id: int = Path(..., title="특정 todo  를 확인하기 위한 ID", ge=1, le=1000)):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                "todo.html",  # 단일 todo 항목 HTML 템플릿 렌더링
                {
                    "request": request,
                    "todo": todo,  # 선택한 todo 항목 전달
                    "todos": todo_list  # 전체 목록도 함께 전달
                }
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 ID 입니다"
    )

# 특정 ID의 todo 항목 업데이트 (PUT)
@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="변경할 아이템의 ID")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "todo 가 업데이트 되었습니다"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 ID 입니다"
    )

# 전체 todo 항목 삭제 (DELETE)
@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return { "message": "모든 todo 가 삭제되었습니다" }

# 특정 ID의 todo 항목 삭제 (DELETE)
@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return { "message": "삭제되었습니다" }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 ID 입니다"
    )
