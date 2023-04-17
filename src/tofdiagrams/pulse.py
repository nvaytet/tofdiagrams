import numpy as np

from .units import microseconds


class Pulse:
    def __init__(self, stop: float = 1.0, start: float = 0.0, kind="ess"):
        self.start = start
        self.stop = stop

        if self.kind == "ess":
            self.stop = self.start + 2860.0 * microseconds

        self.birth_times = None
        self.wavelengths = None

        self.wavelength_min = 1.0  # Angstrom
        self.wavelength_max = 10.0  # Angstrom

    @property
    def duration(self):
        return self.stop - self.start

    def make_neutrons(self, n):
        self.birth_times = np.random.uniform(self.start, self.stop, n)
        self.wavelengths = np.random.uniform(
            self.wavelength_min, self.wavelength_max, n
        )
