from flask import Flask, request, jsonify
import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = "https://cvnuwppsgrhzvmlfxxzb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2bnV3cHBzZ3JoenZtbGZ4eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3Nzg3NjEsImV4cCI6MjA3ODM1NDc2MX0.7IhHKZdeIOLUScF4ui2xhSSxlok1FZVdQoUOtXAcaZA"

def send_email(to_email, name):
    msg = EmailMessage()
    msg.set_content(f"Hello {name}, your data has been submitted successfully!")
    msg['Subject'] = 'Data Submission Success'
    msg['From'] = "shreeshpitambare084@gmail.com"
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("shreeshpitambare084@gmail.com", "fsyo gokf lnqh yywy")
        smtp.send_message(msg)

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    roll = data.get("roll")

    # 1️⃣ Insert data into Supabase
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"name": name, "email": email, "roll": roll}
    supabase_resp = requests.post(SUPABASE_URL, json=payload, headers=headers)

    if supabase_resp.status_code not in [200, 201]:
        return jsonify({"status": "error", "message": "Failed to store data"}), 500

    # 2️⃣ Send email
    try:
        send_email(email, name)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Email sending failed: {e}"}), 500

    return jsonify({"status": "success", "message": "Data stored and email sent successfully"})
