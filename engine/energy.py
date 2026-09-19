import numpy as np


class EnergyAnalysis:
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
        # Total chemical energy entering through fuel
        fuel_energy = (
            self.thermo.fuel_energy_per_cycle()
        )

        # Energy actually released by our
        # combustion model
        released_energy = (
            self.thermo.released_combustion_energy()
        )

        # Net work transferred to the piston
        indicated_work = (
            self.performance.indicated_work(
                results
            )
        )

        # Sum heat transferred into cylinder walls
        wall_loss = np.sum(
            results["wall_heat_loss"]
        )

        # Energy not released because combustion
        # efficiency is less than 100%
        unreleased_fuel_energy = (
            fuel_energy
            - released_energy
        )

        # Energy that is not yet explicitly accounted for.
        #
        # IMPORTANT:
        # We are NOT calling this exhaust energy yet.
        #
        # It currently includes:
        # - energy remaining in the cylinder gas
        # - eventual exhaust energy
        # - simplifications in the model
        # - numerical/model error
        remaining_energy = (
            fuel_energy
            - indicated_work
            - wall_loss
            - unreleased_fuel_energy
        )

        return {
            "fuel_energy": fuel_energy,
            "released_energy": released_energy,
            "indicated_work": indicated_work,
            "wall_loss": wall_loss,
            "unreleased_energy": unreleased_fuel_energy,
            "remaining_energy": remaining_energy,
        }