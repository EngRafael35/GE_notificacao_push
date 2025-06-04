import json
import time
from datetime import datetime, timedelta

from mqtt_listener import MQTTListener
from fcm import send_fcm_notification

service_account_json = os.environ.get("SERVICE_ACCOUNT_JSON")
if not service_account_json:
    raise Exception("A variável de ambiente SERVICE_ACCOUNT_JSON não está definida!")

service_account_info = json.loads(service_account_json)

# Configurações MQTT - ajuste conforme seu broker e tópico
MQTT_BROKER = "broker.emqx.io"  # troque se usar outro broker
MQTT_PORT = 1883
MQTT_TOPIC = "teste"

# Notificação: thresholds e intervalos em horas
NOTIF_RULES = [
    {"threshold": 95, "interval_hours": 1, "message": "ALERTA CRÍTICO! Valor acima de 95!"},
    {"threshold": 85, "interval_hours": 6, "message": "Alerta importante: valor acima de 85."},
    {"threshold": 80, "interval_hours": 12, "message": "Atenção: valor acima de 80."}
]
LAST_NOTIFY = {rule["threshold"]: None for rule in NOTIF_RULES}

def notify_if_needed(value):
    now = datetime.now()
    for rule in NOTIF_RULES:
        if value >= rule["threshold"]:
            last_time = LAST_NOTIFY[rule["threshold"]]
            if not last_time or now - last_time >= timedelta(hours=rule["interval_hours"]):
                print(f"Enviando notificação: {rule['message']}")
                status, resp = send_fcm_notification(
                    service_account_info,
                    MQTT_TOPIC,
                    "ATENÇÃO",
                    rule["message"] + f" Valor atual: {value}"
                )
                print("FCM status:", status, "resp:", resp)
                LAST_NOTIFY[rule["threshold"]] = now
            break # só envia uma notificação por vez, da maior prioridade

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        value = float(payload)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Valor recebido: {value}")
        notify_if_needed(value)
    except Exception as e:
        print("Erro ao processar mensagem:", e)

if __name__ == "__main__":
    listener = MQTTListener(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, on_message)
    listener.start()
    print("Aguardando mensagens MQTT...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Saindo...")

        """ 
            git add .
            git commit -m "atualizaçaõ teste"
            git push origin master

"""