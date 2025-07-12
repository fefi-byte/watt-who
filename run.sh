#!/bin/sh
# Look for the device configuration next to Home Assistant's configuration.yaml
exec python -m watt_who.main --config /config/devices.yml --options /data/options.json
