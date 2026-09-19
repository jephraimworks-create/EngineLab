from models.engine_config import EngineConfig

from engine.geometry import EngineGeometry
from engine.thermodynamics import Thermodynamics
from engine.combustion import CombustionModel
from engine.simulation import EngineSimulation
from engine.performance import PerformanceCalculator
from engine.energy import EnergyAnalysis

from plotting.plots import (
    plot_pressure_vs_angle,
    plot_temperature_vs_angle,
    plot_burned_fraction,
    plot_pv_diagram,
)


# --------------------------------------------------
# CREATE ENGINE
# --------------------------------------------------

config = EngineConfig()

geometry = EngineGeometry(config)
thermo = Thermodynamics(config, geometry)
combustion = CombustionModel(config)

simulation = EngineSimulation(
    config,
    geometry,
    thermo,
    combustion,
)

performance = PerformanceCalculator(
    config,
    geometry,
    thermo,
)

energy_analysis = EnergyAnalysis(
    config,
    geometry,
    thermo,
    performance,
)


# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

results = simulation.simulate_closed_cycle()
energy = energy_analysis.analyze(results)


# --------------------------------------------------
# BASIC ENGINE INFORMATION
# --------------------------------------------------

print("=== EngineLab V0.5 ===")

print(f"Displacement: {geometry.displacement_cc:.2f} cc")
print(f"Air per cycle: {thermo.trapped_air_mass() * 1000:.4f} g")
print(f"Fuel per cycle: {thermo.fuel_mass_per_cycle() * 1000:.5f} g")
print(f"Fuel energy: {thermo.fuel_energy_per_cycle():.2f} J")
print(
    f"Released combustion energy: "
    f"{thermo.released_combustion_energy():.2f} J"
)


# --------------------------------------------------
# PEAK CYLINDER CONDITIONS
# --------------------------------------------------

peak_pressure = results["pressure"].max() / 100000
peak_temperature = results["temperature"].max()

print()
print("=== Peak Conditions ===")
print(f"Peak cylinder pressure: {peak_pressure:.2f} bar")
print(f"Peak cylinder temperature: {peak_temperature:.1f} K")


# --------------------------------------------------
# PERFORMANCE
# --------------------------------------------------

compression_work = performance.compression_work(results)
expansion_work = performance.expansion_work(results)
net_work = performance.indicated_work(results)

imep_bar = performance.imep(results) / 100000

efficiency_percent = (
    performance.indicated_efficiency(results) * 100
)

power_w = performance.indicated_power(results)
torque_nm = performance.indicated_torque(results)

print()
print("=== Performance ===")
print(f"Compression work: {compression_work:.2f} J")
print(f"Expansion work: {expansion_work:.2f} J")
print(f"Net indicated work: {net_work:.2f} J/cycle")
print(f"IMEP: {imep_bar:.2f} bar")
print(f"Indicated efficiency: {efficiency_percent:.2f} %")
print(f"Indicated power @ {config.rpm:.0f} RPM: {power_w / 1000:.3f} kW")
print(f"Indicated horsepower: {power_w / 745.7:.2f} hp")
print(f"Indicated torque: {torque_nm:.3f} Nm")


# --------------------------------------------------
# ENERGY ANALYSIS
# --------------------------------------------------

fuel_energy = energy["fuel_energy"]

print()
print("=== Energy Analysis ===")

print(f"Fuel energy: {fuel_energy:.2f} J (100.0%)")

print(
    f"Released combustion energy: "
    f"{energy['released_energy']:.2f} J"
)

print(
    f"Indicated work: "
    f"{energy['indicated_work']:.2f} J "
    f"({energy['indicated_work'] / fuel_energy * 100:.1f}%)"
)

print(
    f"Wall heat loss: "
    f"{energy['wall_loss']:.2f} J "
    f"({energy['wall_loss'] / fuel_energy * 100:.1f}%)"
)

print(
    f"Unreleased combustion energy: "
    f"{energy['unreleased_energy']:.2f} J "
    f"({energy['unreleased_energy'] / fuel_energy * 100:.1f}%)"
)

print(
    f"Remaining energy: "
    f"{energy['remaining_energy']:.2f} J "
    f"({energy['remaining_energy'] / fuel_energy * 100:.1f}%)"
)


# --------------------------------------------------
# ENERGY BALANCE CHECK
# --------------------------------------------------

accounted_energy = (
    energy["indicated_work"]
    + energy["wall_loss"]
    + energy["unreleased_energy"]
    + energy["remaining_energy"]
)

balance_error = fuel_energy - accounted_energy

print()
print("=== Energy Balance Check ===")
print(f"Accounted energy: {accounted_energy:.2f} J")
print(f"Balance error: {balance_error:.6f} J")


# --------------------------------------------------
# GRAPHS
# --------------------------------------------------

plot_pressure_vs_angle(results)
plot_temperature_vs_angle(results)
plot_burned_fraction(results)
plot_pv_diagram(results)