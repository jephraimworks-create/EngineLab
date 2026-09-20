import math

import numpy as np


class SecondaryExpansion:
    """
    Thermodynamic secondary-expansion model.

    This model tests additional expansion after the
    primary cylinder reaches BDC.

    It is not yet tied to a specific mechanical
    secondary-expander architecture.
    """

    def __init__(
        self,
        config,
        geometry,
        thermo
    ):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo

    def _secondary_surface_area(
        self,
        volume
    ):
        """
        Approximate secondary chamber as a cylinder
        using the primary-engine bore.

        This remains an exploratory assumption until
        an actual secondary-expander geometry is chosen.
        """

        bore = self.geometry.bore

        piston_area = (
            math.pi
            * bore**2
            / 4.0
        )

        chamber_length = (
            volume / piston_area
        )

        end_areas = (
            2.0 * piston_area
        )

        liner_area = (
            math.pi
            * bore
            * chamber_length
        )

        return (
            end_areas
            + liner_area
        )

    def _solve_step(
        self,
        pressure_old,
        temperature_old,
        volume_old,
        volume_new,
        gas_mass,
        dt,
        include_heat_loss
    ):
        """
        Solve one secondary-expansion step.

        Uses predictor-corrector iteration so that
        pressure-volume work is consistent with the
        calculated end state.
        """

        delta_volume = (
            volume_new - volume_old
        )

        wall_heat = 0.0

        if include_heat_loss:
            surface_area = (
                self._secondary_surface_area(
                    volume_old
                )
            )

            wall_heat = (
                self.thermo.wall_heat_loss(
                    pressure=pressure_old,
                    gas_temperature=temperature_old,
                    wall_temperature=(
                        self.config.wall_temperature_k
                    ),
                    surface_area=surface_area,
                    volume=volume_old,
                    dt=dt
                )
            )

        cv = (
            self.thermo.cv(
                temperature_old
            )
        )

        # Initial predictor
        work = (
            pressure_old
            * delta_volume
        )

        temperature_new = (
            temperature_old
            + (
                -work
                - wall_heat
            )
            / (gas_mass * cv)
        )

        temperature_new = max(
            temperature_new,
            200.0
        )

        # Predictor-corrector iterations
        for _ in range(4):
            pressure_new = (
                gas_mass
                * self.thermo.R
                * temperature_new
                / volume_new
            )

            work = (
                0.5
                * (
                    pressure_old
                    + pressure_new
                )
                * delta_volume
            )

            average_temperature = (
                temperature_old
                + temperature_new
            ) / 2.0

            cv_average = (
                self.thermo.cv(
                    average_temperature
                )
            )

            temperature_new = (
                temperature_old
                + (
                    -work
                    - wall_heat
                )
                / (
                    gas_mass
                    * cv_average
                )
            )

            temperature_new = max(
                temperature_new,
                200.0
            )

        pressure_new = (
            gas_mass
            * self.thermo.R
            * temperature_new
            / volume_new
        )

        work = (
            0.5
            * (
                pressure_old
                + pressure_new
            )
            * delta_volume
        )

        return {
            "pressure": pressure_new,
            "temperature": temperature_new,
            "work": work,
            "wall_heat": wall_heat,
        }

    def simulate(
        self,
        initial_pressure,
        initial_temperature,
        initial_volume,
        target_volume,
        gas_mass,
        expansion_duration_s,
        include_heat_loss=True,
        steps=None
    ):
        """Run a complete secondary expansion."""

        if steps is None:
            steps = (
                self.config.secondary_steps
            )

        if target_volume < initial_volume:
            raise ValueError(
                "Target secondary volume cannot "
                "be smaller than initial volume."
            )

        volumes = np.linspace(
            initial_volume,
            target_volume,
            steps
        )

        pressures = np.zeros(steps)
        temperatures = np.zeros(steps)

        pressures[0] = initial_pressure
        temperatures[0] = initial_temperature

        total_work = 0.0
        total_wall_heat = 0.0

        if steps > 1:
            dt = (
                expansion_duration_s
                / (steps - 1)
            )
        else:
            dt = 0.0

        for i in range(1, steps):
            step_result = (
                self._solve_step(
                    pressure_old=pressures[i - 1],
                    temperature_old=temperatures[i - 1],
                    volume_old=volumes[i - 1],
                    volume_new=volumes[i],
                    gas_mass=gas_mass,
                    dt=dt,
                    include_heat_loss=(
                        include_heat_loss
                    )
                )
            )

            pressures[i] = (
                step_result["pressure"]
            )

            temperatures[i] = (
                step_result["temperature"]
            )

            total_work += (
                step_result["work"]
            )

            total_wall_heat += (
                step_result["wall_heat"]
            )

        initial_internal_energy = (
            gas_mass
            * self.thermo.specific_internal_energy(
                initial_temperature
            )
        )

        final_internal_energy = (
            gas_mass
            * self.thermo.specific_internal_energy(
                temperatures[-1]
            )
        )

        internal_energy_drop = (
            initial_internal_energy
            - final_internal_energy
        )

        energy_balance_error = (
            internal_energy_drop
            - total_work
            - total_wall_heat
        )

        return {
            "volume": volumes,
            "pressure": pressures,
            "temperature": temperatures,
            "work": total_work,
            "wall_heat_loss": total_wall_heat,
            "initial_internal_energy": (
                initial_internal_energy
            ),
            "final_internal_energy": (
                final_internal_energy
            ),
            "internal_energy_drop": (
                internal_energy_drop
            ),
            "energy_balance_error": (
                energy_balance_error
            ),
        }