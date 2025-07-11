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

### Optional Environment Variables

The container uses the following variables to configure the MQTT connection:

- `MQTT_PORT` – Port of the MQTT broker (default `1883`).
- `MQTT_USERNAME` – Username for broker authentication.
- `MQTT_PASSWORD` – Password for broker authentication.
- `MQTT_DISABLE` – Set to `1` to disable MQTT entirely.

Example with all options:

```bash
docker run --rm \
  -e MQTT_HOST=192.168.1.10 \
  -e MQTT_PORT=1884 \
  -e MQTT_USERNAME=myuser \
  -e MQTT_PASSWORD=mypass \
  watt-who
```

To run without MQTT, pass `MQTT_DISABLE=1`:

```bash
docker run --rm -e MQTT_DISABLE=1 watt-who
```

### Home Assistant Integration

If your Home Assistant installation provides an MQTT broker, the container can
publish energy data to it. Set the `MQTT_HOST` environment variable to the host
name of your broker and ensure Home Assistant's MQTT integration is enabled.

Home Assistant will automatically discover sensors for each configured device
via MQTT discovery. The energy usage will appear as sensors named
`<device> Energy`.

### Installing as a Home Assistant Add-on

To use this container directly in Home Assistant, add this repository to the
"Add-on store" as a custom source:

1. Open **Settings -> Add-ons -> Add-on Store**.
2. Use the menu in the upper right to select **Repositories** and add the URL of
   this repository.
3. After the repository is added, the "Watt Who" add-on becomes available for
   installation. Configure the MQTT options (host, port, username and password)
   in the add-on settings and start it.

Example configuration:

```yaml
mqtt_host: 192.168.1.10
mqtt_port: 1884
mqtt_username: myuser
mqtt_password: mypass
```

You can disable MQTT in the add-on by defining the `MQTT_DISABLE` environment
variable with the value `1` in the add-on options.
