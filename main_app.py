from boto3.dynamodb.conditions import Attr
import boto3
import os
import uuid
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Inicijuojame DynamoDB client'ą
dynamodb = boto3.resource(
    'dynamodb', 
    region_name='eu-central-1',
    endpoint_url = 'http://localhost:8000'    
    )

table = dynamodb.Table('Tasks')

# Pasirašome funkciją paprastesniam tvarkymui datų
def easy_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").isoformat() if date_str else None

def validate_task_data(task_data):
    required_fields = ["name", "status", "due_date"]
    for field in required_fields:
        if field not in task_data:
            raise ValueError(f"Missing required field: {field}")

# Tasko sukūrimo funkcija
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
# 
    # try:
        # validate_task_data(data)
    # except ValueError as e:
        # return jsonify({"error": str(e)}), 400
# 
    table.put_item(Item=new_task)
    return jsonify({"message": "Task created", "task": new_task}), 201
# 
# Funkcija parodyti visus esamus taskus
@app.route('/tasks', methods=['GET'])
def get_tasks():
    search_query = request.args.get('search','')
    response = table.scan()
    tasks = response.get('Items', [])

    # Filtruojami taskai, jei suvestas query
    if search_query:
        tasks = [
            task for task in tasks
            if search_query.lower() in task['name'].lower() or search_query.lower() in task['description'].lower()
        ]
        
    return jsonify({"tasks": tasks}), 200

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        response = table.get_item(Key={'id': task_id})
        task = response.get('Item', None)

        if not task:
            return jsonify({'message': 'Task not found'}), 404
    
        return jsonify({'task': task}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/status/<status>', methods=['GET'])
def get_tasks_by_status(status):
    try:
        # Query su filtru/sąlyga
        response = table.scan(
            FilterExpression=Attr('status').eq(status)
        )
        tasks = response.get('Items', [])

        return jsonify({'tasks': tasks}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    # Nuskenuojamas dabartinis laikas palyginimui su tasko pabaigimo laiku
    try:
        now = datetime.utcnow().isoformat()
        response = table.scan(
            FilterExpression=Attr('due_date').lt(now)
        )
        tasks = response.get('Items', [])

        return jsonify({'tasks': tasks}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Funkcija, skirta atnaujinti taską
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    update_expression = 'SET'
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
    return jsonify({"message:" "Task updated"}), 200

# Funkcija ištrinti taskui
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    response = table.delete_item(Key={"id": task_id})
    return jsonify({"message": "Task deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
