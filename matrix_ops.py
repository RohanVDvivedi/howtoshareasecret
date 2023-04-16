'''
    This code file is taken from https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
    And then it is modified to be used with this project.
'''

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m, integral_inverse = False):
    determinant = getMatrixDeternminant(m)

    # can not find inverse if determinant is 0
    if(determinant == 0) :
        return (0, False)

    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)

    # find adjoint
    adjoint = transposeMatrix(cofactors)

    # find inverse
    inverse = adjoint
    for r in range(len(adjoint)):
        for c in range(len(inverse)):
            inverse[r][c] = (inverse[r][c] // determinant) if integral_inverse else (inverse[r][c] / determinant)

    # return inverse
    return inverse

def getMatrixMultiplication(X, Y) :
    result = [ [0] * len(Y[0]) ] * len(X)
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result