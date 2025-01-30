from unittest import mock
import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_app import app, table
import uuid

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test to simulate updating a task
def test_update_task(client):
    task_id = 'test-task-id'
    update_data = {
        'name': 'New and improved test task',
        'status': 'actually completed wow',
        'due_date': '2025-01-01'
    }

    with mock.patch.object(table, 'update_item') as mock_update_item:
        mock_update_item.return_value = {}
       

        response = client.put(f'/tasks/{task_id}', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Task updated'

        mock_update_item.assert_called_once_with(
            Key={"id": task_id},
            UpdateExpression="SET name = :name, status = :status, due_date = :due_date",
            ExpressionAttributeValues={
                ':name': update_data['name'],
                ':status': update_data['status'],
                ':due_date': '2025-01-01T00:00:00'
            }
        )