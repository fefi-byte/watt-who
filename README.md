# Watt Who

A simple Home Assistant helper container to track power consumption of devices.

## Usage

1. Define your devices in `devices.yml`.
2. Build the docker image:

```bash
docker build -t watt-who .
```

3. Run it:

```bash
docker run --rm watt-who
```

The example configuration contains one device named `Doerautomat`.
