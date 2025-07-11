import argparse
import os
import random
import time

from .config import load_config
from .tracker import PowerTracker
from .mqtt_client import MqttClient
from .ha_client import HaClient


def main():
    parser = argparse.ArgumentParser(description="Simple power tracker")
    parser.add_argument('--config', default='/config/devices.yml', help='Path to device config')
    parser.add_argument('--interval', type=float, default=1.0, help='Sampling interval in seconds')
    args = parser.parse_args()

    devices = load_config(args.config)
    tracker = PowerTracker(devices)

    mqtt_client = None
    if os.getenv("MQTT_DISABLE") != "1":
        mqtt_client = MqttClient()
        mqtt_client.publish_discovery(devices.keys())

    ha_client = None
    if os.getenv("HOMEASSISTANT_API", "false").lower() == "true":
        ha_client = HaClient()

    try:
        while True:
            # In a real application, replace this with actual sensor reading
            current_power = random.uniform(0, 1000)
            tracker.update_power(current_power)
            energy = tracker.get_energy_kwh()
            print('\r' + ', '.join(f"{name}: {val:.4f} kWh" for name, val in energy.items()), end='')
            if mqtt_client:
                mqtt_client.publish_state(energy)
            if ha_client:
                ha_client.publish_state(energy)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print()  # newline
        for name, val in tracker.get_energy_kwh().items():
            print(f"{name}: {val:.4f} kWh")


if __name__ == '__main__':
    main()
