from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )''')

@app.route('/')
def index():
    with get_db() as conn:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        with get_db() as conn:
            conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def done(task_id):
    with get_db() as conn:
        conn.execute('UPDATE tasks SET done = NOT done WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
