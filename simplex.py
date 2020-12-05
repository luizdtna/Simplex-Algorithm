# Developed by Luiz Araujo

import numpy as np


pivot_vector = []


def matrix_scaling(matrix, pivot_row, pivot_col):
    pivot = float(matrix[pivot_row][pivot_col])

    """if matrix[pivot_row][pivot_col] > 1: #se o pivo for maior que 1, faz opreções para que ele vire 1.
        first_calculation = np.array([i / pivot if i != 0.0 else 0 for i in matrix[pivot_row]], dtype=float)
        matrix[pivot_row] = first_calculation
        pivot = int(matrix[pivot_row][pivot_col])
        print(matrix.astype(int))"""
    for i in range(len(matrix)):

        if matrix[i][pivot_col] == 0:  # If the valeu in the same column of the pivot is 0
            continue

        if i != pivot_row:  # If is not the pivot row

            first_calculation = pivot * matrix[i]
            # print(base_matrix[i])
            second_calculation = matrix[i][pivot_col] * matrix[pivot_row]
            # print(second_calculation)
            result = first_calculation - second_calculation

            matrix[i] = result  # Updade the row of base matrix

    return matrix, pivot


def change_base_column(matrix, index_new_column):
    column_B = matrix[:, -1][:-1]
    new_column_base = matrix[:, index_new_column][:-1]

    if len(np.where(new_column_base <= 0)) == 0:
        # if there are some zero or negative variables in the new base vector
        column_B = np.where(new_column_base <= 0, 0, column_B)
        new_column_base = np.where(column_B <= 0, 1, new_column_base)

    # Divide a coluna B pela nova coluna base
    division = column_B / new_column_base  # Divide column B by new column
    lowest = max(division)  # get some term of array
    lowest_index = 0
    for index, i in enumerate(division):
        # Pega o menor valor e seu índice, após as divisão entre as colunas
        if i > 0:  # Se for 0, não pode ser o pivo
            if i < lowest:
                lowest = i
                lowest_index = index

    pivot_row = lowest_index
    pivot_col = index_new_column

    matrix, pivot = matrix_scaling(matrix, pivot_row, pivot_col)
    return matrix, pivot


def identity_matrix(matrix, matrix_restrictions, vetor_b, vetor_c):
    num_restrictions = len(matrix) - 1
    matrix_identify = np.identity(num_restrictions, dtype=float)
    matrix_normalizeted_aux = []

    for i in range(num_restrictions):
        # Make the matrix normalized, to apply simples
        row_normalized = np.append(matrix_restrictions[i], matrix_identify[i])
        row_normalized = np.append(row_normalized, vetor_b[i])
        matrix_normalizeted_aux.append(row_normalized)

    # Add the last row in the matrix. Object function row.
    aux_vector_zeros = np.zeros(num_restrictions)
    row_normalized = np.append(vetor_c, aux_vector_zeros)
    matrix_normalizeted_aux.append(row_normalized)

    final_matrix = []
    cont = 0
    aux = []
    for i in range(len(matrix_normalizeted_aux)):
        for j in range(len(matrix_normalizeted_aux[0])):
            if cont == len(matrix_normalizeted_aux[0]) - 1:
                aux.append(matrix_normalizeted_aux[i][j])
                final_matrix.append(aux)
                cont = 0
                aux = []
            else:
                aux.append(matrix_normalizeted_aux[i][j])
                cont += 1
    return final_matrix


def search_var_values(matrix, is_max):
    variables = 'abcdefghijklmnopqrstuvwxyz'
    aux = int(len(matrix[0]) - 1)
    variables = variables[:aux]  # get the variables values
    result = ''
    for i in range(len(matrix[0]) - 1):
        if matrix[-1][i] == 0: # if int the last row, the index value is 0

            pivot = np.where(matrix[:, i] > 0)
            pivot_index = pivot[0][0]
            if matrix[pivot_index][i] < 1:# if pivot <= 1. Need to get pivot == 1
                aux = 1 - matrix[pivot_index][i]

                num_inteiro = matrix[pivot_index][i] + aux
                (1 / aux) * matrix[pivot_index][-1]

                result += str(num_inteiro) + variables[i] + ' = ' + str(
                    (1 / matrix[pivot_index][i]) * matrix[pivot_index][-1]) + '\n'
            else:
                result += str(matrix[pivot_index][i]) + variables[i] + ' = ' + str(matrix[pivot_index][-1]) + '\n'

        else:
            result += str(variables[i] + ' = 0\n')
    if is_max:
        func_z = matrix[-1][-1] * -1
        result += 'A melhor solução de Z: ' + str(func_z)
    else:
        result += 'A melhor solução de Z: ' + str(matrix[-1][-1])

    result += '\n\nOBS: Caso queira executar outro problema, feche está aba e execute novamente o programa.'
    # result += 'A melhor solução de Z: ' + str(matrix[-1][-1])
    return result


def search_better(matrix, is_max, start=True):
    global pivot_vector

    if start == True:
        # If beginning of algorithm
        matrix = np.array(matrix)
        matrix = matrix.astype('float')

        matrix = np.array(identity_matrix(matrix, matrix[:-1][:, :-1], matrix[:-1][:, -1], matrix[-1]))

    bigger_value = max(matrix[-1][:])  # get the highest value of last row
    if bigger_value >= 1:
        index_highest_value = np.argmax(matrix[-1][:-1])  # get the index of the highest column C value
        matrix, pivot = change_base_column(matrix, index_highest_value)
        pivot_vector.append(pivot)
        return search_better(matrix, is_max, start=False)

    else:
        for i in pivot_vector:
            matrix = matrix / i

        aux3 = search_var_values(matrix, is_max)

    return aux3
