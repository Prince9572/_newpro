# Experiment: Sudoku Solver using Backtracking
# Question: Solve Sudoku using backtracking and forward-checking.
# Preferably in Python.

board = [
[3,0,6,5,0,8,4,0,0],
[5,2,0,0,0,0,0,0,0],
[0,8,7,0,0,0,0,3,1],
[0,0,3,0,1,0,0,8,0],
[9,0,0,8,6,3,0,0,5],
[0,5,0,0,9,0,6,0,0],
[1,3,0,0,0,0,2,5,0],
[0,0,0,0,0,0,0,7,4],
[0,0,5,2,0,6,3,0,0]
]

def valid(r,c,n):
    for i in range(9):
        if board[r][i]==n or board[i][c]==n:
            return False
    sr,sc=3*(r//3),3*(c//3)
    for i in range(sr,sr+3):
        for j in range(sc,sc+3):
            if board[i][j]==n:
                return False
    return True

def solve():
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                for n in range(1,10):
                    if valid(i,j,n):
                        board[i][j]=n
                        if solve():
                            return True
                        board[i][j]=0
                return False
    return True

solve()

for row in board:
    print(*row)