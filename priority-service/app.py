from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "priority-service",
        "status": "running"
    })


@app.route("/priority", methods=["POST"])
def priority():
    data = request.get_json()
    title = data.get("title", "").lower()

    high_priority_words = [
        "срочно",
        "важно",
        "дедлайн",
        "экзамен",
        "отчет",
        "контрольная",
        "практическая"
    ]

    if any(word in title for word in high_priority_words):
        priority_value = "high"
    else:
        priority_value = "normal"

    return jsonify({
        "title": title,
        "priority": priority_value
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
