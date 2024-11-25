import json
from flask import Flask, request
import requests
from flask_ngrok import run_with_ngrok
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when the app is run

# Retrieve Slack webhook URL from .env
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Handle favicon.ico requests to avoid 404 errors in the browser
@app.route('/favicon.ico')
def favicon():
    return '', 200

@app.route('/alchemy-webhook', methods=['POST'])
def alchemy_webhook():
    # Extract payload from Alchemy webhook
    alchemy_payload = request.json
    
    # Log the payload to make sure it's received correctly 
    print(f"Received payload: {json.dumps(alchemy_payload, indent=2)}")

    if alchemy_payload:
        # Extract the creation timestamp from the top-level payload
        timestamp = alchemy_payload.get('createdAt', '')
        formatted_date = ""
        
        if timestamp:
            try:
                # Format the timestamp into a human-readable date
                created_at = datetime.fromisoformat(timestamp[:-1])  # Removing 'Z' at the end
                formatted_date = created_at.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = "Invalid date format"

        # Continue processing the payload
        event = alchemy_payload.get('event', {})
        activity = event.get('activity', [])

        slack_message = {"text": "🔔 Alchemy Activity Detected!"}
        message_blocks = []

        for item in activity:
            # Extract relevant info for Slack message
            from_address = item.get('fromAddress', 'Unknown')
            to_address = item.get('toAddress', 'Unknown')
            value = item.get('value', 0)
            asset = item.get('asset', 'Unknown')

            formatted_message = f"Transaction Details:\n" \
                                f"🛸 *From:* {from_address}\n" \
                                f"🚀 *To:* {to_address}\n" \
                                f"💰 *Amount:* {value} {asset}\n" \
                                f"📅 *Date:* {formatted_date}\n"

            message_blocks.append({
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": formatted_message
                    }
                ]
            })

        slack_message['blocks'] = message_blocks

        # Send the message to Slack
        response = requests.post("SLACK_WEBHOOK_URL", json=slack_message)

        # Log Slack response for debugging
        print(f"Slack response status code: {response.status_code}")
        print(f"Slack response text: {response.text}")

        if response.status_code == 200:
            return "Message sent to Slack!", 200
        else:
            return f"Failed to send message: {response.text}", response.status_code
    else:
        return "No payload received", 400

@app.route('/alchemy-webhook', methods=['GET'])
def handle_get():
    return "GET method not allowed on this route", 405

if __name__ == '__main__':
    app.run()  # Don't need to pass debug or port here
