from twilio.rest import Client
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)
# Twilio の認証情報
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TARGET_PHONE_NUMBER = os.environ.get("TARGET_PHONE_NUMBER")

@app.route('/webhook', methods=['POST'])
def handle_report():
    data = request.get_json()
    print(f"Received data: {data}")

    # Twilio クライアント作成
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # 通報の電話を発信
    call = client.calls.create(
        to=TARGET_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url='http://demo.twilio.com/docs/voice.xml'
    )

    print(f"Call initiated, SID: {call.sid}")

    # 20秒後にコールを強制終了
    time.sleep(20)
    call.update(status='completed')

    return jsonify({"status": "Call initiated", "call_sid": call.sid})


# reportStatusの管理
report_status = False  # 初期値はFalse

# reportStatusを返すAPI
@app.route('/get_report_status', methods=['GET'])
def get_report_status():
    global report_status
    return jsonify({"reportStatus": report_status})

# reportStatusを更新するAPI
@app.route('/set_report_status', methods=['POST'])
def set_report_status():
    global report_status
    data = request.get_json()
    if 'status' in data:
        report_status = data['status']
        return jsonify({"status": "success", "reportStatus": report_status}), 200
    else:
        return jsonify({"status": "error", "message": "No status provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
