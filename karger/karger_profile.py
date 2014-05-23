import profile 
from karger import read_input, montecarlo_karger

pr = profile.Profile() 
for i in range(5): 
  print pr.calibrate(10000) 

G, edges = read_input(open('kargerMinCut.txt', 'r'))

n = len(G)
    
profile.run('montecarlo_karger(G, edges, n)', 'karger_profile.txt')   