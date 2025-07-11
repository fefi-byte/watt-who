# Watt Who

A simple Home Assistant helper container to track power consumption of devices.
The container can publish sensor data via MQTT so Home Assistant can discover
and display energy usage.

## Usage

1. Define your devices in `devices.yml`.
2. Build the docker image:

```bash
docker build -t watt-who .
```

3. Run it:

```bash
docker run --rm \
  -e MQTT_HOST=<your-mqtt-host> \
  watt-who
```

The example configuration contains one device named `Doerautomat`.

### Home Assistant Integration

If your Home Assistant installation provides an MQTT broker, the container can
publish energy data to it. Set the `MQTT_HOST` environment variable to the host
name of your broker and ensure Home Assistant's MQTT integration is enabled.

Home Assistant will automatically discover sensors for each configured device
via MQTT discovery. The energy usage will appear as sensors named
`<device> Energy`.
