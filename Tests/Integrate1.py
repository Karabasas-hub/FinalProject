import requests 
import uuid

BASE_URL = "http://63.176.109.247:5000/tasks"

def test_create_task():

    task_data = {
        "name": f"Test task {uuid.uuid4()}",
        "status": "pending",
        "due_date": "2025-02-28"
    }

    response = requests.post(BASE_URL, json=task_data)
    
    assert response.status_code == 201
    response_data = response.json()
    assert "task" in response_data
    assert response_data["task"]["name"] == task_data["name"]
    assert response_data["task"]["status"] == task_data["status"]
    assert response_data["task"]["due_date"] == '2025-02-28T00:00:00'

