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
            first_multiplication = (x - x_points[i]) * matrix[i-1][j-1]
            second_multiplication = (x - x_points[i-j]) * matrix[i][j-1]
            denominator = x_points[i] - x_points[i-j]
            # this is the value that we will find in the matrix
            coefficient = (second_multiplication - first_multiplication) / denominator
            matrix[i][j] = coefficient
    
    return matrix

def divided_difference_table(x_points, y_points):
    # set up the matrix
    size: int = (4, 4)
    matrix: np.array = np.zeros(size)
    # fill the matrix
    for index, row in enumerate(matrix):
        row[0] = y_points[index]
    # populate the matrix (end points are based on matrix size and max operations we're using)
    for i in range(1, size[0]):
        for j in range(1, i+1):
            # the numerator are the immediate left and diagonal left indices...
            numerator = matrix[i][j-1] - matrix[i-1][j-1]
            # the denominator is the X-SPAN...
            denominator = x_points[i] - x_points[i-j]
            operation = numerator / denominator
            # cut it off to view it more simpler
            matrix[i][j] = '{0:.7g}'.format(operation)
    return matrix

def get_approximate_result(matrix, x_points, value):
    # p0 is always y0 and we use a reoccuring x to avoid having to recalculate x 
    reoccuring_x_span = 1
    reoccuring_px_result = matrix[0][0]

    # we only need the diagonals...and that starts at the first row...
    for index in range(1, 4):
        polynomial_coefficient = matrix[index][index]
        # we use the previous index for x_points....
        reoccuring_x_span *= (value - x_points[index-1])
        # get a_of_x * the x_span
        mult_operation = polynomial_coefficient * reoccuring_x_span
        # add the reoccuring px result
        reoccuring_px_result = mult_operation + reoccuring_px_result

    
    # final result
    return reoccuring_px_result

np.set_printoptions(precision=7, suppress=True, linewidth=100)
def apply_div_dif(matrix: np.array):
    size = len(matrix)
    for i in range(2, size):
        for j in range(2, i+2):
            # skip if value is prefilled (we dont want to accidentally recalculate...)
            if j >= len(matrix[i]) or matrix[i][j] != 0:
                continue
            
            # get left cell entry
            left: float = matrix[i][j-1]
            # get diagonal left entry
            diagonal_left: float = matrix[i-1][j-1]
            # order of numerator is SPECIFIC.
            numerator: float = left - diagonal_left
            # denominator is current i's x_val minus the starting i's x_val....
            denominator = matrix[i][0] - matrix[i-j+1][0]
            # something save into matrix
            operation = numerator / denominator
            matrix[i][j] = operation
    
    return matrix

def hermite_interpolation():
    x_points = [3.6, 3.8, 3.9]
    y_points = [1.675, 1.436, 1.318]
    slopes = [-1.195, -1.188, -1.182]
    # matrix size changes because of "doubling" up info for hermite 
    num_of_points = len(x_points)*2
    matrix = np.zeros((6, 6))
    # populate x values (make sure to fill every TWO rows)
    for x in range(0, num_of_points):
        matrix[x][0] = x_points[x//2]
    
    # prepopulate y values (make sure to fill every TWO rows)
    for x in range(0, num_of_points):
        matrix[x][1] = y_points[x//2]

    # prepopulate with derivates (make sure to fill every TWO rows. starting row CHANGES.)
    for x in range(0, num_of_points):
        if x == 0:
            matrix[x][2] = 0.0
        elif x%2 == 1:
            matrix[x][2] = slopes[x//2]
        else:
            matrix[x][2] = (matrix[x][1] - matrix[x-1][1]) / (matrix[x][0] - matrix[x-1][0])

    filled_matrix = apply_div_dif(matrix)
    print(filled_matrix)

if __name__ == "__main__":
    # point setup
    x_points = [3.6, 3.8, 3.9]
    y_points = [1.675, 1.436, 1.318]
    approximating_value = 3.7
    matrix = nevilles_method(x_points, y_points, approximating_value)
    print(matrix[2][2])
    print()

    # point setup
    x_points = [7.2, 7.4, 7.5, 7.6]
    y_points = [23.5492, 25.3913, 26.8224, 27.4589]
    divided_table = divided_difference_table(x_points, y_points)
    approximations = [divided_table[1,1], divided_table[2,2], divided_table[3,3]]
    print(approximations)
    print()
    # find approximation
    approximating_x = 7.3
    final_approximation = get_approximate_result(divided_table, x_points, approximating_x)
    print(final_approximation)
    print()

    hermite_interpolation()
    print()

    x_points = [2, 5, 8, 10]
    y_points = [3, 5, 7, 9]
    n = 3
    h = np.zeros(n)
    a = np.array(y_points)
    for i in range(0, n):
        h[i] = x_points[i+1] - x_points[i]

    A = np.zeros((n+1, n+1))
    A[0][0] = 1
    A[n][n] = 1

    for i in range(1, n):
        A[i][i] = 2 * (h[i-1] + h[i])

    for i in range(0, n-1):
        A[i+1][i] = h[i]
    
    for i in range(1, n):
        A[i][i+1] = h[i]

    print(A)
    print()
    
    b = np.zeros(n+1)
    for i in range(1, n):
        b[i] = ((3.0/h[i]) * (a[i+1]-a[i])) - ((3.0/h[i-1]) * (a[i]-a[i-1]))

    print(b)
    print() 

    c = np.zeros(n+1)
    c[n] = 0

    l = np.zeros(n+1)
    u = np.zeros(n+1)
    z = np.zeros(n+1)

    l[0] = 1
    u[0] = 0
    z[0] = 0

    for i in range(1, n):
        l[i] = 2*(x_points[i+1] - x_points[i-1]) - (h[i-1]*u[i-1])
        u[i] = h[i]/l[i]
        z[i] = (b[i] - (h[i-1]*z[i-1]))/l[i]

    l[n] = 1
    z[n] = 0
    c[n] = 0

    for j in range(n-1, -1, -1):
        c[j] = z[j] - (u[j]*c[j+1])

    print(c)

