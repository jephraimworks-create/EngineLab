from models.engine_config import EngineConfig

from engine.geometry import EngineGeometry
from engine.thermodynamics import Thermodynamics
from engine.simulation import EngineSimulation

from plotting.plots import plot_pressure_vs_angle


config = EngineConfig()

geometry = EngineGeometry(config)

thermo = Thermodynamics(
    config,
    geometry
)

simulation = EngineSimulation(
    config,
    geometry,
    thermo
)


print("=== EngineLab V0.2 ===")

print(
    f"Displacement: "
    f"{geometry.displacement_cc:.2f} cc"
)

print(
    f"Trapped air mass: "
    f"{thermo.trapped_air_mass() * 1000:.4f} g"
)


results = simulation.simulate_compression()


final_pressure = (
    results["pressure"][-1] / 100000
)

final_temperature = (
    results["temperature"][-1]
)


print(
    f"TDC Pressure: "
    f"{final_pressure:.2f} bar"
)

print(
    f"TDC Temperature: "
    f"{final_temperature:.1f} K"
)


plot_pressure_vs_angle(results)