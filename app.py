from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

PRIORITY_SERVICE_URL = os.getenv("PRIORITY_SERVICE_URL", "http://priority-service:5001")
STATS_SERVICE_URL = os.getenv("STATS_SERVICE_URL", "http://stats-service:5002")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default="normal")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def get_task_priority(title):
    """
    Обращение к микросервису priority-service.
    Микросервис получает текст задачи и возвращает ее приоритет.
    """
    try:
        response = requests.post(
            f"{PRIORITY_SERVICE_URL}/priority",
            json={"title": title},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("priority", "normal")
    except requests.RequestException:
        pass

    return "normal"


def get_tasks_stats(tasks):
    """
    Обращение к микросервису stats-service.
    Микросервис получает список задач и возвращает статистику.
    """
    payload = {
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority
            }
            for task in tasks
        ]
    }

    try:
        response = requests.post(
            f"{STATS_SERVICE_URL}/stats",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass

    return {
        "total": len(tasks),
        "completed": len([task for task in tasks if task.completed]),
        "active": len([task for task in tasks if not task.completed]),
        "high_priority": len([task for task in tasks if task.priority == "high"])
    }


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    stats = get_tasks_stats(tasks)
    return render_template("index.html", tasks=tasks, stats=stats)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title:
        priority = get_task_priority(title)
        new_task = Task(title=title, priority=priority)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {
        "service": "todo-manager",
        "status": "running"
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
