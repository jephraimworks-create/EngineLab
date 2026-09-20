class ExpansionSweep:
    """Run secondary expansion across candidate ratios."""

    def __init__(
        self,
        config,
        geometry,
        thermo,
        secondary_expansion
    ):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo
        self.secondary = secondary_expansion

    def run(
        self,
        primary_results,
        primary_work,
        fuel_energy
    ):
        initial_pressure = float(
            primary_results["pressure"][-1]
        )

        initial_temperature = float(
            primary_results["temperature"][-1]
        )

        initial_volume = float(
            primary_results["volume"][-1]
        )

        gas_mass = float(
            primary_results["gas_mass"]
        )

        primary_ratio = (
            self.config.compression_ratio
        )

        # Exploratory assumption:
        # secondary expansion occupies 180 crank degrees.
        expansion_duration_s = (
            30.0
            / self.config.rpm
        )

        sweep_results = []

        for ratio in (
            self.config.secondary_expansion_ratios
        ):
            volume_multiplier = (
                ratio / primary_ratio
            )

            target_volume = (
                initial_volume
                * volume_multiplier
            )

            if ratio <= primary_ratio:
                ideal_work = 0.0
                heat_loss_work = 0.0
                secondary_wall_heat = 0.0

                ideal_final_pressure = (
                    initial_pressure
                )

                heat_loss_final_pressure = (
                    initial_pressure
                )

                ideal_final_temperature = (
                    initial_temperature
                )

                heat_loss_final_temperature = (
                    initial_temperature
                )

                ideal_balance_error = 0.0
                heat_loss_balance_error = 0.0

            else:
                ideal = (
                    self.secondary.simulate(
                        initial_pressure=(
                            initial_pressure
                        ),
                        initial_temperature=(
                            initial_temperature
                        ),
                        initial_volume=(
                            initial_volume
                        ),
                        target_volume=(
                            target_volume
                        ),
                        gas_mass=gas_mass,
                        expansion_duration_s=(
                            expansion_duration_s
                        ),
                        include_heat_loss=False
                    )
                )

                heat_loss = (
                    self.secondary.simulate(
                        initial_pressure=(
                            initial_pressure
                        ),
                        initial_temperature=(
                            initial_temperature
                        ),
                        initial_volume=(
                            initial_volume
                        ),
                        target_volume=(
                            target_volume
                        ),
                        gas_mass=gas_mass,
                        expansion_duration_s=(
                            expansion_duration_s
                        ),
                        include_heat_loss=True
                    )
                )

                ideal_work = (
                    ideal["work"]
                )

                heat_loss_work = (
                    heat_loss["work"]
                )

                secondary_wall_heat = (
                    heat_loss["wall_heat_loss"]
                )

                ideal_final_pressure = (
                    ideal["pressure"][-1]
                )

                heat_loss_final_pressure = (
                    heat_loss["pressure"][-1]
                )

                ideal_final_temperature = (
                    ideal["temperature"][-1]
                )

                heat_loss_final_temperature = (
                    heat_loss["temperature"][-1]
                )

                ideal_balance_error = (
                    ideal["energy_balance_error"]
                )

                heat_loss_balance_error = (
                    heat_loss["energy_balance_error"]
                )

            ideal_total_work = (
                primary_work
                + ideal_work
            )

            heat_loss_total_work = (
                primary_work
                + heat_loss_work
            )

            ideal_efficiency = (
                ideal_total_work
                / fuel_energy
            )

            heat_loss_efficiency = (
                heat_loss_total_work
                / fuel_energy
            )

            sweep_results.append({
                "ratio": ratio,
                "target_volume": target_volume,

                "ideal_extra_work": ideal_work,
                "heat_loss_extra_work": (
                    heat_loss_work
                ),

                "ideal_total_work": (
                    ideal_total_work
                ),
                "heat_loss_total_work": (
                    heat_loss_total_work
                ),

                "ideal_efficiency": (
                    ideal_efficiency
                ),
                "heat_loss_efficiency": (
                    heat_loss_efficiency
                ),

                "ideal_final_pressure": (
                    ideal_final_pressure
                ),
                "heat_loss_final_pressure": (
                    heat_loss_final_pressure
                ),

                "ideal_final_temperature": (
                    ideal_final_temperature
                ),
                "heat_loss_final_temperature": (
                    heat_loss_final_temperature
                ),

                "secondary_wall_heat": (
                    secondary_wall_heat
                ),

                "ideal_balance_error": (
                    ideal_balance_error
                ),
                "heat_loss_balance_error": (
                    heat_loss_balance_error
                ),
            })

        return sweep_results