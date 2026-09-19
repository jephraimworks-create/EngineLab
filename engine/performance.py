import numpy as np


class PerformanceCalculator:
    """
    Calculates engine performance from simulated
    cylinder pressure and volume data.
    """

    def __init__(self, config, geometry, thermo):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo

    def indicated_work(self, results):
        """
        Calculate net indicated work using:

            W = integral(P dV)

        Returns:
            Work per cycle in joules.
        """

        pressure = results["pressure"]
        volume = results["volume"]

        # Average pressure across each simulation step
        pressure_avg = (
            pressure[:-1] + pressure[1:]
        ) / 2.0

        # Volume change for each step
        delta_volume = np.diff(volume)

        # dW = P dV
        work_steps = pressure_avg * delta_volume

        # Sum work across entire closed cycle
        work = np.sum(work_steps)

        return work

    def imep(self, results):
        """
        Indicated Mean Effective Pressure.

            IMEP = W / Vd

        Returns:
            Pressure in Pa.
        """

        work = self.indicated_work(results)

        return work / self.geometry.swept_volume

    def indicated_efficiency(self, results):
        """
        Fraction of fuel chemical energy converted
        into indicated cylinder work.

            efficiency = W / fuel energy
        """

        work = self.indicated_work(results)

        fuel_energy = (
            self.thermo.fuel_energy_per_cycle()
        )

        return work / fuel_energy

    def indicated_power(self, results):
        """
        Calculate indicated engine power.

        A four-stroke cylinder completes one cycle
        every two crankshaft revolutions.
        """

        work_per_cycle = self.indicated_work(results)

        cycles_per_second = (
            self.config.rpm / 120.0
        )

        total_power = (
            work_per_cycle
            * cycles_per_second
            * self.config.cylinders
        )

        return total_power

    def indicated_torque(self, results):
        """
        Calculate average indicated torque from power.

            torque = power / angular velocity
        """

        power = self.indicated_power(results)

        angular_velocity = (
            2.0
            * np.pi
            * self.config.rpm
            / 60.0
        )

        torque = power / angular_velocity

        return torque

    def compression_work(self, results):
        """
        Work during the compression portion
        from 180 to 360 degrees.
        """

        angle = results["angle"]
        pressure = results["pressure"]
        volume = results["volume"]

        mask = angle <= 360.0

        pressure = pressure[mask]
        volume = volume[mask]

        pressure_avg = (
            pressure[:-1] + pressure[1:]
        ) / 2.0

        delta_volume = np.diff(volume)

        return np.sum(
            pressure_avg * delta_volume
        )

    def expansion_work(self, results):
        """
        Work during the expansion portion
        from 360 to 540 degrees.
        """

        angle = results["angle"]
        pressure = results["pressure"]
        volume = results["volume"]

        mask = angle >= 360.0

        pressure = pressure[mask]
        volume = volume[mask]

        pressure_avg = (
            pressure[:-1] + pressure[1:]
        ) / 2.0

        delta_volume = np.diff(volume)

        return np.sum(
            pressure_avg * delta_volume
        )