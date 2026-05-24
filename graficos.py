import os
import math

import pandas as pd
import matplotlib.pyplot as plt


def theoretical_classic(n):

    return n ** 3


def theoretical_strassen(n):

    return n ** (math.log2(7))


def normalize_curve(real_times, theoretical_curve):

    if len(real_times) == 0:
        return theoretical_curve

    scale = real_times.iloc[0] / theoretical_curve[0]

    return [
        x * scale
        for x in theoretical_curve
    ]


def plot_experiment(data, experiment_name):

    experiment_data = data[
        data["experiment"] == experiment_name
    ]

    plt.figure(figsize=(10, 6))

    algorithms = experiment_data["algorithm"].unique()

    sizes = sorted(
        experiment_data["n"].unique()
    )

    for algorithm in algorithms:

        subset = experiment_data[
            experiment_data["algorithm"] == algorithm
        ]

        subset = subset.sort_values("n")

        plt.errorbar(
            subset["n"],
            subset["average_time"],
            yerr=subset["std_dev"],
            marker="o",
            capsize=4,
            label=algorithm
        )

    classic_curve = [
        theoretical_classic(n)
        for n in sizes
    ]

    strassen_curve = [
        theoretical_strassen(n)
        for n in sizes
    ]

    classic_times = experiment_data[
        experiment_data["algorithm"] == "Classic"
    ]["average_time"]

    strassen_times = experiment_data[
        experiment_data["algorithm"] == "Strassen"
    ]["average_time"]

    classic_curve = normalize_curve(
        classic_times,
        classic_curve
    )

    strassen_curve = normalize_curve(
        strassen_times,
        strassen_curve
    )

    plt.plot(
        sizes,
        classic_curve,
        linestyle="--",
        color="gray",
        label="Ajuste teorico O(n^3)"
    )

    plt.plot(
        sizes,
        strassen_curve,
        linestyle="--",
        color="black",
        label="Ajuste teorico O(n^2.807)"
    )

    plt.xscale("log", base=2)
    plt.yscale("log")

    plt.xlabel("Tamano de matriz (n)")
    plt.ylabel("Tiempo de ejecucion promedio (segundos)")
    plt.title(experiment_name)

    plt.grid(True, which="both", linestyle=":")
    plt.legend()

    filename = (
        experiment_name
        .replace(" ", "_")
        .lower()
        + ".png"
    )

    plt.tight_layout()
    plt.savefig(filename, dpi=300)

    print(f"Saved graph: {filename}")

    plt.close()


def plot_n0_results():

    if not os.path.exists("resultados_n0.csv"):
        print("resultados_n0.csv no encontrado.")
        return

    data = pd.read_csv("resultados_n0.csv")

    plt.figure(figsize=(10, 6))

    n0_values = sorted(
        data["n0"].unique()
    )

    for n0 in n0_values:

        subset = data[
            data["n0"] == n0
        ]

        subset = subset.sort_values("n")

        plt.errorbar(
            subset["n"],
            subset["average_time"],
            yerr=subset["std_dev"],
            marker="o",
            capsize=4,
            label=f"n0 = {n0}"
        )

    plt.xscale("log", base=2)
    plt.yscale("log")

    plt.xlabel("Tamano de matriz (n)")
    plt.ylabel("Tiempo de ejecucion promedio (segundos)")
    plt.title("Comparacion de valores n0 para Strassen hibrido")

    plt.grid(True, which="both", linestyle=":")
    plt.legend()

    filename = "comparacion_n0.png"

    plt.tight_layout()
    plt.savefig(filename, dpi=300)

    print(f"Saved graph: {filename}")

    plt.close()


def main():

    data = pd.read_csv("resultados.csv")

    experiments = data["experiment"].unique()

    for experiment in experiments:

        plot_experiment(
            data,
            experiment
        )

    plot_n0_results()


if __name__ == "__main__":
    main()