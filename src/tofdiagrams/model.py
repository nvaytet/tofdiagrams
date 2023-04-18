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

    def __repr__(self):
        return (
            f"Model(choppers={self.choppers},\n      detector={self.detector},\n      "
            f"pulse={self.pulse},\n      neutrons={len(self.pulse.birth_times)})"
        )
