import time
import statistics
import math

from matrix import *
from strassen import *


def benchmark(function, A, B, runs=32):

    times = []

    for _ in range(runs):

        start = time.perf_counter()

        function(A, B)

        end = time.perf_counter()

        execution_time = end - start

        times.append(execution_time)

    average = statistics.mean(times)

    std_dev = statistics.stdev(times)

    minimum = min(times)

    maximum = max(times)

    return {
        "average": average,
        "std_dev": std_dev,
        "min": minimum,
        "max": maximum,
        "runs": runs
    }


def print_benchmark_result(name, n, result):

    print(f"\n{name}")
    print(f"Matrix size: {n}x{n}")

    print(f"Average time: {result['average']:.8f} seconds")
    print(f"Standard deviation: {result['std_dev']:.8f} seconds")
    print(f"Minimum time: {result['min']:.8f} seconds")
    print(f"Maximum time: {result['max']:.8f} seconds")


def compare_algorithms(A, B, runs=32, n0=64):

    n = len(A)

    print(f"\nCOMPARACIÓN DE {n}x{n}")


    classic_result = benchmark(
        classic_multiply,
        A,
        B,
        runs
    )

    strassen_result = benchmark(
        strassen,
        A,
        B,
        runs
    )

    hybrid_result = benchmark(
        lambda x, y: strassen_hybrid(x, y, n0),
        A,
        B,
        runs
    )

    print_benchmark_result(
        "CLASSIC MULTIPLICACIÓN",
        n,
        classic_result
    )

    print_benchmark_result(
        "STRASSEN MULTIPLICACIÓN",
        n,
        strassen_result
    )

    print_benchmark_result(
        "HYBRID STRASSEN",
        n,
        hybrid_result
    )

    return {
        "classic": classic_result,
        "strassen": strassen_result,
        "hybrid": hybrid_result
    }


def theoretical_classic(n):

    return n ** 3


def theoretical_strassen(n):

    return n ** (math.log2(7))


def experiment_random_integers(
    sizes,
    runs=32
):

    print("\n1 ENTEROS ALEATORIOS")

    results = []

    for n in sizes:

        print(f"\nSize {n}x{n}")

        A = create_matrix(
            n,
            randomize=True,
            min_value=0,
            max_value=10
        )

        B = create_matrix(
            n,
            randomize=True,
            min_value=0,
            max_value=10
        )

        result = compare_algorithms(
            A,
            B,
            runs
        )

        results.append((n, result))

    return results


def experiment_random_floats(
    sizes,
    runs=32
):

    print("\n2 FLOTACIÓN ALEATORIAS")

    results = []

    for n in sizes:

        print(f"\nSize {n}x{n}")

        A = create_random_float_matrix(n)

        B = create_random_float_matrix(n)

        result = compare_algorithms(
            A,
            B,
            runs
        )

        results.append((n, result))

    return results


def experiment_identity(
    sizes,
    runs=32
):

    print("\n3 MATRICES DE IDENTIDAD")

    results = []

    for n in sizes:

        print(f"\nSize {n}x{n}")

        A = create_identity_matrix(n)

        B = create_identity_matrix(n)

        result = compare_algorithms(
            A,
            B,
            runs
        )

        results.append((n, result))

    return results


def experiment_sparse(
    sizes,
    runs=32,
    density=0.1
):

    print("\n4 MATRICES DISPERSAS ")


    results = []

    for n in sizes:

        print(f"\nSize {n}x{n}")

        A = create_sparse_matrix(
            n,
            density
        )

        B = create_sparse_matrix(
            n,
            density
        )

        result = compare_algorithms(
            A,
            B,
            runs
        )

        results.append((n, result))

    return results


def experiment_constant(
    sizes,
    runs=32,
    value=1
):

    print("\n5 MATRICES CONSTANTES")

    results = []

    for n in sizes:

        print(f"\nSize {n}x{n}")

        A = create_constant_matrix(
            n,
            value
        )

        B = create_constant_matrix(
            n,
            value
        )

        result = compare_algorithms(
            A,
            B,
            runs
        )

        results.append((n, result))

    return results


def find_best_n0(
    sizes,
    n0_values,
    runs=32
):

    print("\nBUSCANDO EL MEJOR PARA HÍBRIDOS STRASSEN")


    best_n0 = None

    best_time = float("inf")

    for n0 in n0_values:

        print(f"\nnumero de Testing= {n0}")

        total_time = 0

        for n in sizes:

            A = create_matrix(
                n,
                randomize=True
            )

            B = create_matrix(
                n,
                randomize=True
            )

            result = benchmark(
                lambda x, y: strassen_hybrid(x, y, n0),
                A,
                B,
                runs
            )

            total_time += result["average"]

        print(f"Tiempo promedio: {total_time:.8f}")

        if total_time < best_time:

            best_time = total_time

            best_n0 = n0

    print("\n")
    print(f"BEST FOUND: {best_n0}")
    print(f"BEST TIME: {best_time:.8f}")

    return best_n0


def verify_correctness(n=8):

    print("\nVERIFICACIÓN")

    A = create_matrix(
        n,
        randomize=True
    )

    B = create_matrix(
        n,
        randomize=True
    )

    classic_result = classic_multiply(A, B)

    strassen_result = strassen(A, B)

    hybrid_result = strassen_hybrid(A, B)

    print(
        "Classic vs Strassen:",
        equal_matrix(classic_result, strassen_result)
    )

    print(
        "Classic vs Hybrid:",
        equal_matrix(classic_result, hybrid_result)
    )

    return (
        equal_matrix(classic_result, strassen_result)
        and
        equal_matrix(classic_result, hybrid_result)
    )