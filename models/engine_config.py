from dataclasses import dataclass


@dataclass
class EngineConfig:
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

    # Gas properties
    gamma: float = 1.35

    # Fuel
    afr: float = 14.7
    fuel_lhv_j_per_kg: float = 44_000_000

    # Combustion
    ignition_timing_deg: float = 15.0       # degrees before TDC
    combustion_duration_deg: float = 50.0   # crank degrees
    combustion_efficiency: float = 0.95

    # Thermal conditions
    wall_temperature_k: float = 450.0