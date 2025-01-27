from unittest import mock
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_app import app, table
import uuid

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test to simulate updating a task
def test_update_task(client):
    mock_data = {
        'id': str(uuid.uuid4()),
        'name': 'Updated test task',
        'status': 'still testing but successful',
        'due_date': '2025-03-11'
    }

    # Mocking dynamodbs post method
    with mock.patch.object(table, 'put_item') as mock_put_item,\
         mock.patch.object(table, 'update_item') as mock_update_item:
        mock_put_item.return_value = {
            'Item': mock_data
        }

        response = client.post('/tasks', json=mock_data)
        print(f"created task response: {response.data}")
        assert response.status_code == 201
        created_task = response.json
        assert "id" in created_task["task"]
        assert created_task["task"]["name"] == "Updated test task"
        assert created_task["task"]["status"] == "still testing but successful"
        task_id = created_task["task"]["id"]
        print(task_id)
    
        update_data = {
            'id': task_id,
            'name': 'Actually updated task',
            'status': 'even more successful',
            'due_date': '2025-03-12'
        }

        response = client.put(f'/tasks/{task_id}', json=update_data)
        print(f"update response: {response.data}")
        assert response.status_code == 200
        assert b'"message": "Task updated"' in response.data
            
        mock_update_item.assert_called_once_with(
            Key={"id": task_id},
            UpdateExpression= "SET #name = :name, #status = :status, due_date = :due_date",
            ExpressionAttributeNames={
                '#name': 'name',
                '#status': 'status'
            },
            ExpressionAttributeValues={
                ":name": update_data['name'],
                ":status": update_data['status'],
                ":due_date": update_data['due_date']
            }
        )