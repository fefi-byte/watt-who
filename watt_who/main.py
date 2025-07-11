import argparse
import logging
import os
import random
import time

from .config import load_config
from .tracker import PowerTracker
from .ha_client import HaClient


def main():
    parser = argparse.ArgumentParser(description="Simple power tracker")
    parser.add_argument('--config', default='/config/devices.yml', help='Path to device config')
    parser.add_argument('--interval', type=float, default=1.0, help='Sampling interval in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug or os.getenv('DEBUG') == '1' else logging.INFO,
                        format='[%(levelname)s] %(message)s')

    devices = load_config(args.config)
    tracker = PowerTracker(devices)

    ha_client = HaClient()

    try:
        while True:
            # In a real application, replace this with actual sensor reading
            current_power = random.uniform(0, 1000)
            tracker.update_power(current_power)
            energy = tracker.get_energy_kwh()
            running = tracker.get_running_states()
            logging.info(', '.join(f"{name}: {val:.4f} kWh" for name, val in energy.items()))
            logging.debug(', '.join(f"{name} running: {'on' if state else 'off'}" for name, state in running.items()))
            ha_client.publish_state(energy, running)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        for name, val in tracker.get_energy_kwh().items():
            logging.info(f"{name}: {val:.4f} kWh")
        for name, state in tracker.get_running_states().items():
            logging.info(f"{name} running: {'on' if state else 'off'}")


if __name__ == '__main__':
    main()
