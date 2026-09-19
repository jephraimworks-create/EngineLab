class Thermodynamics:
    """
    Thermodynamic calculations for EngineLab.

    V0.5 adds:
    - Temperature-dependent gas properties
    - Approximate wall heat transfer
    """

    def __init__(self, config, geometry):
        self.config = config
        self.geometry = geometry

        # Specific gas constant for air
        # J / (kg * K)
        self.R = 287.05

    # --------------------------------------------------
    # MASS / FUEL
    # --------------------------------------------------

    def trapped_air_mass(self):
        """
        Estimate trapped air mass at BDC using:

            PV = mRT
        """

        P = self.config.intake_pressure_pa
        T = self.config.intake_temperature_k

        V = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        return (P * V) / (self.R * T)

    def fuel_mass_per_cycle(self):
        air_mass = self.trapped_air_mass()

        return air_mass / self.config.afr

    def fuel_energy_per_cycle(self):
        fuel_mass = self.fuel_mass_per_cycle()

        return (
            fuel_mass
            * self.config.fuel_lhv_j_per_kg
        )

    def released_combustion_energy(self):
        return (
            self.fuel_energy_per_cycle()
            * self.config.combustion_efficiency
        )

    # --------------------------------------------------
    # GAS PROPERTIES
    # --------------------------------------------------

    def cp(self, temperature):
        """
        Approximate temperature-dependent specific
        heat capacity at constant pressure.

        Units:
            J / (kg * K)

        This is intentionally a simple approximation
        for V0.5, not a detailed combustion-gas model.
        """

        T = max(250.0, min(float(temperature), 3500.0))

        cp = (
            1005.0
            + 0.10 * (T - 300.0)
        )

        return cp

    def cv(self, temperature):
        """
        cv = cp - R
        """

        return (
            self.cp(temperature)
            - self.R
        )

    def gamma(self, temperature):
        """
        gamma = cp / cv
        """

        cp = self.cp(temperature)
        cv = self.cv(temperature)

        return cp / cv

    # --------------------------------------------------
    # ORIGINAL COMPRESSION HELPERS
    # --------------------------------------------------

    def compression_pressure(self, volume):
        """
        Approximate ideal compression helper.

        Retained primarily for comparison with the
        earlier V0.2 model.
        """

        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        P1 = self.config.intake_pressure_pa

        gamma = self.gamma(
            self.config.intake_temperature_k
        )

        return (
            P1
            * (V1 / volume) ** gamma
        )

    def compression_temperature(self, volume):
        V1 = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        T1 = self.config.intake_temperature_k

        gamma = self.gamma(T1)

        return (
            T1
            * (V1 / volume) ** (gamma - 1.0)
        )

    # --------------------------------------------------
    # HEAT TRANSFER
    # --------------------------------------------------

    def wall_heat_transfer_coefficient(
        self,
        pressure,
        temperature,
        piston_speed
    ):
        """
        Simplified empirical heat-transfer coefficient.

        Returns:
            W / (m^2 * K)

        This is a deliberately simplified engineering
        approximation for V0.5.
        """

        pressure_bar = pressure / 100000.0

        h = (
            120.0
            + 18.0 * pressure_bar
            + 35.0 * abs(piston_speed)
        )

        return max(h, 50.0)

    def wall_heat_loss(
        self,
        pressure,
        gas_temperature,
        wall_temperature,
        surface_area,
        piston_speed,
        dt
    ):
        """
        Calculate heat transferred from cylinder gas
        to the walls during one timestep.

            Q = h A (Tgas - Twall) dt

        Returns joules.
        """

        if gas_temperature <= wall_temperature:
            return 0.0

        h = self.wall_heat_transfer_coefficient(
            pressure,
            gas_temperature,
            piston_speed
        )

        heat_loss = (
            h
            * surface_area
            * (gas_temperature - wall_temperature)
            * dt
        )

        return max(heat_loss, 0.0)