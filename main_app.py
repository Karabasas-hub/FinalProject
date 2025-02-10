from boto3.dynamodb.conditions import Attr
import boto3
import os
import uuid
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Initializing DynamoDB client
dynamodb = boto3.resource(
    'dynamodb', 
    region_name='eu-central-1',   
    )

table = dynamodb.Table('Tasks')

# Function for handling of dates
def easy_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").isoformat() if date_str else None

def validate_task_data(task_data):
    required_fields = ["name", "status", "due_date"]
    for field in required_fields:
        if field not in task_data:
            raise ValueError(f"Missing required field: {field}")

# Function to create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Task name is required"}), 400
    task_id = str(uuid.uuid4())
    due_date = data.get('due_date')
    if due_date:
        try:
            due_date = datetime.fromisoformat(due_date).isoformat()
        except ValueError:
            print("Invalid date format or missing due date:", due_date)
    new_task = {
        "id": task_id,
        "name": name,
        "status": data.get("status", "pending"),
        "due_date": due_date,
        "created_at": datetime.utcnow().isoformat()
    }
    table.put_item(Item=new_task)
    return jsonify({"message": "Task created", "task": new_task}), 201

# Function to view all created tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    search_query = request.args.get('search','')
    response = table.scan()
    tasks = response.get('Items', [])

    # Filtering of tasks
    if search_query:
        tasks = [
            task for task in tasks
            if search_query.lower() in task['name'].lower() or search_query.lower() in task['description'].lower()
        ]
        
    return jsonify({"tasks": tasks}), 200

# Function to get task by unique ID
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        response = table.scan(FilterExpression=Attr('id').eq(task_id))

        if not response['Items']:
            return jsonify({'message': 'Task not found'}), 404

        task = response['Items'][0]
        return jsonify({'task': task}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to retrieve tasks by status
@app.route('/tasks/status/<status>', methods=['GET'])
def get_tasks_by_status(status):
    try:
        # Query with a filter/condition
        response = table.scan(
            FilterExpression=Attr('status').eq(status)
        )
        tasks = response.get('Items', [])

        return jsonify({'tasks': tasks}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to retrieve overdue tasks
@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    # Getting the current time to compare with the due date of the task
    try:
        now = datetime.utcnow().isoformat()
        response = table.scan(
            FilterExpression=Attr('due_date').lt(now)
        )
        tasks = response.get('Items', [])

        return jsonify({'tasks': tasks}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Function to update a task
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    update_expression = 'SET '
    expression_values = {}
    if 'name' in data:
        update_expression += "name = :name, "
        expression_values[":name"] = data['name']
    if 'status' in data:
        update_expression += "status = :status, "
        expression_values[":status"] = data['status']
    if 'due_date' in data:
        update_expression += "due_date = :due_date, "
        expression_values[":due_date"] = easy_date(data['due_date'])

    update_expression = update_expression.rstrip(", ")

    if not expression_values:
        return jsonify({"error:" "Nothing to update"}), 400
    
    table.update_item(
        Key = {"id": task_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    return jsonify({"message": "Task updated"}), 200

# Function to delete a task by ID
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        response = table.scan(FilterExpression=Attr('id').eq(task_id))
        if not response["Items"]:
            return jsonify({"error": "Task not found"}), 404
        
        task = response["Items"][0]
        due_date = task.get('due_date')

        if not due_date:
            return jsonify({"error": "Task due_date missing"}), 400
        
        table.delete_item(Key={'id': task_id, 'due_date': due_date})

        return jsonify({"message": "Task deleted successfully"}), 200
    
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
