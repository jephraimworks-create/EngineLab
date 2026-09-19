from models.engine_config import EngineConfig

from engine.geometry import EngineGeometry
from engine.thermodynamics import Thermodynamics
from engine.combustion import CombustionModel
from engine.simulation import EngineSimulation

from plotting.plots import (
    plot_pressure_vs_angle,
    plot_temperature_vs_angle,
    plot_burned_fraction,
    plot_pv_diagram,
)


config = EngineConfig()

geometry = EngineGeometry(config)

thermo = Thermodynamics(
    config,
    geometry
)

combustion = CombustionModel(
    config
)

simulation = EngineSimulation(
    config,
    geometry,
    thermo,
    combustion
)


print("=== EngineLab V0.3 ===")

print(
    f"Displacement: "
    f"{geometry.displacement_cc:.2f} cc"
)

print(
    f"Air per cycle: "
    f"{thermo.trapped_air_mass() * 1000:.4f} g"
)

print(
    f"Fuel per cycle: "
    f"{thermo.fuel_mass_per_cycle() * 1000:.5f} g"
)

print(
    f"Fuel energy: "
    f"{thermo.fuel_energy_per_cycle():.2f} J"
)

print(
    f"Released combustion energy: "
    f"{thermo.released_combustion_energy():.2f} J"
)


results = simulation.simulate_closed_cycle()


peak_pressure = (
    results["pressure"].max()
    / 100000
)

peak_temperature = (
    results["temperature"].max()
)


print()

print(
    f"Peak cylinder pressure: "
    f"{peak_pressure:.2f} bar"
)

print(
    f"Peak cylinder temperature: "
    f"{peak_temperature:.1f} K"
)


plot_pressure_vs_angle(results)

plot_temperature_vs_angle(results)

plot_burned_fraction(results)

plot_pv_diagram(results)