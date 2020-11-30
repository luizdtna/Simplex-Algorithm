# Developed by Luiz Araujo
import numpy as np


def make_matrix_test():
    matrix = np.array([
        [5.0, 10.0, 1.0, 0.0, 0.0, 100.0],
        [9.0, 6.0, 0.0, 1.0, 0.0, 108.0],
        [0.0, 1.0, 0.0, 0.0, 1.0, 8.0],
        [4000.0, 5000.0, 0.0, 0.0, 0.0, 0.0]
    ])

    matrix = np.array([
        [20,10,1,0,0,80],
        [1,1,0,-1,1,5],
        [30000,10000,0,0,0,0]
    ], dtype='float')


    matrix = np.array([
        [2,1,1,0,0,1000],
        [1,1,0,1,0,800],
        [1,0,0,0,1,700],
        [4,3,0,0,0,0]
    ], dtype='float')
    print(matrix.astype(int))
    """
    matrix = np.array([
        [10, 12, 1, 0, 60],
        [2, 1,0, 1, 6],
        [5, 2, 0, 0, 0]
    ], dtype='float')"""

    """for i in range(4):
        for j in range(6):
            print(matrix[i][j], end=' ')
            if j == 5:
                print('')"""

    return matrix


def base_matrix(num_restriction):
    columns_index_base = np.arange(2,num_restriction+2)

    #base = matrix[:,2:num_restriction+2]
    # print(index_base)
    return columns_index_base

def matrix_scaling(matrix, pivot_row, pivot_col):
    pivot = float(matrix[pivot_row][pivot_col])
    #if matrix[pivot_row][pivot_col] > 0 and matrix[pivot_row][pivot_col] < 1:
    #    first_calculation = matrix[pivot_row]+1-pivot
    #    matrix[pivot_row] = first_calculation

    if matrix[pivot_row][pivot_col] > 1: #se o pivo for maior que 1, faz opreções para que ele vire 1.
        first_calculation = np.array([i / pivot if i != 0.0 else 0 for i in matrix[pivot_row]], dtype=float)
        matrix[pivot_row] = first_calculation
        pivot = int(matrix[pivot_row][pivot_col])
        print(matrix.astype(int))
    for i in range(len(matrix)):

        if matrix[i][pivot_col] == 0: # se o termo na mesma coluna do pivor é igual a zero
            continue

        if i != pivot_row: # Se não for a linha do pivo

            first_calculation = pivot * matrix[i]
            #print(base_matrix[i])
            second_calculation = matrix[i][pivot_col] * matrix[pivot_row]
            #print(second_calculation)
            result = first_calculation - second_calculation

            matrix[i] = result # Updade the row of base matrix

    return matrix

def change_base_column(matrix,index_new_column):
    ##Aqui eu devo juntar a matriz não basica com a matriz básica

    #size_base = len(base_matrix[1])

    column_B = matrix[:,-1][:-1]
    new_column_base = matrix[:,index_new_column][:-1]

    # Esse if não tá fazendo nada
    if (np.where(new_column_base <= 0)):
        #index_testes = np.where(new_column <= 0)
        #print(index_testes)

        column_B = np.where(new_column_base <= 0, 0, column_B) # zera os termos que não vão interfir na função obj
        new_column_base = np.where(column_B <= 0, 1, new_column_base)



    # Divide a coluna B pela nova coluna base
    division = column_B / new_column_base # Divide column B by new column
    lowest = max(division) # get some term of array
    lowest_index = 0
    for index, i in enumerate(division):
        # Pega o menor valor e seu índice, após as divisão entre as colunas
        if i > 0: #Se for 0, não pode ser o pivo
            if i < lowest:
                lowest = i
                lowest_index = index

    #lowest_value_index = np.argmin(division) # division's lowest term index
    #print(lowest_value_index)



    pivot_row = lowest_index
    pivot_col = index_new_column
    matrix = matrix_scaling(matrix,pivot_row, pivot_col)
    return matrix


def search_better(matrix, columns_index_base):
    bigger_value = max(matrix[-1][:]) #Pega o maior valor da linha da função objetiva
    if bigger_value >= 1:
        index_highest_value = np.argmax(matrix[-1][:]) # get the index of the highest column C value
        matrix = change_base_column(matrix,index_highest_value)
        print(matrix.astype(int))
        search_better(matrix, columns_index_base)
    else:
        print('deu')
        print(matrix)
if __name__ == '__main__':

    matrix = make_matrix_test()
    num_restriction = 2
    columns_index_base = base_matrix(num_restriction)
    search_better(matrix, columns_index_base)

