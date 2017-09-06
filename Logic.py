import Data as BigData

board = BigData.board

def isGraphOk(board):
    ''' this function checks if the graph is well formed, (only used once) '''
    for vertex in board:                         # go over all the vertexes
        for neighbor in board[vertex]:           # go over my neighbors
            if vertex not in board[neighbor]:    # if im not my neighbor's neighbor
                print vertex, neighbor

    return True

def vertexPartOfTriangle(vertex):
    ''' this function gets a vertex and returns a list of all the triangles he is a part of'''
    triangles = []
    for neighbor in board[vertex]:             # go over all the vertex's neighbors
        for neighbor2 in board[neighbor]:      # go over all the neighbor's neighbors
            if neighbor2 in board[vertex]:     # check if the neighbor's neighbor is a neighbor of the origianl vertex
                if sorted([vertex, neighbor, neighbor2]) not in triangles:           # prevent duplicates
                    triangles.append(sorted([vertex, neighbor, neighbor2]))

    return triangles

def isNeighbors(vertex1, vertex2):
    ''' this function gets two vertexes and returns if the two vertexes are neighbors '''
    if vertex2[0] == -1:
        return False
    for i in board[vertex1]:
        if i == vertex2:
            return True
    return False