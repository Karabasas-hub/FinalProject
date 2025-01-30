import requests
import os

BASE_URL = os.getenv("BASE_URL")

def test_create_get_task():

    create_response = requests.post(f"{BASE_URL}/tasks", json={
        "name": "Test task",
        "status": "pendingasasasas",
        "due_date": "2025-01-30"
    })

    assert create_response.status_code == 201
    task = create_response.json()["task"]
    task_id = task["id"]
    print(f"Task created: {task_id}")

    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()["task"]
    assert retrieved_task["name"] == "Test task"