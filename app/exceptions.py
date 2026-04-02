from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 404):
        self.code = code
        self.message = message
        self.status_code = status_code

class TaskNotFound(AppException):
    def __init__(self):
        super().__init__(code="TASK_NOT_FOUND", message="Задача не найдена")

class CommentNotFound(AppException):
    def __init__(self):
        super().__init__(code="COMMENT_NOT_FOUND", message="Комментарий не найден")

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )