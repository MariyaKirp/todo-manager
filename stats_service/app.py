from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    tasks = []
    if request.is_json:
        tasks = request.json.get('tasks', [])
    completed = len([task for task in tasks if task.get('completed')])
    return jsonify({'total': len(tasks), 'completed': completed, 'active': len(tasks) - completed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
