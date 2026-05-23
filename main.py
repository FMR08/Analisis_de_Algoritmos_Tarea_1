from benchmark import *

# tamaños potencia de 2
sizes = [2, 4, 8, 16, 32, 64, 128]

# verificar correctitud
verify_correctness(8)

# experimentos
experiment_random_integers(sizes)

experiment_random_floats(sizes)

experiment_identity(sizes)

experiment_sparse(sizes)

# buscar mejor n0
find_best_n0(
    sizes=[32, 64, 128],
    n0_values=[8, 16, 32, 64, 128]
)