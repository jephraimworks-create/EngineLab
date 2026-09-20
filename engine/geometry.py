import math

import numpy as np


class EngineGeometry:
    """Conventional slider-crank geometry for the primary cylinder."""

    def __init__(self, config):
        self.config = config

        self.bore = config.bore_mm / 1000.0
        self.stroke = config.stroke_mm / 1000.0
        self.rod_length = config.rod_length_mm / 1000.0

        self.crank_radius = self.stroke / 2.0

        self.piston_area = (
            math.pi * self.bore**2 / 4.0
        )

        self.swept_volume = (
            self.piston_area * self.stroke
        )

        self.clearance_volume = (
            self.swept_volume
            / (config.compression_ratio - 1.0)
        )

    def piston_position(self, crank_angle_deg):
        """
        Piston displacement from TDC.

        Returns:
            Position in metres.
        """

        theta = np.radians(crank_angle_deg)

        r = self.crank_radius
        l = self.rod_length

        under_root = (
            l**2
            - (r * np.sin(theta))**2
        )

        position = (
            r * (1.0 - np.cos(theta))
            + l
            - np.sqrt(under_root)
        )

        return position

    def cylinder_volume(self, crank_angle_deg):
        """Cylinder volume at a given crank angle."""

        position = self.piston_position(
            crank_angle_deg
        )

        return (
            self.clearance_volume
            + self.piston_area * position
        )

    def piston_velocity(self, crank_angle_deg, rpm):
        """
        Numerically calculate instantaneous piston velocity.

        Returns:
            m/s
        """

        delta_angle = 0.01

        x_before = self.piston_position(
            crank_angle_deg - delta_angle
        )

        x_after = self.piston_position(
            crank_angle_deg + delta_angle
        )

        dx_dtheta = (
            (x_after - x_before)
            / (2.0 * delta_angle)
        )

        degrees_per_second = (
            rpm * 360.0 / 60.0
        )

        return (
            dx_dtheta * degrees_per_second
        )

    def chamber_surface_area(self, crank_angle_deg):
        """
        Approximate exposed cylinder surface area.

        Includes:
        - piston crown
        - cylinder head
        - exposed cylinder liner
        """

        piston_position = self.piston_position(
            crank_angle_deg
        )

        piston_crown_area = self.piston_area
        head_area = self.piston_area

        liner_area = (
            math.pi
            * self.bore
            * piston_position
        )

        return (
            piston_crown_area
            + head_area
            + liner_area
        )

    @property
    def displacement_cc(self):
        return (
            self.swept_volume
            * 1_000_000.0
        )

    @property
    def clearance_volume_cc(self):
        return (
            self.clearance_volume
            * 1_000_000.0
        )

    @property
    def total_bdc_volume_cc(self):
        return (
            (
                self.swept_volume
                + self.clearance_volume
            )
            * 1_000_000.0
        )