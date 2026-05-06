import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 

# 1. Initialize the app to look in the current folder for everything
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app) 

# --- CONFIGURATION ---
# Using the second email account you provided
EMAIL_USER = "roneymwangi24@gmail.com"
# Pulls your 16-letter App Password safely from Render's Environment tab
EMAIL_PASS = os.environ.get('WEDDING_APP_PASS') 

# 2. ROUTE: Serves the main page (index.html)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 3. ROUTE: Serves CSS, JS, and Groom.png so the site looks good
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

# 4. ROUTE: Handles the RSVP form submission
@app.route('/submit-rsvp', methods=['POST'])
def rsvp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
            
        guest_name = data.get('name')
        guest_email = data.get('email')

        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = f'💍 RSVP: {guest_name}'
        msg['From'] = f"Wedding Planner <{EMAIL_USER}>"
        msg['To'] = EMAIL_USER 
        msg.set_content(f"New Confirmation!\n\nName: {guest_name}\nEmail: {guest_email}")

        # The PORT 587 + STARTTLS logic that worked for your portfolio
        # This bypasses the 'Network is unreachable' block
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as smtp:
            smtp.starttls()  # This secures the connection manually
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": f"Confirmed! See you there, {guest_name}."}), 200

    except smtplib.SMTPAuthenticationError:
        print("Error: Invalid Gmail App Password.")
        return jsonify({"status": "error", "message": "Authentication failed."}), 500
    except Exception as e:
        print(f"Server Error Details: {e}")
        return jsonify({"status": "error", "message": "Network error. Please try again."}), 500

if __name__ == "__main__":
    # Render provides the port dynamically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
