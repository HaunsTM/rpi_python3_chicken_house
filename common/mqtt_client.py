from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import random
import string

# -*- coding: utf-8 -*
class mqtt_client:
    
    def __init__(self, broker_address: str, heart_beat_topic: str):
        self._broker_address = broker_address
        self._heart_beat_topic = heart_beat_topic

        self.setup_client()
        self._client.connect(self._broker_address)

    def setup_client(self):
        lowercase_letters = string.ascii_lowercase
        self._mqtt_client_id = ''.join( random.choice( lowercase_letters ) for i in range(10))
        self._client = mqtt.Client( self._mqtt_client_id )

    def get_broker_address(self):
        return self._broker_address

    def get_mqtt_client_id(self):
        return self._mqtt_client_id

    def publish_message(self, mqtt_topic, data):
        self._client.publish(mqtt_topic, data)
        
    def send_heart_beat_message(self):
        utc = datetime.now(timezone.utc).timestamp() * 1000

        self.publish_message(self._heart_beat_topic, str(utc))
    