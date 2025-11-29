# app.py
from flask import Flask, request, jsonify
# We need requests to send the initial submission POST request to the evaluation server
import requests 

# Assuming you added solver.py in the previous steps
from solver import solve_quiz 

app = Flask(__name__)

# !!! REPLACE WITH YOUR ACTUAL CREDENTIALS !!!
STUDENT_EMAIL = "24f2005372@ds.study.iitm.ac.in" 
STUDENT_SECRET = "visishtp2"    # <--- REPLACE THIS (KEEP THE QUOTES!)
# ------------------------------------------

# --- CRITICAL STATIC URLS FOR QUIZ INITIATION ---
# The URL that identifies the starting quiz task
START_URL = "https://tds-llm-analysis.s-anand.net/project2" 
# The URL where all your answers must be POSTed
SUBMIT_URL_BASE = "https://tds-llm-analysis.s-anand.net/submit"
# HACK: Use the URL as the first answer to start the sequence
INITIAL_ANSWER = START_URL
# -------------------------------------------------


@app.route('/', methods=['GET'])
def status_check():
    return jsonify({"status": "running", "endpoint": "/quiz-solver"}), 200

@app.route('/quiz-solver', methods=['POST'])
def handle_quiz_request():
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Invalid JSON payload"}), 400

    email = payload.get("email")
    secret = payload.get("secret")
    quiz_url = payload.get("url")

    # 1. Verification Check
    if secret != STUDENT_SECRET or email != STUDENT_EMAIL:
        return jsonify({"error": "Invalid secret or email"}), 403

    if not quiz_url:
        return jsonify({"error": "Missing quiz URL"}), 400

    # 2. START THE QUIZ SEQUENCE by making the first submission (REQUIRED by instructions)
    submission_payload = {
        "email": email,
        "secret": secret,
        "url": START_URL,  # Use the static starting URL identifier
        "answer": INITIAL_ANSWER # Use the static placeholder answer
    }

    try:
        # Send the initial POST request to the system's submission endpoint
        initial_response = requests.post(SUBMIT_URL_BASE, json=submission_payload, timeout=30)
        initial_response.raise_for_status()
        
        quiz_init_result = initial_response.json()
        
        # --- SOLVER LOOP START ---
        # If the first submission is correct/accepted, the result will contain the first real quiz URL.
        
        if quiz_init_result.get("url"):
             next_url = quiz_init_result["url"]
             # *** THIS IS WHERE THE FULL SOLVER WOULD BE CALLED ***
             # solver.solve_quiz(email, secret, next_url)
             # For the moment, we confirm the initiation worked.

        return jsonify({
            "message": "Quiz initiation POST successful.", 
            "init_result": quiz_init_result
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal error during quiz initiation POST: {e}"}), 500

# ... (if __name__ == '__main__': ... block)