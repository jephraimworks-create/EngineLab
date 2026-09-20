from models.engine_config import EngineConfig

from engine.geometry import EngineGeometry
from engine.thermodynamics import Thermodynamics
from engine.combustion import CombustionModel
from engine.simulation import EngineSimulation
from engine.performance import PerformanceCalculator
from engine.energy import EnergyAnalysis
from engine.secondary_expansion import SecondaryExpansion
from engine.expansion_sweep import ExpansionSweep

from plotting.plots import (
    plot_pressure_vs_angle,
    plot_temperature_vs_angle,
    plot_burned_fraction,
    plot_pv_diagram,
    plot_expansion_work,
    plot_expansion_efficiency,
    plot_expansion_final_pressure,
    plot_expansion_final_temperature,
)


def build_engine():
    """Create all EngineLab model components."""

    config = EngineConfig()

    geometry = EngineGeometry(
        config
    )

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

    performance = PerformanceCalculator(
        config,
        geometry,
        thermo
    )

    energy_analysis = EnergyAnalysis(
        config,
        geometry,
        thermo,
        performance
    )

    secondary = SecondaryExpansion(
        config,
        geometry,
        thermo
    )

    sweep = ExpansionSweep(
        config,
        geometry,
        thermo,
        secondary
    )

    return {
        "config": config,
        "geometry": geometry,
        "thermo": thermo,
        "combustion": combustion,
        "simulation": simulation,
        "performance": performance,
        "energy_analysis": energy_analysis,
        "sweep": sweep,
    }


def print_primary_results(
    engine,
    results,
    energy
):
    config = engine["config"]
    geometry = engine["geometry"]
    thermo = engine["thermo"]
    combustion = engine["combustion"]
    performance = engine["performance"]

    work = (
        performance.indicated_work(
            results
        )
    )

    compression_work = (
        performance.compression_work(
            results
        )
    )

    expansion_work = (
        performance.expansion_work(
            results
        )
    )

    efficiency = (
        performance.gross_indicated_efficiency(
            results
        )
    )

    power = (
        performance.indicated_power_w(
            results
        )
    )

    torque = (
        performance.indicated_torque_nm(
            results
        )
    )

    imep_bar = (
        performance.gross_imep_pa(
            results
        )
        / 100000.0
    )

    peak_pressure_index = (
        results["pressure"].argmax()
    )

    peak_temperature_index = (
        results["temperature"].argmax()
    )

    print("=== EngineLab V1.0 ===")

    print(
        f"Displacement: "
        f"{geometry.displacement_cc:.2f} cc"
    )

    print(
        f"Compression ratio: "
        f"{config.compression_ratio:.2f}:1"
    )

    print(
        f"Engine speed: "
        f"{config.rpm:.0f} RPM"
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
        f"{energy['fuel_energy']:.2f} J"
    )

    print()

    print("=== Combustion ===")

    print(
        "Model: Single Wiebe"
    )

    print(
        f"Start of combustion: "
        f"{combustion.start_angle():.1f} deg"
    )

    print(
        f"Nominal combustion end: "
        f"{combustion.nominal_end_angle():.1f} deg"
    )

    nominal_burned_fraction = (
        combustion.burned_fraction(
            combustion.nominal_end_angle()
        )
        * 100.0
    )

    print(
        f"Burned fraction at nominal end: "
        f"{nominal_burned_fraction:.2f}%"
    )

    print()

    print("=== Peak Conditions ===")

    print(
        f"Peak pressure: "
        f"{results['pressure'][peak_pressure_index] / 100000:.2f} bar"
    )

    print(
        f"Peak pressure angle: "
        f"{results['angle'][peak_pressure_index]:.1f} deg"
    )

    print(
        f"Peak temperature: "
        f"{results['temperature'][peak_temperature_index]:.1f} K"
    )

    print()

    print("=== Primary Performance ===")

    print(
        f"Compression work: "
        f"{compression_work:.2f} J"
    )

    print(
        f"Expansion work: "
        f"{expansion_work:.2f} J"
    )

    print(
        f"Gross indicated work: "
        f"{work:.2f} J/cycle"
    )

    print(
        f"Gross IMEP: "
        f"{imep_bar:.2f} bar"
    )

    print(
        f"Gross indicated efficiency: "
        f"{efficiency * 100:.2f}%"
    )

    print(
        f"Indicated power: "
        f"{power / 1000:.3f} kW"
    )

    print(
        f"Indicated horsepower: "
        f"{power / 745.7:.2f} hp"
    )

    print(
        f"Indicated torque: "
        f"{torque:.3f} Nm"
    )

    print()

    print("=== Primary Energy Analysis ===")

    print(
        f"Fuel energy: "
        f"{energy['fuel_energy']:.2f} J"
    )

    print(
        f"Actual combustion heat release: "
        f"{energy['actual_heat_release']:.2f} J"
    )

    print(
        f"Wall heat loss: "
        f"{energy['wall_heat_loss']:.2f} J"
    )

    print(
        f"Combustion efficiency loss: "
        f"{energy['combustion_loss']:.2f} J"
    )

    print(
        f"Remaining energy bucket: "
        f"{energy['remaining_energy']:.2f} J"
    )

    print()

    print("=== End of Primary Expansion ===")

    print(
        f"Pressure: "
        f"{energy['end_pressure_pa'] / 100000:.2f} bar"
    )

    print(
        f"Temperature: "
        f"{energy['end_temperature_k']:.1f} K"
    )

    print(
        f"Volume: "
        f"{energy['end_volume_m3'] * 1_000_000:.2f} cc"
    )

    print(
        f"Gamma: "
        f"{energy['end_gamma']:.4f}"
    )


