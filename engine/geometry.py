import math
import numpy as np

from models.engine_config import EngineConfig


class EngineGeometry:

    def __init__(self, config: EngineConfig):
        self.config = config

        self.bore = config.bore_mm / 1000
        self.stroke = config.stroke_mm / 1000
        self.rod_length = config.rod_length_mm / 1000

        self.crank_radius = self.stroke / 2

        self.piston_area = math.pi * self.bore**2 / 4

        self.swept_volume = self.piston_area * self.stroke

        self.clearance_volume = (
            self.swept_volume /
            (config.compression_ratio - 1)
        )

    def piston_position(self, crank_angle_deg):
        theta = np.radians(crank_angle_deg)

        r = self.crank_radius
        l = self.rod_length

        position = (
            r * (1 - np.cos(theta))
            + l
            - np.sqrt(l**2 - (r * np.sin(theta))**2)
        )

        return position

    def cylinder_volume(self, crank_angle_deg):
        position = self.piston_position(crank_angle_deg)

        return (
            self.clearance_volume
            + self.piston_area * position
        )

    @property
    def displacement_cc(self):
        return self.swept_volume * 1_000_000

    @property
    def clearance_volume_cc(self):
        return self.clearance_volume * 1_000_000

    @property
    def total_bdc_volume_cc(self):
        return (
            self.swept_volume
            + self.clearance_volume
        ) * 1_000_000