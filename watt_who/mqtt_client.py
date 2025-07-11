import os
import json
from typing import Dict, Iterable

import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, prefix: str = "watt_who"):
        host = os.getenv("MQTT_HOST", "homeassistant")
        port = int(os.getenv("MQTT_PORT", "1883"))
        username = os.getenv("MQTT_USERNAME")
        password = os.getenv("MQTT_PASSWORD")
        self.prefix = prefix.rstrip('/')
        self.client = mqtt.Client()
        if username:
            self.client.username_pw_set(username, password)
        self.client.connect(host, port)
        self.client.loop_start()

    def publish_discovery(self, devices: Iterable[str]):
        for device in devices:
            topic = f"homeassistant/sensor/{self.prefix}_{device}/config"
            payload = {
                "name": f"{device} Energy",
                "state_topic": f"{self.prefix}/{device}/energy_kwh",
                "unit_of_measurement": "kWh",
                "unique_id": f"{self.prefix}_{device}_energy",
                "device_class": "energy",
            }
            self.client.publish(topic, json.dumps(payload), retain=True)

    def publish_state(self, energy: Dict[str, float]):
        for device, value in energy.items():
            topic = f"{self.prefix}/{device}/energy_kwh"
            self.client.publish(topic, f"{value:.4f}", retain=True)
