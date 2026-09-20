import matplotlib.pyplot as plt


def plot_pressure_vs_angle(results):
    angle = results["angle"]

    pressure_bar = (
        results["pressure"]
        / 100000.0
    )

    plt.figure()

    plt.plot(
        angle,
        pressure_bar
    )

    plt.xlabel(
        "Crank Angle (degrees)"
    )

    plt.ylabel(
        "Cylinder Pressure (bar)"
    )

    plt.title(
        "Cylinder Pressure"
    )

    plt.grid()

    plt.tight_layout()
    plt.show()


def plot_temperature_vs_angle(results):
    plt.figure()

    plt.plot(
        results["angle"],
        results["temperature"]
    )

    plt.xlabel(
        "Crank Angle (degrees)"
    )

    plt.ylabel(
        "Cylinder Temperature (K)"
    )

    plt.title(
        "Cylinder Temperature"
    )

    plt.grid()

    plt.tight_layout()
    plt.show()


def plot_burned_fraction(results):
    burned_percent = (
        results["burned_fraction"]
        * 100.0
    )

    plt.figure()

    plt.plot(
        results["angle"],
        burned_percent
    )

    plt.xlabel(
        "Crank Angle (degrees)"
    )

    plt.ylabel(
        "Fuel Burned (%)"
    )

    plt.title(
        "Combustion Progress"
    )

    plt.grid()

    plt.tight_layout()
    plt.show()


def plot_pv_diagram(results):
    volume_cc = (
        results["volume"]
        * 1_000_000.0
    )

    pressure_bar = (
        results["pressure"]
        / 100000.0
    )

    plt.figure()

    plt.plot(
        volume_cc,
        pressure_bar
    )

    plt.xlabel(
        "Cylinder Volume (cc)"
    )

    plt.ylabel(
        "Cylinder Pressure (bar)"
    )

    plt.title(
        "P-V Diagram"
    )

    plt.grid()

    plt.tight_layout()
    plt.show()


def plot_expansion_work(sweep_results):
    ratios = [
        result["ratio"]
        for result in sweep_results
    ]

    ideal_work = [
        result["ideal_extra_work"]
        for result in sweep_results
    ]

    heat_loss_work = [
        result["heat_loss_extra_work"]
        for result in sweep_results
    ]

    plt.figure()

    plt.plot(
        ratios,
        ideal_work,
        marker="o",
        label="Ideal"
    )

    plt.plot(
        ratios,
        heat_loss_work,
        marker="o",
        label="With Heat Loss"
    )

    plt.xlabel(
        "Total Expansion Ratio"
    )

    plt.ylabel(
        "Additional Work (J/cycle)"
    )

    plt.title(
        "Secondary Expansion Work"
    )

    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_expansion_efficiency(
    sweep_results
):
    ratios = [
        result["ratio"]
        for result in sweep_results
    ]

    ideal_efficiency = [
        result["ideal_efficiency"]
        * 100.0
        for result in sweep_results
    ]

    heat_loss_efficiency = [
        result["heat_loss_efficiency"]
        * 100.0
        for result in sweep_results
    ]

    plt.figure()

    plt.plot(
        ratios,
        ideal_efficiency,
        marker="o",
        label="Ideal Secondary Expansion"
    )

    plt.plot(
        ratios,
        heat_loss_efficiency,
        marker="o",
        label="With Heat Loss"
    )

    plt.xlabel(
        "Total Expansion Ratio"
    )

    plt.ylabel(
        "Gross Indicated Efficiency (%)"
    )

    plt.title(
        "Efficiency vs Expansion Ratio"
    )

    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_expansion_final_pressure(
    sweep_results
):
    ratios = [
        result["ratio"]
        for result in sweep_results
    ]

    pressures = [
        result["heat_loss_final_pressure"]
        / 100000.0
        for result in sweep_results
    ]

    plt.figure()

    plt.plot(
        ratios,
        pressures,
        marker="o"
    )

    plt.axhline(
        y=1.01325,
        linestyle="--",
        label="Atmospheric Pressure"
    )

    plt.xlabel(
        "Total Expansion Ratio"
    )

    plt.ylabel(
        "Final Pressure (bar)"
    )

    plt.title(
        "Secondary Expansion Final Pressure"
    )

    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_expansion_final_temperature(
    sweep_results
):
    ratios = [
        result["ratio"]
        for result in sweep_results
    ]

    temperatures = [
        result["heat_loss_final_temperature"]
        for result in sweep_results
    ]

    plt.figure()

    plt.plot(
        ratios,
        temperatures,
        marker="o"
    )

    plt.xlabel(
        "Total Expansion Ratio"
    )

    plt.ylabel(
        "Final Gas Temperature (K)"
    )

    plt.title(
        "Secondary Expansion Final Temperature"
    )

    plt.grid()

    plt.tight_layout()
    plt.show()