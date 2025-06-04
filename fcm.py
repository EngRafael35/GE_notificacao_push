import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

PROJECT_ID = "teste-apk-29017a"

def send_fcm_notification(service_account_info, topic, title, body):
    message = {
        "message": {
            "topic": topic,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    access_token = credentials.token

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }
    response = requests.post(url, headers=headers, data=json.dumps(message))
    return response.status_code, response.text