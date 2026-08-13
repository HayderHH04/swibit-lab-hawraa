import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_user_flow():
    unique_id = str(uuid.uuid4())[:8]
    username = f"user_{unique_id}"
    email = f"user_{unique_id}@example.com"
    password = "testpassword123"

    # 1. Register
    user_data = {
        "email": email,
        "username": username,
        "password": password
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code in [200, 201], f"Register failed: {response.text}"

    # 2. Login (تم تغيير username إلى email)
    login_data = {
        "username": email,
        "password": password
    }
    response = client.post("/users/login", data=login_data)
    
    # إذا كان النظام يستقبل JSON بدلاً من Form Data، استخدمي السطر التالي بدلاً من السطر السابق:
    # response = client.post("/users/login", json={"email": email, "password": password})

    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Task
    task_data = {
        "title": "Integration Test Task",
        "description": "Testing the full flow"
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code in [200, 201], f"Create task failed: {response.text}"

    # 4. List Tasks
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200, f"List tasks failed: {response.text}"
    tasks = response.json()
    assert len(tasks) > 0