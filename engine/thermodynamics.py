class Thermodynamics:
    """
    Basic thermodynamic calculations for EngineLab.
    """

    def __init__(self, config, geometry):
        self.config = config
        self.geometry = geometry

        # Specific gas constant for air
        # J / (kg * K)
        self.R = 287.05

    def trapped_air_mass(self):
        """
        Estimate the mass of air trapped in the cylinder
        at bottom dead center using the ideal gas law.

        PV = mRT
        """

        P = self.config.intake_pressure_pa
        T = self.config.intake_temperature_k

        V = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        mass = (P * V) / (self.R * T)

        return mass

    def compression_pressure(self, volume):
        """
        Calculate pressure during ideal adiabatic compression.
        """

        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        P1 = self.config.intake_pressure_pa

        pressure = (
            P1
            * (V1 / volume) ** self.config.gamma
        )

        return pressure

    def compression_temperature(self, volume):
        """
        Calculate temperature during ideal adiabatic compression.
        """

        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        T1 = self.config.intake_temperature_k

        temperature = (
            T1
            * (V1 / volume)
            ** (self.config.gamma - 1)
        )

        return temperature

    def fuel_mass_per_cycle(self):
        """
        Calculate fuel mass from trapped air mass
        and air/fuel ratio.
        """

        air_mass = self.trapped_air_mass()

        fuel_mass = air_mass / self.config.afr

        return fuel_mass

    def fuel_energy_per_cycle(self):
        """
        Calculate chemical energy contained in the
        fuel for one combustion event.
        """

        fuel_mass = self.fuel_mass_per_cycle()

        fuel_energy = (
            fuel_mass
            * self.config.fuel_lhv_j_per_kg
        )

        return fuel_energy

    def released_combustion_energy(self):
        """
        Estimate how much fuel energy is actually
        released during combustion.
        """

        released_energy = (
            self.fuel_energy_per_cycle()
            * self.config.combustion_efficiency
        )

        return released_energy