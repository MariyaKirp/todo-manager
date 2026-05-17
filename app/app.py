from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)
TASKS = []

HTML = '''
<!doctype html>
<html lang="ru">
<head><meta charset="UTF-8"><title>To-Do Manager</title></head>
<body>
<h1>To-Do менеджер</h1>
<form method="post" action="/add">
  <input name="title" placeholder="Введите задачу" required>
  <button type="submit">Добавить</button>
</form>
<ul>
{% for task in tasks %}
<li>{{ task.title }} | приоритет: {{ task.priority }} | всего задач: {{ stats.total }}</li>
{% endfor %}
</ul>
</body>
</html>
'''

@app.route('/')
def index():
    try:
        stats = requests.get('http://stats-service:5002/stats', json={'tasks': TASKS}, timeout=2).json()
    except Exception:
        stats = {'total': len(TASKS)}
    return render_template_string(HTML, tasks=TASKS, stats=stats)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    try:
        priority = requests.post('http://priority-service:5001/priority', json={'title': title}, timeout=2).json()['priority']
    except Exception:
        priority = 'обычный'
    TASKS.append({'title': title, 'completed': False, 'priority': priority})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
