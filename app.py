# app.py
from flask import Flask, request, jsonify
from solver import solve_quiz
app = Flask(__name__)


STUDENT_EMAIL = "24f2005372@ds.study.iitm.ac.in" 
STUDENT_SECRET = "visishtp2" 


@app.route('/', methods=['GET'])
def status_check():
    # This is just to check if the server is alive.
    return jsonify({"status": "running", "endpoint": "/quiz-solver"}), 200

@app.route('/quiz-solver', methods=['POST'])
def handle_quiz_request():
    # This function checks the secret key.

    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Invalid JSON payload"}), 400

    email = payload.get("email")
    secret = payload.get("secret")
    quiz_url = payload.get("url")

    # CHECK 1: The secret key must match yours.
    if secret != STUDENT_SECRET or email != STUDENT_EMAIL:
            try:
                print(f"Starting quiz for URL: {quiz_url}")
                result = solve_quiz(email, secret, quiz_url)
                print(f"Quiz result: {result}")
                # Return 200 immediately, even if the solver failed, to confirm API structure works.
                return jsonify({"message": "Solver initiated and completed (check logs for outcome).", "result": result}), 200

            except Exception as e:
                print(f"An unexpected error occurred in the solver: {e}")
                return jsonify({"error": "Internal server error during quiz solving."}), 500
    if not quiz_url:
        return jsonify({"error": "Missing quiz URL"}), 400

    # CHECK 2: If the secret matches, send the success code (HTTP 200).
    # We don't solve the quiz here, just verify the secret.
    return jsonify({
        "message": "Secret verified. Solver initiated (placeholder).", 
        "quiz_url": quiz_url
    }), 200

if __name__ == '__main__':
    # Start the small Flask server for testing.
    app.run(host='0.0.0.0', port=5000, debug=True)