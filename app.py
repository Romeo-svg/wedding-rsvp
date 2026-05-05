import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import smtplib
from email.message import EmailMessage

# This tells Flask to look in the current folder for everything[cite: 4]
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app) 

# --- CONFIGURATION ---
EMAIL_USER = "roneymwangi24@gmail.com"
EMAIL_PASS = os.environ.get('WEDDING_APP_PASS') 

# 1. This serves the main page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. This serves your CSS, JS, and Images so the site looks good[cite: 1, 2]
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route('/submit-rsvp', methods=['POST'])
def rsvp():
    try:
        data = request.get_json()
        guest_name = data.get('name')
        guest_email = data.get('email')

        msg = EmailMessage()
        msg['Subject'] = f'💍 RSVP: {guest_name}'
        msg['From'] = f"Wedding Planner <{EMAIL_USER}>"
        msg['To'] = EMAIL_USER 
        msg.set_content(f"New Confirmation!\n\nName: {guest_name}\nEmail: {guest_email}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": f"Confirmed! See you there, {guest_name}."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
