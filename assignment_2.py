import numpy as np

def nevilles_method(x_points, y_points, x):
    # must specify the matrix size (this is based on how many columns/rows you want)
    matrix = np.zeros((3, 3))
    # fill in value (just the y values because we already have x set)
    for counter, row in enumerate(matrix):
        row[0] = y_points[counter]
    # the end of the first loop are how many columns you have...
    num_of_points = 3
    # populate final matrix (this is the iterative version of the recursion explained in class)
    # the end of the second loop is based on the first loop...
    for i in range(1, num_of_points):
        for j in range(1, i+1):
            first_multiplication = (x - x_points[i]) * matrix[i][j-1]
            second_multiplication = (x - x_points[i-1]) * matrix[i-1][j-1]
            denominator = x_points[i] - x_points[i-1]
            # this is the value that we will find in the matrix
            coefficient = (first_multiplication - second_multiplication) / denominator
            matrix[i][j] = coefficient
    
    return None
if __name__ == "__main__":
    # point setup
    x_points = [3.6, 3.8, 3.9]
    y_points = [1.675, 1.436, 1.318]
    approximating_value = 3.7
    nevilles_method(x_points, y_points, approximating_value)