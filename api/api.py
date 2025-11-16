from flask import Flask, request, jsonify
import os
import requests
import time

app = Flask(__name__)

# --- YOUR FIXED SUPABASE SETTINGS ---
SUPABASE_URL = "https://cvnuwppsgrhzvmlfxxzb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2bnV3cHBzZ3JoenZtbGZ4eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3Nzg3NjEsImV4cCI6MjA3ODM1NDc2MX0.7IhHKZdeIOLUScF4ui2xhSSxlok1FZVdQoUOtXAcaZA"
SUPABASE_TABLE = "messages"
# ------------------------------------

def supabase_headers():
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }

@app.route('/api/send', methods=['POST'])
def send():
    data = request.get_json()
    if not data:
        return jsonify({'error':'no json'}), 400

    payload = {
        "sender": data['sender'],
        "receiver": data['receiver'],
        "enc_message": data['enc_message'],
        "enc_aes_key": data['enc_aes_key'],
        "profile": data.get('profile', None),
        "created_at": int(time.time())
    }

    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=supabase_headers(),
        json=payload
    )
    if r.status_code in (200,201):
        return jsonify({'ok': True}), 201
    else:
        return jsonify({'error': r.text}), r.status_code

@app.route('/api/messages', methods=['GET'])
def messages():
    receiver = request.args.get('receiver')
    since = request.args.get('since', '0')
    if not receiver:
        return jsonify({'error':'receiver required'}), 400

    q = f"?receiver=eq.{receiver}&created_at=gte.{since}&order=created_at.asc"
    r = requests.get(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}{q}", headers=supabase_headers())
    if r.status_code == 200:
        return jsonify(r.json()), 200
    else:
        return jsonify({'error': r.text}), r.status_code

@app.route('/api/ping')
def ping():
    return jsonify({'pong': True})
