from dataclasses import dataclass


@dataclass
class EngineConfig:
    """Central configuration for the EngineLab engine model."""

    # Geometry
    bore_mm: float = 50.0
    stroke_mm: float = 50.0
    rod_length_mm: float = 100.0
    cylinders: int = 1
    compression_ratio: float = 10.0

    # Operating conditions
    rpm: float = 2000.0

    # Intake conditions
    intake_pressure_pa: float = 101325.0
    intake_temperature_k: float = 298.15

    # Fuel
    afr: float = 14.7
    fuel_lhv_j_per_kg: float = 44_000_000.0
    combustion_efficiency: float = 0.95

    # Combustion
    combustion_start_btdc_deg: float = 15.0
    combustion_duration_deg: float = 50.0
    wiebe_a: float = 5.0
    wiebe_m: float = 2.0

    # Thermal conditions
    wall_temperature_k: float = 450.0

    # Simulation
    crank_step_deg: float = 0.5

    # Secondary-expansion sweep
    secondary_expansion_ratios: tuple = (
        10.0,
        12.0,
        14.0,
        16.0,
        18.0,
        20.0,
        25.0,
        30.0,
    )

    secondary_steps: int = 500