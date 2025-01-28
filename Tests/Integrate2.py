import requests
import uuid

BASE_URL = "http://<ec2-ip>:5000"

def test_get_task():
    task_data = {
        "name": "Retrieve test task",
        "status": "pending",
        "due_date": "2025-03-01"
    }

    create_response = requests.post(BASE_URL, json=task_data)
    assert create_response.status_code == 201

    created_task = create_response.json()["task"]
    task_id = created_task["id"]

    retrieve_url = f"{BASE_URL}/tasks/{task_id}"
    response = requests.get(retrieve_url)

    assert response.status_code == 200
    retrieved_task = response.json()["task"]

    assert retrieved_task["id"] == task_id
    assert retrieved_task["name"] == task_data["name"]
    assert retrieved_task["status"] == task_data["status"]
    assert retrieved_task["due_date"] == task_data["due_date"]

    

