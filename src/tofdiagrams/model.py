import numpy as np

from . import units
from .pulse import Pulse


class Model:
    def __init__(self, choppers, detector, neutrons=1_000_000, pulse=None):
        # # Conversion factors
        # microseconds = 1.0e6
        # v_to_lambda = 3956.0
        # v_to_mev = 437.0
        self.choppers = choppers
        self.detector = detector
        self.pulse = pulse

        if self.pulse is None:
            self.pulse = Pulse(kind="ess")

        self.pulse.make_neutrons(neutrons)

    # ray_trace(choppers=choppers, neutrons=neutrons, pulse_length=pulse_length)

    def ray_trace(self):
        # self.arrival_times = {}
        # self.masks = {}

        sorted_choppers = [
            k
            for k, v in sorted(
                [(name, ch.distance) for name, ch in self.choppers.items()],
                key=lambda item: item[1],
            )
        ]

        initial_mask = np.full_like(self.pulse.birth_times, True, dtype=bool)
        for name in sorted_choppers:
            ch = self.choppers[name]
            t = ch.distance / self.pulse.speeds
            ch._arrival_times = t
            m = np.full_like(t, False, dtype=bool)
            to = ch.open_times
            tc = ch.close_times
            for i in range(len(to)):
                m |= (t > to[i]) & (t < tc[i])
            combined = initial_mask & m
            ch._mask = combined
            initial_mask = combined

        self.detector._arrival_times = self.detector.distance / self.pulse.speeds
        self.detector._mask = initial_mask

    def __repr__(self):
        return (
            f"Model(choppers={self.choppers},\n      detector={self.detector},\n      "
            f"pulse={self.pulse},\n      neutrons={len(self.pulse.birth_times)})"
        )
