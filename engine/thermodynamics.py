class Thermodynamics:
    """
    Handles the basic thermodynamic calculations
    for the EngineLab simulation.
    """

    def __init__(self, config, geometry):
        self.config = config
        self.geometry = geometry

        # Specific gas constant for air
        # Units: J / (kg * K)
        self.R = 287.05

    def trapped_air_mass(self):
        """
        Estimate the mass of air trapped in the cylinder
        at bottom dead center (BDC).

        Uses the ideal gas law:

            PV = mRT

        Rearranged:

            m = PV / RT
        """

        P = self.config.intake_pressure_pa
        T = self.config.intake_temperature_k

        # Cylinder volume at BDC
        V = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        mass = (P * V) / (self.R * T)

        return mass

    def compression_pressure(self, volume):
        """
        Calculate cylinder pressure during ideal
        adiabatic compression.

        Relationship:

            P1 * V1^gamma = P2 * V2^gamma

        Therefore:

            P2 = P1 * (V1 / V2)^gamma
        """

        # Cylinder volume at BDC
        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        # Intake pressure
        P1 = self.config.intake_pressure_pa

        pressure = (
            P1
            * (V1 / volume) ** self.config.gamma
        )

        return pressure

    def compression_temperature(self, volume):
        """
        Calculate cylinder temperature during ideal
        adiabatic compression.

        Relationship:

            T1 * V1^(gamma - 1)
            =
            T2 * V2^(gamma - 1)

        Therefore:

            T2 = T1 * (V1 / V2)^(gamma - 1)
        """

        # Cylinder volume at BDC
        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        # Intake temperature
        T1 = self.config.intake_temperature_k

        temperature = (
            T1
            * (V1 / volume)
            ** (self.config.gamma - 1)
        )

        return temperature