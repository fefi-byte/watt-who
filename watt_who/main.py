import argparse
import random
import time

from .config import load_config
from .tracker import PowerTracker


def main():
    parser = argparse.ArgumentParser(description="Simple power tracker")
    parser.add_argument('--config', default='devices.yml', help='Path to device config')
    parser.add_argument('--interval', type=float, default=1.0, help='Sampling interval in seconds')
    args = parser.parse_args()

    devices = load_config(args.config)
    tracker = PowerTracker(devices)

    try:
        while True:
            # In a real application, replace this with actual sensor reading
            current_power = random.uniform(0, 1000)
            tracker.update_power(current_power)
            energy = tracker.get_energy_kwh()
            print('\r' + ', '.join(f"{name}: {val:.4f} kWh" for name, val in energy.items()), end='')
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print()  # newline
        for name, val in tracker.get_energy_kwh().items():
            print(f"{name}: {val:.4f} kWh")


if __name__ == '__main__':
    main()
