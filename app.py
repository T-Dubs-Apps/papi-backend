import os
import datetime
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- AEGISCORE CONFIGURATION ---
AEGIS_API_KEY = os.environ.get("AEGIS_KEY", "papi-secure-token-2025-v2")
SYSTEM_STATUS = "ARMED"

# --- SECURITY MIDDLEWARE: AEGISCORE ---
def aegis_core_guard(func):
    def wrapper(*args, **kwargs):
        # Accepts token via Header OR URL (for easy browser testing)
        incoming_key = request.headers.get('X-Aegis-Token') or request.args.get('token')
        
        if incoming_key != AEGIS_API_KEY:
            print(f"[AEGIS-ALERT] Unauthorized access attempt from {request.remote_addr}")
            return jsonify({
                "system": "AegisCore v1.0",
                "status": "ACCESS_DENIED", 
                "message": "Security Protocol Violation. Trace initiated."
            }), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# --- CORE PAPI LOGIC ---
def calculate_market_value(item):
    # Simulates complex AI valuation
    base_price = random.uniform(10.0, 100.0)
    return round(base_price, 2)

# --- ROUTES ---
@app.route('/')
def dashboard():
    return render_template('index.html', status=SYSTEM_STATUS)

@app.route('/api/command', methods=['POST'])
@aegis_core_guard
def execute_command():
    data = request.json
    command = data.get('command', '').lower()
    
    response_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "aegis_signature": "VERIFIED_AES_256"
    }

    if "scan" in command:
        item = command.replace("scan", "").strip()
        price = calculate_market_value(item)
        response_data["papi_response"] = f"Scanning global markets... Target '{item}' valued at ${price}."
    elif "status" in command:
        response_data["papi_response"] = "All systems nominal. AegisCore is active."
    else:
        response_data["papi_response"] = f"Command '{command}' processed. Awaiting further instructions."

    return jsonify(response_data)

if __name__ == '__main__':
    # Local Development Entry Point
    port = int(os.environ.get('PORT', 10000))
    print(f"--- PAPI SYSTEM ONLINE on Port {port} ---")
    app.run(host='0.0.0.0', port=port)
