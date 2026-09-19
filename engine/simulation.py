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
        # Simulation resolution in crankshaft degrees
        step_deg = 0.5

        # Closed portion of the four-stroke cycle:
        # 180° = BDC before compression
        # 360° = TDC
        # 540° = BDC after expansion
        angles = np.arange(
            180.0,
            540.0 + step_deg,
            step_deg
        )

        # Calculate cylinder volume at every crank angle
        volumes = np.array([
            self.geometry.cylinder_volume(angle)
            for angle in angles
        ])

        # Arrays used to store simulation results
        pressures = np.zeros_like(angles)
        temperatures = np.zeros_like(angles)
        burned_fraction = np.zeros_like(angles)
        heat_release = np.zeros_like(angles)
        wall_heat_loss = np.zeros_like(angles)

        # ---------------------------------------------
        # MASS
        # ---------------------------------------------

        air_mass = self.thermo.trapped_air_mass()

        fuel_mass = self.thermo.fuel_mass_per_cycle()

        total_mass = air_mass + fuel_mass

        R = self.thermo.R

        # ---------------------------------------------
        # INITIAL CONDITIONS
        # ---------------------------------------------

        temperatures[0] = (
            self.config.intake_temperature_k
        )

        pressures[0] = (
            self.config.intake_pressure_pa
        )

        total_combustion_energy = (
            self.thermo.released_combustion_energy()
        )

        # ---------------------------------------------
        # TIME STEP
        # ---------------------------------------------

        # Convert RPM into crankshaft degrees per second
        degrees_per_second = (
            self.config.rpm
            * 360.0
            / 60.0
        )

        # Time represented by one simulation step
        dt = (
            step_deg
            / degrees_per_second
        )

        # ---------------------------------------------
        # SIMULATION LOOP
        # ---------------------------------------------

        for i in range(1, len(angles)):
            angle_old = angles[i - 1]
            angle_new = angles[i]

            V_old = volumes[i - 1]
            V_new = volumes[i]

            P_old = pressures[i - 1]
            T_old = temperatures[i - 1]

            # -----------------------------------------
            # COMBUSTION
            # -----------------------------------------

            xb_old = self.combustion.burned_fraction(
                angle_old
            )

            xb_new = self.combustion.burned_fraction(
                angle_new
            )

            burned_fraction[i] = xb_new

            delta_xb = xb_new - xb_old

            # Energy released during this crank step
            dQ_combustion = (
                total_combustion_energy
                * delta_xb
            )

            heat_release[i] = dQ_combustion

            # -----------------------------------------
            # PISTON BOUNDARY WORK
            # -----------------------------------------

            dV = V_new - V_old

            # Positive during expansion
            # Negative during compression
            dW = P_old * dV

            # -----------------------------------------
            # WALL HEAT TRANSFER
            # -----------------------------------------

            piston_speed = (
                self.geometry.piston_velocity(
                    angle_old,
                    self.config.rpm
                )
            )

            surface_area = (
                self.geometry.chamber_surface_area(
                    angle_old
                )
            )

            dQ_wall = (
                self.thermo.wall_heat_loss(
                    pressure=P_old,
                    gas_temperature=T_old,
                    wall_temperature=(
                        self.config.wall_temperature_k
                    ),
                    surface_area=surface_area,
                    piston_speed=piston_speed,
                    dt=dt
                )
            )

            wall_heat_loss[i] = dQ_wall

            # -----------------------------------------
            # GAS PROPERTIES
            # -----------------------------------------

            # cv now changes with temperature
            cv = self.thermo.cv(T_old)

            # -----------------------------------------
            # FIRST LAW OF THERMODYNAMICS
            #
            # dU = dQ_combustion - dQ_wall - dW
            # -----------------------------------------

            dU = (
                dQ_combustion
                - dQ_wall
                - dW
            )

            dT = (
                dU
                / (total_mass * cv)
            )

            T_new = T_old + dT

            # Numerical safeguard
            T_new = max(
                T_new,
                200.0
            )

            # -----------------------------------------
            # PRESSURE
            # -----------------------------------------

            # Ideal gas relationship:
            #
            # P = mRT / V

            P_new = (
                total_mass
                * R
                * T_new
                / V_new
            )

            temperatures[i] = T_new
            pressures[i] = P_new

        # ---------------------------------------------
        # RETURN RESULTS
        # ---------------------------------------------

        return {
            "angle": angles,
            "volume": volumes,
            "pressure": pressures,
            "temperature": temperatures,
            "burned_fraction": burned_fraction,
            "heat_release": heat_release,
            "wall_heat_loss": wall_heat_loss,
        }