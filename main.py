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

@app.get("/users")
def get_users():
    return []

@app.post("/users")
def create_user():
    return {"message": "User created"}

@app.put("/users/{user_id}")
def update_user(user_id: int):
    return {"message": "User updated", "user_id": user_id}
	
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": "User deleted", "user_id": user_id}
	
@app.get("/tasks")
def get_tasks():
    return []	

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}	

@app.post("/tasks")
def create_task():
    return {"message": "Task created"}	

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    return {"message": "Task updated", "task_id": task_id}	

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return {"message": "Task deleted", "task_id": task_id}	

