import matplotlib.pyplot as plt


def plot_pressure_vs_angle(results):

    angle = results["angle"]
    pressure_bar = results["pressure"] / 100000

    plt.figure()

    plt.plot(angle, pressure_bar)

    plt.xlabel("Crank Angle (degrees)")
    plt.ylabel("Cylinder Pressure (bar)")
    plt.title("Cylinder Pressure")

    plt.grid()

    plt.show()


def plot_temperature_vs_angle(results):

    angle = results["angle"]
    temperature = results["temperature"]

    plt.figure()

    plt.plot(angle, temperature)

    plt.xlabel("Crank Angle (degrees)")
    plt.ylabel("Cylinder Temperature (K)")
    plt.title("Cylinder Temperature")

    plt.grid()

    plt.show()


def plot_burned_fraction(results):

    angle = results["angle"]
    burned = results["burned_fraction"] * 100

    plt.figure()

    plt.plot(angle, burned)

    plt.xlabel("Crank Angle (degrees)")
    plt.ylabel("Fuel Burned (%)")
    plt.title("Combustion Progress")

    plt.grid()

    plt.show()


def plot_pv_diagram(results):

    volume_cc = (
        results["volume"]
        * 1_000_000
    )

    pressure_bar = (
        results["pressure"]
        / 100000
    )

    plt.figure()

    plt.plot(
        volume_cc,
        pressure_bar
    )

    plt.xlabel("Cylinder Volume (cc)")
    plt.ylabel("Cylinder Pressure (bar)")
    plt.title("P-V Diagram")

    plt.grid()

    plt.show()