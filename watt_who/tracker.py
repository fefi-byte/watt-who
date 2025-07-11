import time
from typing import Dict
from dataclasses import dataclass, field

from .config import DeviceConfig

@dataclass
class DeviceState:
    config: DeviceConfig
    energy_wh: float = 0.0
    _active_for: float = 0.0

    @property
    def running(self) -> bool:
        return self._active_for >= self.config.peak_duration

    def update(self, power: float, delta: float):
        # If power close to peak, count as running
        expected = self.config.peak_power
        if expected == 0:
            return
        threshold = expected * self.config.threshold
        if power >= threshold:
            self.energy_wh += power * delta / 3600.0
            self._active_for += delta
        else:
            self._active_for = 0.0

class PowerTracker:
    def __init__(self, configs: Dict[str, DeviceConfig]):
        self.devices: Dict[str, DeviceState] = {
            name: DeviceState(cfg) for name, cfg in configs.items()
        }
        self.last_time = time.time()

    def update_power(self, power: float):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now
        for state in self.devices.values():
            state.update(power, delta)

    def get_energy_kwh(self) -> Dict[str, float]:
        return {name: state.energy_wh / 1000.0 for name, state in self.devices.items()}

    def get_running_states(self) -> Dict[str, bool]:
        return {name: state.running for name, state in self.devices.items()}
