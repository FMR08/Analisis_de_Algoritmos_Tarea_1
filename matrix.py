import random


def create_matrix(n, randomize=False, min_value=0, max_value=10):

    matrix = []

    for i in range(n):

        row = []

        for j in range(n):

            if randomize:
                value = random.randint(min_value, max_value)
            else:
                value = 0

            row.append(value)

        matrix.append(row)

    return matrix


def create_random_float_matrix(n):

    matrix = []

    for i in range(n):

        row = []

        for j in range(n):
            row.append(random.random())

        matrix.append(row)

    return matrix


def create_identity_matrix(n):

    matrix = create_matrix(n)

    for i in range(n):
        matrix[i][i] = 1

    return matrix


def create_constant_matrix(n, value):

    matrix = []

    for i in range(n):

        row = []

        for j in range(n):
            row.append(value)

        matrix.append(row)

    return matrix


def create_sparse_matrix(n, density=0.1):

    matrix = create_matrix(n)

    total_values = int(n * n * density)

    for _ in range(total_values):

        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        matrix[i][j] = random.randint(1, 10)

    return matrix


def copy_matrix(A):

    return [row[:] for row in A]


def add_matrix(A, B):

    n = len(A)

    C = create_matrix(n)

    for i in range(n):
        for j in range(n):

            C[i][j] = A[i][j] + B[i][j]

    return C


def sub_matrix(A, B):

    n = len(A)

    C = create_matrix(n)

    for i in range(n):
        for j in range(n):

            C[i][j] = A[i][j] - B[i][j]

    return C


def classic_multiply(A, B):

    n = len(A)

    C = create_matrix(n)

    for i in range(n):

        for j in range(n):

            total = 0

            for k in range(n):

                total += A[i][k] * B[k][j]

            C[i][j] = total

    return C


def split_matrix(A):

    n = len(A)

    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]

    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    return A11, A12, A21, A22


def join_matrix(C11, C12, C21, C22):

    n = len(C11)

    matrix = []

    for i in range(n):
        matrix.append(C11[i] + C12[i])

    for i in range(n):
        matrix.append(C21[i] + C22[i])

    return matrix


def print_matrix(A):

    for row in A:
        print(row)


def equal_matrix(A, B, epsilon=1e-9):

    n = len(A)

    for i in range(n):
        for j in range(n):

            if abs(A[i][j] - B[i][j]) > epsilon:
                return False

    return True


def matrix_size(A):

    return len(A), len(A[0])


def is_power_of_two(n):

    return n > 0 and (n & (n - 1)) == 0


def validate_square_matrix(A):

    rows = len(A)

    for row in A:

        if len(row) != rows:
            return False

    return True


def zero_pad_matrix(A, new_size):

    old_size = len(A)

    padded = create_matrix(new_size)

    for i in range(old_size):
        for j in range(old_size):

            padded[i][j] = A[i][j]

    return padded


def unpad_matrix(A, size):

    result = []

    for i in range(size):

        result.append(A[i][:size])

    return result


def next_power_of_two(n):

    power = 1

    while power < n:
        power *= 2

    return power