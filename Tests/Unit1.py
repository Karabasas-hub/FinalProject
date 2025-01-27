from unittest import mock
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_app import app, table


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Unit test for creating a task with valid data
def test_create_task(client):
    # Create a mock dynamodb put method to not use dynamo db
    with mock.patch.object(table, 'put_item') as mock_put_item:
        data = {
            'id': '3',
            'name': 'test_task_1',
            'due_date': '2025-12-12',
            'status': 'testing'
        }

        response = client.post('/tasks', json=data)

        assert response.status_code == 201
        response_data = response.json
        task = response_data.get('task', {})
        assert task.get('name') == 'test_task_1'
        assert task.get('status') == 'testing'
        assert task.get('due_date') == '2025-12-12T00:00:00'

