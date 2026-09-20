import math

import numpy as np


class PerformanceCalculator:
    """Calculate indicated engine performance."""

    def __init__(
        self,
        config,
        geometry,
        thermo
    ):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo

    @staticmethod
    def _integrate_pressure_volume(
        pressure,
        volume
    ):
        pressure_average = (
            pressure[:-1]
            + pressure[1:]
        ) / 2.0

        delta_volume = (
            volume[1:]
            - volume[:-1]
        )

        return float(
            np.sum(
                pressure_average
                * delta_volume
            )
        )

    def indicated_work(self, results):
        return (
            self._integrate_pressure_volume(
                results["pressure"],
                results["volume"]
            )
        )

    def compression_work(self, results):
        mask = (
            results["angle"] <= 360.0
        )

        return (
            self._integrate_pressure_volume(
                results["pressure"][mask],
                results["volume"][mask]
            )
        )

    def expansion_work(self, results):
        mask = (
            results["angle"] >= 360.0
        )

        return (
            self._integrate_pressure_volume(
                results["pressure"][mask],
                results["volume"][mask]
            )
        )

    def gross_imep_pa(self, results):
        return (
            self.indicated_work(results)
            / self.geometry.swept_volume
        )

    def gross_indicated_efficiency(
        self,
        results
    ):
        return (
            self.indicated_work(results)
            / self.thermo.fuel_energy_per_cycle()
        )

    def indicated_power_w(self, results):
        work_per_cycle = (
            self.indicated_work(results)
        )

        cycles_per_second = (
            self.config.rpm / 120.0
        )

        return (
            work_per_cycle
            * cycles_per_second
            * self.config.cylinders
        )

    def indicated_torque_nm(self, results):
        power = (
            self.indicated_power_w(results)
        )

        angular_velocity = (
            2.0
            * math.pi
            * self.config.rpm
            / 60.0
        )

        return (
            power / angular_velocity
        )