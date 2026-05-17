from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/priority', methods=['POST'])
def priority():
    title = request.json.get('title', '').lower()
    urgent_words = ['срочно', 'важно', 'deadline', 'экзамен', 'отчет']
    priority_value = 'высокий' if any(word in title for word in urgent_words) else 'обычный'
    return jsonify({'priority': priority_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
