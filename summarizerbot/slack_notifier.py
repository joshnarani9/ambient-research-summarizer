import requests
import os

# Slack webhook
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def send_to_slack(message: str):
    """Send summarized research update to Slack channel"""
    try:
        payload = {"text": message}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"⚠️ Slack error: {response.text}")
    except Exception as e:
        print(f"⚠️ Failed to send Slack message: {e}")
