# Watt Who

A simple Home Assistant helper container to track power consumption of devices.
Sensor states are pushed directly to Home Assistant via the REST API.

## Usage

1. Define your devices in `/config/devices.yml` alongside your `configuration.yaml`.
2. Build the docker image:

```bash
docker build -t watt-who .
```

3. Run it:

```bash
docker run --rm -e SUPERVISOR_TOKEN=<token> watt-who
```

Use the `--debug` flag or set the environment variable `DEBUG=1` to enable
verbose debug output.

The example configuration contains one device named `Doerautomat`.

## Configuration



### Home Assistant Integration

The container requires the `SUPERVISOR_TOKEN` environment variable so it can
update entity states via the Home Assistant REST API. Each device defined in
`devices.yml` will create:

* `sensor.watt_who_<device>_energy` – the energy meter in kWh
* `binary_sensor.watt_who_<device>_running` – shows if the device is running

### Installing as a Home Assistant Add-on

To use this container directly in Home Assistant, add this repository to the
"Add-on store" as a custom source:

1. Open **Settings -> Add-ons -> Add-on Store**.
2. Use the menu in the upper right to select **Repositories** and add the URL of
   this repository.
3. After the repository is added, the "Watt Who" add-on becomes available for
   installation. Ensure the add-on has the **Home Assistant Core API**
   permission so it can update entity states. Start the add-on after saving the
   settings.

## License

This project is licensed under the [MIT License](LICENSE).
