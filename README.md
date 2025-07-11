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

### Installing as a Home Assistant Add-on

To use this container directly in Home Assistant, add this repository to the
"Add-on store" as a custom source:

1. Open **Settings -> Add-ons -> Add-on Store**.
2. Use the menu in the upper right to select **Repositories** and add the URL of
   this repository.
3. After the repository is added, the "Watt Who" add-on becomes available for
   installation. Configure the MQTT options (host, port, username and password)
   in the add-on settings. To update sensor states via the Home Assistant REST
   API, enable the option `homeassistant_api: true`. The add-on requires the
   **Home Assistant Core API** permission for this feature. Start the add-on
   after saving the settings.

## License

This project is licensed under the [MIT License](LICENSE).
