from datetime import datetime, timezone
from .mqtt_client import mqtt_client

# -*- coding: utf-8 -*
class mqtt_client_reporter(mqtt_client):

    
    def __init__(self, broker_address: str, heart_beat_topic: str):
        super().__init__( broker_address, heart_beat_topic)
        self.last_reported_heart_beat_time = -1
        self.next_time_heart_beat_time = -1

    def send_heart_beat_message_if_it_is_time_to_do_so(self, heart_beat_frequency_ms: int, pid: int):
        utc = datetime.now(timezone.utc).timestamp() * 1000

        if self.next_time_heart_beat_time < utc:
            self.last_reported_heart_beat_time = utc
            self.next_time_heart_beat_time = self.last_reported_heart_beat_time + heart_beat_frequency_ms
            super(mqtt_client_reporter, self).send_heart_beat_message(pid)