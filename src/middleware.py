from src.main import app
from fastapi import Request, Response


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        # some logging
        print(ex)
        return Response("Internal server error", status_code=500)
