import random
import numpy as np

# create array of size m*n, for example:
m=10
n=10
array = np.zeros((m,n))

#place bombs: 1) each cell contains a bomb with given probability, for example
p = 0.2
for i in range(1,m-1):
    for j in range(1,n-1):
        array[i][j] = (random.random() < p)
        
        
#solve the game by computing for each cell the nb of bombs contained in the 
#nearest neighboring cells
solutions = np.zeros((m,n))
for i in range(1,m-1):
    for j in range(1,n-1):
        if not(array[i][j]):
            #corresponding cell of solutions contains the nb of bombs near it
            solutions[i][j] = np.sum(array[i-1:i+2,j-1:j+2])
        else:
            #if cell contains a bomb, value will be 10 (arbitrarily)
            solutions[i][j] = 10
