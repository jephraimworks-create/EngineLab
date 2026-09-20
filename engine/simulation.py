import numpy as np


class EngineSimulation:
    """Closed-cycle primary-cylinder simulation."""

    def __init__(
        self,
        config,
        geometry,
        thermo,
        combustion
    ):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo
        self.combustion = combustion

    def simulate_closed_cycle(self):
        step_deg = (
            self.config.crank_step_deg
        )

        angles = np.arange(
            180.0,
            540.0 + step_deg,
            step_deg
        )

        volumes = np.array([
            self.geometry.cylinder_volume(angle)
            for angle in angles
        ])

        pressures = np.zeros_like(angles)
        temperatures = np.zeros_like(angles)

        burned_fraction = np.zeros_like(angles)
        heat_release = np.zeros_like(angles)
        wall_heat_loss = np.zeros_like(angles)
        boundary_work = np.zeros_like(angles)

        gas_mass = (
            self.thermo.trapped_air_mass()
        )

        gas_constant = (
            self.thermo.R
        )

        temperatures[0] = (
            self.config.intake_temperature_k
        )

        pressures[0] = (
            self.config.intake_pressure_pa
        )

        burned_fraction[0] = (
            self.combustion.burned_fraction(
                angles[0]
            )
        )

        total_combustion_energy = (
            self.thermo.released_combustion_energy()
        )

        degrees_per_second = (
            self.config.rpm
            * 360.0
            / 60.0
        )

        dt = (
            step_deg
            / degrees_per_second
        )

        for i in range(1, len(angles)):
            angle_old = angles[i - 1]
            angle_new = angles[i]

            volume_old = volumes[i - 1]
            volume_new = volumes[i]

            pressure_old = pressures[i - 1]
            temperature_old = temperatures[i - 1]

            # ------------------------------------------
            # COMBUSTION
            # ------------------------------------------

            xb_old = (
                self.combustion.burned_fraction(
                    angle_old
                )
            )

            xb_new = (
                self.combustion.burned_fraction(
                    angle_new
                )
            )

            burned_fraction[i] = xb_new

            delta_xb = (
                xb_new - xb_old
            )

            combustion_heat = (
                total_combustion_energy
                * delta_xb
            )

            heat_release[i] = (
                combustion_heat
            )

            # ------------------------------------------
            # WALL HEAT TRANSFER
            # ------------------------------------------

            surface_area = (
                self.geometry.chamber_surface_area(
                    angle_old
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

            wall_heat_loss[i] = (
                wall_heat
            )

            # ------------------------------------------
            # BOUNDARY WORK
            # ------------------------------------------

            delta_volume = (
                volume_new - volume_old
            )

            work = (
                pressure_old
                * delta_volume
            )

            boundary_work[i] = (
                work
            )

            # ------------------------------------------
            # FIRST LAW
            # ------------------------------------------

            cv = (
                self.thermo.cv(
                    temperature_old
                )
            )

            delta_internal_energy = (
                combustion_heat
                - wall_heat
                - work
            )

            delta_temperature = (
                delta_internal_energy
                / (gas_mass * cv)
            )

            temperature_new = (
                temperature_old
                + delta_temperature
            )

            temperature_new = max(
                temperature_new,
                200.0
            )

            pressure_new = (
                gas_mass
                * gas_constant
                * temperature_new
                / volume_new
            )

            temperatures[i] = (
                temperature_new
            )

            pressures[i] = (
                pressure_new
            )

        return {
            "angle": angles,
            "volume": volumes,
            "pressure": pressures,
            "temperature": temperatures,
            "burned_fraction": burned_fraction,
            "heat_release": heat_release,
            "wall_heat_loss": wall_heat_loss,
            "boundary_work": boundary_work,
            "gas_mass": gas_mass,
        }