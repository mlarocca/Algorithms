'''
Created on 15/dic/2012

@author: mlarocca
'''

# CHALLENGE PROBLEM: 
#
# Use your check_sudoku function as the basis for solve_sudoku(): a
# function that takes a partially-completed Sudoku grid and replaces
# each 0 cell with an integer in the range 1..9 in such a way that the
# final grid is valid.
#
# There are many ways to cleverly solve a partially-completed Sudoku
# puzzle, but a brute-force recursive solution with backtracking is a
# perfectly good option. The solver should return None for broken
# input, False for inputs that have no valid solutions, and a valid
# 9x9 Sudoku grid containing no 0 elements otherwise. In general, a
# partially-completed Sudoku grid does not have a unique solution. You
# should just return some member of the set of solutions.
#

'''Checks if the grid is a valid sudoku (partial) solution
   ASSUMES that the grid is well formed
   Checks ONLY the distribution of the values inside a valid grid
   DO NOT check that all values are valid (for performance reasons it is checked 
   only once when the input is read)
   @param grid: The grid to be checked
   @return:  True <=> the grid is a valid (possibly partial) solution
             False <-> Otherwise
'''
def check_sudoku(grid):
        
    #checks rows and cols values
    row_i = {}   
    col_i = {}
    for i in xrange(9):
        row_i.clear()
        col_i.clear()
        for j in xrange(9):
            #For every values it gets on the grid,
            #Increments a counter that keeps track
            #Of how many times that value appear in the ith col and row
            try:
                row_i[grid[i][j]] += 1
            except KeyError:
                row_i[grid[i][j]] = 1
            try:
                col_i[grid[j][i]] += 1
            except KeyError:
                col_i[grid[j][i]] = 1               
        #Discards values relative to zeros (wildcards)
        try:
            del row_i[0]
        except KeyError:
            pass
        try:
            del col_i[0]
        except KeyError:
            pass
        
        #If any value (excluding 0) appears more than once in a single
        #row or column, then the sudoku assignment isn't valid
        row_i_v = row_i.values()
        col_i_v = col_i.values()
        if ((len(row_i_v) > 0 and max(row_i_v) > 1) or 
            (len(col_i_v) > 0 and max(col_i_v) > 1)):
            return False
    
    #now checks the 3x3 cells
    
    cell = {}
    for cell_row in xrange(3):
        for cell_col in xrange(3):
            #For each cell...
            cell.clear()
            for row in xrange(3 * cell_row, 3 * (cell_row + 1)):
                for col in xrange(3 * cell_col, 3 * (cell_col + 1)):
                    #...for each value found in a single cell
                    #Increments a counter that keeps track
                    #Of how many times that value appear in the cell
                    try:
                        cell[grid[row][col]] += 1
                    except KeyError:
                        cell[grid[row][col]] = 1
            #Discards values relative to zeros (wildcards)
            try:
                del cell[0]
            except KeyError:
                pass
            
            #If any value (excluding 0) appears more than once in a single
            #cell, then the sudoku assignment isn't valid
            cell_v = cell.values()
            if len(cell_v) > 0 and max(cell_v) > 1:
                return False
            
    #If it has made it so far, the assignment is valid        
    return True

