def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def rotate(matrix, clockwise=True):
    if clockwise:
        return [list(reversed(row)) for row in transpose(matrix)]
    else:
        return list(reversed(transpose(matrix)))

