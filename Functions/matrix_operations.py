# Matrices and their related operations
# treats matrices as a list of lists

from helper_functions import is_even

def matrix_shape(matrix=list):
    # used to get the shape of a matrix that is either stored as a list or list of lists
    # returns a tuple of two integers representing rows and columns, respectively
    if type(matrix[0]) == list:
        # when the matrix is a list of lists, it has multiple rows
        rows = len(matrix)
        cols = len(matrix[0])
        # make sure all rows in each matrix are the same size (columns consistent) since the matrices are just represented with lists of lists
        for row in matrix:
            assert len(row) == cols, "Matrix is not consistent in it's number of columns in each row."
    else:
        # when the matrix is just a list, it has one row with columns equal to its length
        rows = 1
        cols = len(matrix)
    return (rows, cols)

def create_zeroed_matrix(rows=int, cols=int):
    zeroed_matrix = []
    for row in range(rows):
        row = [0]*cols
        zeroed_matrix.append(row)
    return zeroed_matrix

def transpose_matrix(matrix=list):
    # this function swaps the columns and rows in a matrix
    # it was created specifically for the case when a matrix with 1 column is represented a simple list of elements rather than list of lists of a single element
    rows, cols = matrix_shape(matrix)
    if rows == 1:
        transposed_matrix = []
        for item in matrix:
            transposed_matrix.append([item])
    else:
        transposed_matrix = create_zeroed_matrix(cols, rows)
        for row in range(rows):
            new_col = row         
            for col in range(cols):
                new_row = col
                item = matrix[row][col]
                transposed_matrix[new_row][new_col] = item
    return transposed_matrix

def condense_single_col_matrix(matrix=list):
    # used to make a matrix with only one column represented by a single list of elements, instead of list of lists of single elements
    rows, cols = matrix_shape(matrix)
    assert cols == 1, "Matrix has more than one column and cannot be condensed into a single list."
    new_matrix = []
    for row in range(rows):
        new_matrix.append(matrix[row][0])
    return new_matrix

def matrix_multiplication(matrix1=list, matrix2=list):
    # specifically multiplies matrices of binary and returns binary product
    # get matrix shapes
    m1_rows, m1_cols = matrix_shape(matrix1)
    m2_rows, m2_cols = matrix_shape(matrix2)
    # transpose if one of the matrices has rows = 1
    # this is because matrices that are just a list of elements (not a list of lists) cannot be interpreted by this code
    if m1_rows == 1:
        matrix1 = transpose_matrix(matrix1)
        m1_rows, m1_cols = matrix_shape(matrix1)
    if m2_rows == 1:
        matrix2 = transpose_matrix(matrix2)
        m2_rows, m2_cols = matrix_shape(matrix2)
    # check if matrix shapes are eligible for multiplication
    # the number of columns in the first matrix must be equal to the number of rows in the second matrix
    assert m1_cols == m2_rows, f"Matrices cannot be multiplied due to their shapes. \nMatrix 1: {m1_rows}r x {m1_cols}c \nMatrix 2: {m2_rows}r x {m2_cols}c "
    # create new matrix for product; it will be of shape m1_rows x m2_cols
    # right now it is filled with zeros as place holders
    prod_rows, prod_cols = m1_rows, m2_cols
    product = create_zeroed_matrix(prod_rows, prod_cols)
    # multiply the columns in matrix 1 by the rows in matrix 2 and insert into the correct spot in the product
    for ii in range(m1_rows):
        for jj in range(m2_cols):
            for kk in range(m1_cols):
                product[ii][jj] += matrix1[ii][kk] * matrix2[kk][jj]
    # return each item in the product to binary
    for row in range(prod_rows):
        for column in range(prod_cols):
            item = product[row][column]
            if is_even(item):
                product[row][column] = 0
            else:
                product[row][column] = 1
    if prod_cols == 1:
        product = condense_single_col_matrix(product)
    return product