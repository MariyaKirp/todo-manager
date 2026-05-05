from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "stats-service",
        "status": "running"
    })


@app.route("/stats", methods=["POST"])
def stats():
    data = request.get_json()
    tasks = data.get("tasks", [])

    total = len(tasks)
    completed = len([task for task in tasks if task.get("completed")])
    active = total - completed
    high_priority = len([task for task in tasks if task.get("priority") == "high"])

    return jsonify({
        "total": total,
        "completed": completed,
        "active": active,
        "high_priority": high_priority
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
