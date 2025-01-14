import boto3
import uuid
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Inicijuojame DynamoDB client'ą
dynamodb = boto3.resource(
    'dynamodb', 
    region_name='eu-central-1',
    endpoint_url = "http://localhost:8080"
    )
table = dynamodb.Table('Tasks')

# Pasirašome funkciją paprastesniam tvarkymui datų
def easy_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").isoformat() if date_str else None

# Tasko sukūrimo funkcija
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    name = data.get('name')
    due_date = easy_date(data.get('due_date'))
    if not name:
        return jsonify({"error": "Task name is required"}), 400
    
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "name": name,
        "status": data.get("status", "pending"),
        "due_date": due_date,
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=new_task)
    return jsonify({"message": "Task created", "task": new_task}), 201

# Funkcija parodyti visus esamus taskus
@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = table.scan()
    tasks = response.get('Items', [])
    return jsonify({"tasks": tasks})

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
    app.run(debug=True)
