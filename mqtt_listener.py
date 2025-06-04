import paho.mqtt.client as mqtt

class MQTTListener:
    def __init__(self, broker, port, topic, on_message_callback):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.on_message_callback = on_message_callback
        self.client = mqtt.Client()

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message_callback
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao MQTT Broker com código", rc)
        client.subscribe(self.topic)