# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# !!! REPLACE WITH YOUR ACTUAL CREDENTIALS (STEP 5) !!!
STUDENT_EMAIL = "24f2005372@ds.study.iitm.ac.in" # <--- REPLACE THIS (KEEP THE QUOTES!)
STUDENT_SECRET = "visishtp2"    # <--- REPLACE THIS (KEEP THE QUOTES!)
# ------------------------------------------

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
        return jsonify({"error": "Invalid secret or email"}), 403 # Error 403 is for unauthorized

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