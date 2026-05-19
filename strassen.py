from matrix import *


def strassen(A, B):

    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)
    M1 = strassen(
        add_matrix(A11, A22),
        add_matrix(B11, B22)
    )

    M2 = strassen(
        add_matrix(A21, A22),
        B11
    )

    M3 = strassen(
        A11,
        sub_matrix(B12, B22)
    )

    M4 = strassen(
        A22,
        sub_matrix(B21, B11)
    )

    M5 = strassen(
        add_matrix(A11, A12),
        B22
    )

    M6 = strassen(
        sub_matrix(A21, A11),
        add_matrix(B11, B12)
    )

    M7 = strassen(
        sub_matrix(A12, A22),
        add_matrix(B21, B22)
    )
    C11 = add_matrix(
        sub_matrix(
            add_matrix(M1, M4),
            M5
        ),
        M7
    )

    C12 = add_matrix(M3, M5)

    C21 = add_matrix(M2, M4)

    C22 = add_matrix(
        add_matrix(
            sub_matrix(M1, M2),
            M3
        ),
        M6
    )
    return join_matrix(C11, C12, C21, C22)


def strassen_hybrid(A, B, n0=64):

    n = len(A)

    #hibrido
    if n <= n0:
        return classic_multiply(A, B)

    #absoluto
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    M1 = strassen_hybrid(
        add_matrix(A11, A22),
        add_matrix(B11, B22),
        n0
    )

    M2 = strassen_hybrid(
        add_matrix(A21, A22),
        B11,
        n0
    )

    M3 = strassen_hybrid(
        A11,
        sub_matrix(B12, B22),
        n0
    )

    M4 = strassen_hybrid(
        A22,
        sub_matrix(B21, B11),
        n0
    )

    M5 = strassen_hybrid(
        add_matrix(A11, A12),
        B22,
        n0
    )

    M6 = strassen_hybrid(
        sub_matrix(A21, A11),
        add_matrix(B11, B12),
        n0
    )

    M7 = strassen_hybrid(
        sub_matrix(A12, A22),
        add_matrix(B21, B22),
        n0
    )
    C11 = add_matrix(
        sub_matrix(
            add_matrix(M1, M4),
            M5
        ),
        M7
    )

    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)

    C22 = add_matrix(
        add_matrix(
            sub_matrix(M1, M2),
            M3
        ),
        M6
    )
    return join_matrix(C11, C12, C21, C22)


def strassen_general(A, B):
    original_size = len(A)

    if not is_power_of_two(original_size):
        new_size = next_power_of_two(original_size)
        A = zero_pad_matrix(A, new_size)
        B = zero_pad_matrix(B, new_size)
        C = strassen(A, B)
        return unpad_matrix(C, original_size)

    return strassen(A, B)
