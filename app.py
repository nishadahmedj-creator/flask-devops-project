from flask import Flask, jsonify, request
from datetime import datetime 

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return "Welcome to Mini task manager! created by @nishad"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400
    task = {
        "id": len(tasks) + 1,
        "task": data["task"],
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    for task in tasks: 
        if task["id"] == task_id:
            task["status"] = data.get("status", task["status"])
            return jsonify(task)
        
        return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)