from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
TASKS = []
NEXT_ID = 1


@app.route('/')
def index():
    try:
        stats = requests.post(
            'http://stats-service:5002/stats',
            json={'tasks': TASKS},
            timeout=2
        ).json()
    except Exception:
        completed = len([task for task in TASKS if task.get('completed')])
        stats = {
            'total': len(TASKS),
            'completed': completed,
            'active': len(TASKS) - completed
        }

    important = len([task for task in TASKS if task.get('priority') == 'высокий'])

    return render_template(
        'index.html',
        tasks=TASKS,
        stats=stats,
        important=important
    )


@app.route('/add', methods=['POST'])
def add():
    global NEXT_ID

    title = request.form.get('title', '').strip()

    if title:
        try:
            priority = requests.post(
                'http://priority-service:5001/priority',
                json={'title': title},
                timeout=2
            ).json()['priority']
        except Exception:
            priority = 'обычный'

        TASKS.append({
            'id': NEXT_ID,
            'title': title,
            'completed': False,
            'priority': priority
        })

        NEXT_ID += 1

    return redirect('/')


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    for task in TASKS:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

    return redirect('/')


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    global TASKS
    TASKS = [task for task in TASKS if task['id'] != task_id]
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)