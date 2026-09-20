import math


class CombustionModel:
    """Single-Wiebe combustion model."""

    def __init__(self, config):
        self.config = config

    def start_angle(self):
        """Start of combustion in absolute crank angle."""

        return (
            360.0
            - self.config.combustion_start_btdc_deg
        )

    def nominal_end_angle(self):
        """
        Nominal combustion-duration endpoint.

        The Wiebe function approaches 100%
        asymptotically and is not forcibly truncated here.
        """

        return (
            self.start_angle()
            + self.config.combustion_duration_deg
        )

    def burned_fraction(self, crank_angle_deg):
        """
        Calculate mass fraction burned using:

            xb = 1 - exp(-a * x^(m + 1))
        """

        start = self.start_angle()

        if crank_angle_deg <= start:
            return 0.0

        progress = (
            crank_angle_deg - start
        ) / self.config.combustion_duration_deg

        burned_fraction = (
            1.0
            - math.exp(
                -self.config.wiebe_a
                * progress ** (
                    self.config.wiebe_m + 1.0
                )
            )
        )

        return min(
            max(burned_fraction, 0.0),
            1.0
        )