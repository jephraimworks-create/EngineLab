import numpy as np


class EnergyAnalysis:
    """Primary-cylinder energy accounting."""

    def __init__(
        self,
        config,
        geometry,
        thermo,
        performance
    ):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo
        self.performance = performance

    def analyze(self, results):
        fuel_energy = (
            self.thermo.fuel_energy_per_cycle()
        )

        available_combustion_energy = (
            self.thermo.released_combustion_energy()
        )

        actual_heat_release = float(
            np.sum(
                results["heat_release"]
            )
        )

        indicated_work = (
            self.performance.indicated_work(
                results
            )
        )

        wall_heat_loss = float(
            np.sum(
                results["wall_heat_loss"]
            )
        )

        combustion_loss = (
            fuel_energy
            - available_combustion_energy
        )

        incomplete_wiebe_release = (
            available_combustion_energy
            - actual_heat_release
        )

        remaining_energy = (
            fuel_energy
            - indicated_work
            - wall_heat_loss
            - combustion_loss
            - incomplete_wiebe_release
        )

        end_pressure = float(
            results["pressure"][-1]
        )

        end_temperature = float(
            results["temperature"][-1]
        )

        end_volume = float(
            results["volume"][-1]
        )

        return {
            "fuel_energy": fuel_energy,
            "available_combustion_energy": (
                available_combustion_energy
            ),
            "actual_heat_release": (
                actual_heat_release
            ),
            "indicated_work": indicated_work,
            "wall_heat_loss": wall_heat_loss,
            "combustion_loss": combustion_loss,
            "incomplete_wiebe_release": (
                incomplete_wiebe_release
            ),
            "remaining_energy": (
                remaining_energy
            ),
            "end_pressure_pa": end_pressure,
            "end_temperature_k": end_temperature,
            "end_volume_m3": end_volume,
            "end_cp": self.thermo.cp(
                end_temperature
            ),
            "end_cv": self.thermo.cv(
                end_temperature
            ),
            "end_gamma": self.thermo.gamma(
                end_temperature
            ),
        }