import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
import tempfile
import os

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

    # Salva o JSON temporariamente para o google-auth usar
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp_json:
        json.dump(service_account_info, tmp_json)
        tmp_json.flush()

        credentials = service_account.Credentials.from_service_account_file(
            tmp_json.name,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        access_token = credentials.token

    os.unlink(tmp_json.name)  # Remove o arquivo temporário

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }
    response = requests.post(url, headers=headers, data=json.dumps(message))
    return response.status_code, response.text