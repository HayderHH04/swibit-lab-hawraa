from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/search")
def search_user(name: str):
    return {"name": name}