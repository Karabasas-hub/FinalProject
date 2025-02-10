import requests
import uuid
import os

BASE_URL = os.getenv("BASE_URL")

def test_get_task():
    task_data = {
        "name": "Retrieve test task",
        "status": "pending from Integrate2",
        "due_date": "2025-03-01"
    }

    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    assert create_response.status_code == 201

    created_task = create_response.json()["task"]
    task_id = created_task["id"]
    print(type(task_id))
    print(created_task)

    retrieve_url = f'{BASE_URL}/{task_id}'
    print(retrieve_url)
    response = requests.get(retrieve_url)

    assert response.status_code == 200
    retrieved_task = response.json()["task"]

    assert retrieved_task["id"] == task_id
    assert retrieved_task["name"] == task_data["name"]
    assert retrieved_task["status"] == task_data["status"]
    assert retrieved_task["due_date"] == '2025-03-01T00:00:00'



