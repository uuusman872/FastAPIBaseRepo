from typing import Dict
import uvicorn
from fastapi import FastAPI, Header, status
from baseModels import ResponseBad, ResponseOk
from contextlib import asynccontextmanager
from models.database import init_db
from routes import books_route, user_router

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"[+] Hello this fucked up life :->)")
    await init_db()
    yield
    print(f"[+] Will survive this fucked up life :=?")

app = FastAPI(
    title="This is title here",
    description="A Rest Api Resting",
    version="v1",
    lifespan=life_span
)

app.include_router(books_route.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(user_router.router, prefix="/api/v1/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
