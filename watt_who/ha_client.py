import os
from typing import Dict
import requests

class HaClient:
    def __init__(self, prefix: str = "watt_who", base_url: str = "http://supervisor/core/api"):
        self.prefix = prefix.rstrip("/")
        self.base_url = base_url.rstrip("/")
        token = os.getenv("SUPERVISOR_TOKEN")
        if not token:
            raise RuntimeError("SUPERVISOR_TOKEN not set")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def publish_state(self, energy: Dict[str, float], running: Dict[str, bool]):
        for device, value in energy.items():
            entity_id = f"sensor.{self.prefix}_{device}_energy"
            url = f"{self.base_url}/states/{entity_id}"
            payload = {
                "state": f"{value:.4f}",
                "attributes": {
                    "unit_of_measurement": "kWh",
                    "device_class": "energy",
                    "state_class": "total_increasing",
                },
            }
            resp = self.session.post(url, json=payload)
            resp.raise_for_status()

            run_id = f"binary_sensor.{self.prefix}_{device}_running"
            run_url = f"{self.base_url}/states/{run_id}"
            run_payload = {
                "state": "on" if running.get(device, False) else "off",
                "attributes": {"device_class": "running"},
            }
            resp = self.session.post(run_url, json=run_payload)
            resp.raise_for_status()
