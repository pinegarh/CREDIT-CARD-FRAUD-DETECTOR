from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

@app.route('/')
def home():
    return send_file('inde.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        amount = float(data.get('Amount', 0))
        time = float(data.get('Time', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Amount and Time must be numeric'}), 400

    if amount < 0 or time < 0:
        return jsonify({'error': 'Amount and Time must be non-negative'}), 400

    # Simple rule-based scorer for demonstration.
    # Replace this with a real ML model once you have one trained and saved.
    score = 0.0
    score += min(amount / 100.0, 10.0)
    score += 5.0 if amount > 1000 else 0.0
    score += 3.0 if time < 60 else 0.0
    score += 2.0 if time < 10 else 0.0

    is_fraud = score >= 8.0

    return jsonify({
        'is_fraud': is_fraud,
        'score': round(score, 2),
        'message': 'High risk' if is_fraud else 'Low risk'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')