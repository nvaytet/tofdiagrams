from .pulse import Pulse


def main(choppers, detector, neutrons=1_000_000, pulse=None):
    # # Conversion factors
    # microseconds = 1.0e6
    # v_to_lambda = 3956.0
    # v_to_mev = 437.0

    if pulse is None:
        pulse = Pulse(kind="ess")

    pulse.make_neutrons(neutrons)

    ray_trace(choppers=choppers, neutrons=neutrons, pulse_length=pulse_length)
