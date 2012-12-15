'''
Created on 15/dic/2012

@author: mlarocca
'''
from sudoku_solver import solve_sudoku
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

if __name__ == '__main__':
  import cProfile

  cProfile.run('solve_sudoku(super_hard)', 's_profile.txt')
  
  import pstats
  p = pstats.Stats('s_profile.txt')
  p.sort_stats('time').print_stats(20)