'''A sudoku solver function
   If the grid is well formed (any iterable containing 9 iterables each of
   which contains 9 integers between 0 and 9 included is accepted as valid)
   and if it is a valid partial solution for the sudoku puzzle,
   it tries to solve it, if possible. 

   @param grid: The grid representing the specific sudoku puzzle to solve;
   @return:  The grid properly filled <=> The grid is properly formatted and 
                                          the puzzle is solvable
             False <=> The grid is properly formatted but there is no
                       solution to the puzzle
             None <=>  The grid violates the sudoku contraints
                       (wrong size or wrong types or values)
'''
def solve_sudoku(grid):

   

    ''' For a partial solution grid and a cell (the cell at the
        crossing of ith row and jth column) enumerates all the possible
        values that can be assigned to that cell;
        @param grid:  A partial solution grid
        @param i:  Row of the cell under evaluation
        @param j: Column of the cell under evaluation
        @return: A list of the possible values for the cell.        
    '''
    def get_valid_values_for_cell(grid, i, j):
        valid_values = {i : 0 for i in xrange(10) }  #Initially, 1 to 9 are supposed to be valid
        for k in xrange(9):
            #For every values it gets on the grid,
            #removes it from the valid ones, if it's still included

            valid_values[grid[i][k]] = 1
            valid_values[grid[k][j]] = 1

        #Now checks the 3x3 cell
        cell_i = i - i%3
        cell_j = j - j%3
        for i in xrange(cell_i, cell_i + 3):
            for j in xrange(cell_j, cell_j + 3):
                valid_values[grid[i][j]] = 1

        #If the call is issued correctly grid[i][j] == 0 and therefore valid_values[0] == 1 => 0 in valid_values
        del valid_values[0]

        return [k for (k,v) in valid_values.items() if v == 0]
    
    ''' Given a partial solution grid and the list of its unassigned cells
        chooses the next move (i.e. the next cell to be assigned a value)
        according to the most constrained one first criterium
        
        @param grid:  A partial solution grid
        @param free_cells:  A list of the free cells remaining in the grid
        @return: A couple containing:
                 - The list of possible values that can be assigned to the chosen cell
                 - A couple of indices for row and column of the chosen cell
    '''
    def pick_next_move(grid, free_cells):
        best_choice_len = float("inf")
        
        for (i,j) in free_cells:
            values = get_valid_values_for_cell(grid, i, j)
            n = len(values)
            if n == 0:
                return None, (None, None)    #This cell has no possible choice, so we can as well backtrack
            elif n == 1:
                #This is the most possible constrained situation
                #so we can as well choose this
                return values, (i, j)
            elif n < best_choice_len:
                best_choice_len = n
                best_choice = (values, (i,j))
        assert(best_choice)
        return best_choice
        
            
    ''' Given a partial solution grid and the list of its unassigned cells
        tries to solve the puzzle by choosing the best possible next cell
        to assign a value to and then trying to assign it all the possible
        values, for each one recursively calls itself in a DFS search.
        
        @param grid:  A partial solution grid
        @param free_cells:  A list of the free cells remaining in the grid
        @return:  The grid properly filled <=> The grid is properly formatted and 
                                                the puzzle is solvable
                  False <=> The grid is properly formatted but there is no
                             solution to the puzzle
    '''    
    def recursive_solver(grid, free_cells):
        #Grid completed
        if len(free_cells) == 0:
          assert(check_sudoku(grid))
          return grid

            
        #looks for the best next move
        values, (i,j) = pick_next_move(grid, free_cells)
        if values is None:
            return False    #Must backtrack
        #else
        free_cells.remove((i,j))
        #free cell!
        
        for val in values:
            grid[i][j] = val
            sol = recursive_solver(grid, free_cells[:])
            if sol != False:
                return sol
        
        #If none of the attempted substitution worked, then must backtrack
        grid[i][j] = 0
        return False
      
    ''' solve_sudoku BODY '''  
    #checks that the grid is well formed
    try:
        rows = len(grid)
    except TypeError:
        return None
 
    if rows != 9:
        return None
            
    free_cells = []
    for i in xrange(9): #INVARIANT: assert(len(grid) == 9)
        #check that the single rows are well formed
        try:
            cols = len(grid[i])
        except TypeError:
            return None
    
        if cols != 9:
            return None 
                  
        for j in xrange(9): #INVARIANT: assert(len(grid[i]) == 9)
            val = grid[i][j]
            if val == 0:
                free_cells.append((i,j))
            elif type(val) != int or val < 0 or val > 9:
                #The cell contains an invalid value
                return None
              
    check = check_sudoku(grid)
    if check != True:
        return False    #The input is already an invalid solution    
    #else, try to solve the puzzle      
    return recursive_solver(grid, free_cells)