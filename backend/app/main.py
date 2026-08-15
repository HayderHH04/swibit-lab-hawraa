from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import users, tasks
from app.core.database import Base, engine
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("application starting")
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/health")
def health():
    return {"status": "healthy"}
