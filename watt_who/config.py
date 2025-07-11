import yaml
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Cycle:
    on: float
    off: float
    power: float

@dataclass
class DeviceConfig:
    name: str
    peak_power: float
    threshold: float
    peak_duration: float
    cycle: Cycle


def load_config(path: str) -> Dict[str, DeviceConfig]:
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}
    devices = {}
    for name, cfg in data.items():
        cycle_cfg = cfg.get('cycle', {})
        devices[name] = DeviceConfig(
            name=name,
            peak_power=float(cfg.get('peak_power', 0)),
            threshold=float(cfg.get('threshold', 1.0)),
            peak_duration=float(cfg.get('peak_duration', 0)),
            cycle=Cycle(
                on=float(cycle_cfg.get('on', 0)),
                off=float(cycle_cfg.get('off', 0)),
                power=float(cycle_cfg.get('power', cfg.get('peak_power', 0))),
            ),
        )
    return devices
