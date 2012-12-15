'''
Created on 15/dic/2012

@author: mlarocca
'''

from sudoku_solver import *

# solve_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

ill_formed_2 = [(5,3,4,6,7,8,9,1,2),
                [6,"7",2,1,9,5,3,4,8],
                [1,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,10],  # <---
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return valid unchanged
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return False
invalid_2 =  [[1,0,0,0,0,7,0,9,0],
              [0,3,0,0,2,0,0,0,8],
              [0,0,3,6,0,0,5,0,0],
              [0,0,5,3,0,0,9,0,0],
              [0,1,0,0,8,0,0,0,2],
              [6,0,0,0,0,4,0,0,0],
              [3,0,0,0,0,0,0,1,0],
              [0,4,0,0,0,0,0,0,7],
              [0,0,7,0,0,0,3,0,0]]


# solve_sudoku should return a 
# sudoku grid which passes a 
# sudoku checker. There may be
# multiple correct grids which 
# can be made from this starting 
# grid.
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# Note: this may timeout 
# in the Udacity IDE! Try running 
# it locally if you'd like to test 
# your solution with it.
# 
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

super_hard = [[0,0,3,0,0,5,4,1,0],
        [0,0,0,1,0,0,0,8,5],
        [0,0,0,3,0,0,6,0,0],
        [0,0,0,0,3,0,0,6,0],
        [2,0,0,7,0,9,0,0,8],
        [0,6,0,0,5,0,0,0,0],
        [0,0,8,0,0,3,0,0,0],
        [9,3,0,0,0,6,0,0,0],
        [0,5,7,4,0,0,9,0,0]]

blank = [[0]*9 for i in xrange(9)]

print solve_sudoku(ill_formed) # --> None
print solve_sudoku(ill_formed_2) # --> None
print solve_sudoku(3) # --> None
print solve_sudoku([3]) # --> None
print solve_sudoku([3 for i in xrange(9)]) # --> None
print solve_sudoku(valid)      
print solve_sudoku(invalid)    # --> False
print solve_sudoku(invalid_2)    # --> False
print solve_sudoku(easy)      
print solve_sudoku(hard)       
print solve_sudoku(super_hard)
print solve_sudoku(blank) #edge case