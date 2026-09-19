import matplotlib.pyplot as plt


def plot_pressure_vs_angle(results):

    angle = results["angle"]
    pressure_bar = results["pressure"] / 100000

    plt.figure()

    plt.plot(angle, pressure_bar)

    plt.xlabel("Crank Angle (degrees)")
    plt.ylabel("Cylinder Pressure (bar)")
    plt.title("Compression Stroke")

    plt.grid()

    plt.show()