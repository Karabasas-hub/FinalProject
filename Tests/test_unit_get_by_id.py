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

# Unit test to get a task based on ID
def test_get_by_id(client):
        mock_data ={
            'id': str(uuid.uuid4()),
            'name': 'Test task',
            'status': 'testing',
            'due_date': '2025-01-31',
        }
        with mock.patch.object(table, 'get_item') as mock_get_item,\
             mock.patch.object(table, 'put_item') as mock_put_item,
             mock.patch.object(table, 'scan') as mock_scan:
            
            mock_get_item.return_value = {'Item': mock_data}
            mock_put_item.return_value = {}
            mock_scan.return_value = {'Items': [mock_data]}

            response = client.post('/tasks', json=mock_data)
            assert response.status_code == 201
            created_task = response.json
            print(created_task)
                 
            # Mock dynamdb get method to get a mock task back
            assert "id" in created_task["task"]
            assert created_task["task"]["name"] == "Test task"
            assert created_task["task"]["status"] == "testing"
            assert created_task["task"]["due_date"] == "2025-01-31T00:00:00"
        
            task_id = created_task["task"]["id"]
            response = client.get(f'/tasks/{task_id}')
            assert response.status_code == 200
        
            response_data = response.json
            task = response_data.get('task', {})
            assert task.get('name') == "Test task"
            assert task.get('status') == "testing"
            assert task.get('due_date') == "2025-01-31T00:00:00"
