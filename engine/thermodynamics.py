import math


class Thermodynamics:
    """
    Thermodynamic property and heat-transfer calculations.

    Uses:
    - ideal-gas equation of state
    - temperature-dependent air specific heats
    - Hohenberg-style in-cylinder heat transfer
    """

    def __init__(self, config, geometry):
        self.config = config
        self.geometry = geometry

        # Specific gas constant for air
        self.R = 287.05

        # Calorically perfect reference value
        self.gamma_reference = 1.4

        # Approximate vibrational temperature for air
        self.theta_v = 5500.0 * (5.0 / 9.0)

    # --------------------------------------------------
    # MASS AND FUEL
    # --------------------------------------------------

    def trapped_air_mass(self):
        """Calculate trapped air mass at BDC."""

        pressure = self.config.intake_pressure_pa
        temperature = self.config.intake_temperature_k

        volume = (
            self.geometry.swept_volume
            + self.geometry.clearance_volume
        )

        return (
            pressure * volume
            / (self.R * temperature)
        )

    def fuel_mass_per_cycle(self):
        return (
            self.trapped_air_mass()
            / self.config.afr
        )

    def fuel_energy_per_cycle(self):
        return (
            self.fuel_mass_per_cycle()
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

    def _vibrational_term(self, temperature):
        temperature = max(
            float(temperature),
            200.0
        )

        x = self.theta_v / temperature

        exp_x = math.exp(x)

        denominator = (
            exp_x - 1.0
        ) ** 2

        return (
            x**2
            * exp_x
            / denominator
        )

    def cp(self, temperature):
        """Temperature-dependent cp in J/(kg K)."""

        gamma = self.gamma_reference

        cp_reference = (
            gamma
            * self.R
            / (gamma - 1.0)
        )

        correction = (
            1.0
            + (
                (gamma - 1.0)
                / gamma
            )
            * self._vibrational_term(
                temperature
            )
        )

        return (
            cp_reference
            * correction
        )

    def cv(self, temperature):
        """Temperature-dependent cv in J/(kg K)."""

        return (
            self.cp(temperature)
            - self.R
        )

    def gamma(self, temperature):
        """Temperature-dependent heat-capacity ratio."""

        cp = self.cp(temperature)
        cv = self.cv(temperature)

        return cp / cv

    # --------------------------------------------------
    # INTERNAL ENERGY
    # --------------------------------------------------

    def specific_internal_energy(self, temperature):
        """
        Numerically integrate cv(T) from 200 K to T.

        This is primarily used for energy accounting.
        """

        temperature = max(
            float(temperature),
            200.0
        )

        if temperature == 200.0:
            return 0.0

        steps = 200

        delta_t = (
            temperature - 200.0
        ) / steps

        energy = 0.0

        for i in range(steps):
            t1 = (
                200.0
                + i * delta_t
            )

            t2 = (
                t1 + delta_t
            )

            cv_average = (
                self.cv(t1)
                + self.cv(t2)
            ) / 2.0

            energy += (
                cv_average
                * delta_t
            )

        return energy

    # --------------------------------------------------
    # PISTON SPEED
    # --------------------------------------------------

    def mean_piston_speed(self):
        """Mean piston speed in m/s."""

        return (
            2.0
            * self.geometry.stroke
            * self.config.rpm
            / 60.0
        )

    # --------------------------------------------------
    # HEAT TRANSFER
    # --------------------------------------------------

    def hohenberg_heat_transfer_coefficient(
        self,
        pressure,
        temperature,
        volume
    ):
        """
        Approximate Hohenberg heat-transfer correlation.

        Returns:
            W/(m^2 K)
        """

        volume = max(
            float(volume),
            1e-12
        )

        temperature = max(
            float(temperature),
            200.0
        )

        pressure_bar = max(
            float(pressure) / 100000.0,
            0.01
        )

        mean_speed = (
            self.mean_piston_speed()
        )

        return (
            130.0
            * volume ** (-0.06)
            * pressure_bar**0.8
            * temperature ** (-0.4)
            * (mean_speed + 1.4) ** 0.8
        )

    def wall_heat_loss(
        self,
        pressure,
        gas_temperature,
        wall_temperature,
        surface_area,
        volume,
        dt
    ):
        """
        Convective wall heat loss for one time step.

        Positive result means heat leaves the gas.
        """

        if gas_temperature <= wall_temperature:
            return 0.0

        h = (
            self.hohenberg_heat_transfer_coefficient(
                pressure=pressure,
                temperature=gas_temperature,
                volume=volume
            )
        )

        heat_loss = (
            h
            * surface_area
            * (
                gas_temperature
                - wall_temperature
            )
            * dt
        )

        return max(
            heat_loss,
            0.0
        )