import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 

# 1. Initialize the app to look in the current folder for all files
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app) 

# --- CONFIGURATION ---
EMAIL_USER = "roneymwangi24@gmail.com"
# Pulls your 16-letter App Password safely from Render's Environment tab[cite: 4]
EMAIL_PASS = os.environ.get('WEDDING_APP_PASS') 

# 2. ROUTE: Serves the main RSVP page[cite: 5]
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 3. ROUTE: Serves CSS, JS, and Images so the site looks beautiful[cite: 1, 2]
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

# 4. ROUTE: Handles the RSVP form submission[cite: 4]
@app.route('/submit-rsvp', methods=['POST'])
def rsvp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
            
        guest_name = data.get('name')
        guest_email = data.get('email')

        # Create the email message[cite: 4]
        msg = EmailMessage()
        msg['Subject'] = f'💍 RSVP: {guest_name}'
        msg['From'] = f"Wedding Planner <{EMAIL_USER}>"
        msg['To'] = EMAIL_USER 
        msg.set_content(f"New Confirmation!\n\nName: {guest_name}\nEmail: {guest_email}")

        # Connect to Gmail with a 10-second timeout to prevent Render crashes[cite: 4]
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": f"Confirmed! See you there, {guest_name}."}), 200

    except smtplib.SMTPAuthenticationError:
        print("Error: Invalid Gmail App Password.")
        return jsonify({"status": "error", "message": "Server authentication failed."}), 500
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"status": "error", "message": "Server error. Please try again."}), 500

if __name__ == "__main__":
    # Render provides the port dynamically[cite: 4]
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
