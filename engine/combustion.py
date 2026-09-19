import numpy as np


class CombustionModel:

    def __init__(self, config):
        self.config = config

    def start_angle(self):
        """
        Convert ignition timing in degrees BTDC
        into our 0-720 degree crank-angle system.
        """

        return 360.0 - self.config.ignition_timing_deg

    def end_angle(self):
        """
        End of the simplified combustion event.
        """

        return (
            self.start_angle()
            + self.config.combustion_duration_deg
        )

    def burned_fraction(self, crank_angle_deg):
        """
        Approximate the fraction of fuel burned at
        a particular crank angle.

        Uses a smooth half-cosine curve.

        Returns a value from 0.0 to 1.0.
        """

        start = self.start_angle()
        end = self.end_angle()

        if crank_angle_deg <= start:
            return 0.0

        if crank_angle_deg >= end:
            return 1.0

        progress = (
            (crank_angle_deg - start)
            / (end - start)
        )

        fraction = (
            0.5
            - 0.5 * np.cos(np.pi * progress)
        )

        return fraction