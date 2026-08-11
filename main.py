from fastapi import FastAPI

from app.routers import users, tasks
from app.core.database import Base, engine

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "healthy"}