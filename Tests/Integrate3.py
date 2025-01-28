import requests
import uuid

BASE_URL = "http://<ec2-ip>:5000"

def test_delete_task():
    
    task_data = {
        "name": "Delete test task",
        "status": "pending",
        "due_date": "2025-03-02"
    }

    create_response = requests.post(BASE_URL, json=task_data)
    assert create_response.status_code == 201

    created_task = create_response.json()["task"]
    task_id = created_task["id"]

    delete_url = f"{BASE_URL}/tasks/{task_id}"
    response = requests.delete(delete_url)

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

    retrieve_url = f"{BASE_URL}/tasks/{task_id}"
    get_response = requests.get(retrieve_url)
    assert get_response.status_code == 404