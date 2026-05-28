import csv
import platform
import ctypes

from benchmark import *


SIZES = [2, 4, 8, 16, 32, 64, 128, 256]

RUNS = 32

N0_SIZES = [32, 64, 128, 256]
N0_VALUES = [8, 16, 32, 64, 128]


def save_result(writer, experiment, algorithm, n, avg, std):

    writer.writerow([ experiment, algorithm, n, avg, std])


def get_ram_info():

    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memory_status = MEMORYSTATUSEX()
        memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

        ctypes.windll.kernel32.GlobalMemoryStatusEx(
            ctypes.byref(memory_status)
        )

        total_gb = memory_status.ullTotalPhys / (1024 ** 3)

        return f"{total_gb:.2f} GB"

    except Exception:
        return "No disponible"


def save_system_info():

    with open("system_info.txt", "w") as file:

        file.write("SYSTEM INFORMATION\n")
        file.write("=" * 40 + "\n")

        file.write(f"Operating System: {platform.platform()}\n")
        file.write(f"Processor: {platform.processor()}\n")
        file.write(f"RAM: {get_ram_info()}\n")
        file.write(f"Python Version: {platform.python_version()}\n")


def search_best_n0():
    best_n0 = None
    best_average = None

    with open("resultados_n0.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["n0", "n", "average_time", "std_dev"])

        for n0 in N0_VALUES:
            total_time = 0
            for n in N0_SIZES:
                A = create_matrix(n, randomize=True)
                B = create_matrix(n, randomize=True)

                result = benchmark(
                    lambda x, y: strassen_hybrid(x, y, n0),
                    A, B, runs=5
                )

                writer.writerow([n0, n, result["average"], result["std_dev"]])
                total_time += result["average"]

            average_for_n0 = total_time / len(N0_SIZES)
            if best_average is None or average_for_n0 < best_average:
                best_average = average_for_n0
                best_n0 = n0

    return best_n0


def run_experiment(
    writer,
    experiment_name,
    matrix_generator,
    best_n0
):


    for n in SIZES:

        A = matrix_generator(n)
        B = matrix_generator(n)

        classic_result = benchmark(
            classic_multiply,
            A,
            B,
            RUNS
        )

        strassen_result = benchmark(
            strassen,
            A,
            B,
            RUNS
        )

        hybrid_result = benchmark(
            lambda x, y: strassen_hybrid(x, y, best_n0),
            A,
            B,
            RUNS
        )

        save_result(
            writer,
            experiment_name,
            "Classic",
            n,
            classic_result["average"],
            classic_result["std_dev"]
        )

        save_result(
            writer,
            experiment_name,
            "Strassen",
            n,
            strassen_result["average"],
            strassen_result["std_dev"]
        )

        save_result(
            writer,
            experiment_name,
            f"Hybrid n0={best_n0}",
            n,
            hybrid_result["average"],
            hybrid_result["std_dev"]
        )


def main():


    verify_correctness(8)

    save_system_info()

    best_n0 = search_best_n0()

    with open(
        "resultados.csv",
        mode="w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "experiment",
            "algorithm",
            "n",
            "average_time",
            "std_dev"
        ])

        # Experimento 1
        run_experiment(
            writer,
            "Random Integers",
            lambda n: create_matrix(
                n,
                randomize=True
            ),
            best_n0
        )

        # Experimento 2
        run_experiment(
            writer,
            "Random Floats",
            create_random_float_matrix,
            best_n0
        )

        # Experimento 3
        run_experiment(
            writer,
            "Identity",
            create_identity_matrix,
            best_n0
        )

        # Experimento 4
        run_experiment(
            writer,
            "Sparse",
            lambda n: create_sparse_matrix(
                n,
                density=0.1
            ),
            best_n0
        )

    print("\nresultados.csv listo")
    print("\nsystem_info.txt listo")
    print("\nresultados_n0.csv listo")


if __name__ == "__main__":
    main()