def print_secondary_results(
    sweep_results
):
    print()

    print("=== Secondary Expansion Sweep ===")

    header = (
        f"{'Ratio':>8}"
        f"{'Ideal +W':>13}"
        f"{'Heat +W':>13}"
        f"{'Total W':>13}"
        f"{'Eff.':>10}"
        f"{'Final P':>11}"
        f"{'Final T':>11}"
        f"{'Balance':>12}"
    )

    print(header)
    print("-" * len(header))

    for result in sweep_results:
        print(
            f"{result['ratio']:>7.1f}:1"
            f"{result['ideal_extra_work']:>11.2f} J"
            f"{result['heat_loss_extra_work']:>11.2f} J"
            f"{result['heat_loss_total_work']:>11.2f} J"
            f"{result['heat_loss_efficiency'] * 100:>9.2f}%"
            f"{result['heat_loss_final_pressure'] / 100000:>10.2f}"
            f"{result['heat_loss_final_temperature']:>10.1f}"
            f"{result['heat_loss_balance_error']:>11.3f}"
        )

    print()

    print(
        "Secondary results are indicated "
        "thermodynamic estimates."
    )

    print(
        "Transfer losses, pumping losses, dead volume, "
        "and mechanism friction are not yet included."
    )


def show_plots(
    primary_results,
    sweep_results
):
    plot_pressure_vs_angle(
        primary_results
    )

    plot_temperature_vs_angle(
        primary_results
    )

    plot_burned_fraction(
        primary_results
    )

    plot_pv_diagram(
        primary_results
    )

    plot_expansion_work(
        sweep_results
    )

    plot_expansion_efficiency(
        sweep_results
    )

    plot_expansion_final_pressure(
        sweep_results
    )

    plot_expansion_final_temperature(
        sweep_results
    )


def main():
    engine = build_engine()

    simulation = engine["simulation"]
    performance = engine["performance"]
    thermo = engine["thermo"]
    energy_analysis = engine["energy_analysis"]
    sweep = engine["sweep"]

    primary_results = (
        simulation.simulate_closed_cycle()
    )

    energy = (
        energy_analysis.analyze(
            primary_results
        )
    )

    primary_work = (
        performance.indicated_work(
            primary_results
        )
    )

    fuel_energy = (
        thermo.fuel_energy_per_cycle()
    )

    sweep_results = (
        sweep.run(
            primary_results=primary_results,
            primary_work=primary_work,
            fuel_energy=fuel_energy
        )
    )

    print_primary_results(
        engine,
        primary_results,
        energy
    )

    print_secondary_results(
        sweep_results
    )

    show_plots(
        primary_results,
        sweep_results
    )


if __name__ == "__main__":
    main()