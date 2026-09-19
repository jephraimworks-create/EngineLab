import numpy as np


class EngineSimulation:

    def __init__(self, config, geometry, thermo):
        self.config = config
        self.geometry = geometry
        self.thermo = thermo

    def simulate_compression(self):
        angles = np.linspace(180, 360, 361)

        volumes = []
        pressures = []
        temperatures = []

        for angle in angles:
            volume = self.geometry.cylinder_volume(angle)

            pressure = (
                self.thermo.compression_pressure(volume)
            )

            temperature = (
                self.thermo.compression_temperature(volume)
            )

            volumes.append(volume)
            pressures.append(pressure)
            temperatures.append(temperature)

        return {
            "angle": np.array(angles),
            "volume": np.array(volumes),
            "pressure": np.array(pressures),
            "temperature": np.array(temperatures),
        }