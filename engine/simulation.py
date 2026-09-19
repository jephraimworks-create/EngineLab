import numpy as np


class EngineSimulation:

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

        # Compression BDC -> TDC -> expansion BDC
        angles = np.arange(
            180.0,
            540.0 + 0.5,
            0.5
        )

        volumes = np.array([
            self.geometry.cylinder_volume(angle)
            for angle in angles
        ])

        pressures = np.zeros_like(angles)
        temperatures = np.zeros_like(angles)
        burned_fraction = np.zeros_like(angles)

        # Trapped mixture mass
        air_mass = self.thermo.trapped_air_mass()
        fuel_mass = self.thermo.fuel_mass_per_cycle()

        total_mass = air_mass + fuel_mass

        # Gas properties
        R = self.thermo.R
        gamma = self.config.gamma

        cv = R / (gamma - 1.0)

        # Initial conditions at BDC
        temperatures[0] = (
            self.config.intake_temperature_k
        )

        pressures[0] = (
            self.config.intake_pressure_pa
        )

        total_combustion_energy = (
            self.thermo.released_combustion_energy()
        )

        for i in range(1, len(angles)):

            V_old = volumes[i - 1]
            V_new = volumes[i]

            T_old = temperatures[i - 1]
            P_old = pressures[i - 1]

            # Change in burned fraction
            xb_old = self.combustion.burned_fraction(
                angles[i - 1]
            )

            xb_new = self.combustion.burned_fraction(
                angles[i]
            )

            burned_fraction[i] = xb_new

            delta_xb = xb_new - xb_old

            # Heat released during this crank-angle step
            dQ = (
                total_combustion_energy
                * delta_xb
            )

            # Approximate boundary work during this step
            dV = V_new - V_old

            dW = P_old * dV

            # First law:
            #
            # dU = dQ - dW
            #
            # and:
            #
            # U = m * cv * T

            dT = (
                (dQ - dW)
                / (total_mass * cv)
            )

            T_new = T_old + dT

            # Pressure from ideal gas law
            P_new = (
                total_mass
                * R
                * T_new
                / V_new
            )

            temperatures[i] = T_new
            pressures[i] = P_new

        return {
            "angle": angles,
            "volume": volumes,
            "pressure": pressures,
            "temperature": temperatures,
            "burned_fraction": burned_fraction,
        }