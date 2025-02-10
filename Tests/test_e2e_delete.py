import requests
import os

BASE_URL = os.getenv("BASE_URL")

def test_delete_task():

    create_response = requests.post(f"{BASE_URL}/tasks", json={
        "name": "Task to update",
        "status": "still pending from E2E2",
        "due_date": "2025-02-01"
    })

    assert create_response.status_code == 201
    task = create_response.json()["task"]
    task_id = task["id"]
    print(f"Task created for update: {task_id}")

    delete_response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert delete_response.status_code == 200

    check_deleted = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert check_deleted.status_code == 404
    

