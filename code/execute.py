import subprocess
import multiprocessing as mp
import itertools

def function(name):
	subprocess.call(name)

def multi(l):
	p = mp.Pool(mp.cpu_count() - 2)
	p.map(function, l)
	p.close()

if __name__ == "__main__":

    alg = ["MOMFEA", "NSGAII"]
#    problems = ["bitflip", "scaling", "profitflip"]
    problems = ["scaling"]
    
    sr = ["1.01", "1.02", "1.03", "1.04", "1.06", "1.07", "1.08", "1.09"]
#    fr = ["0.25", "0.2", "0.15", "0.1", "0.05"]
#    pfr = ["0.05", "0.1", "0.15", "0.2", "0.25"]
    # params = [sr, fr, pfr]
    params = [sr]

    interval = ["5"]
    size = ["10"]
    island_params = [[i, s] for i in interval for s in size]
    
    args = []

    for i, p in enumerate(problems):
        tmp = [["java", "-jar", "NSGAII-island_for_Knapsack.jar", p , param] for param in params[i]]
        args.extend([t + list(elem) for t in tmp for elem in island_params])
    
    for a in alg:
        for i, p in enumerate(problems):
            args.extend([["java", "-jar", a + "_for_Knapsack.jar", p , param] for param in params[i]])
            
    for i in range(len(args)):
        args[i].insert(5, "31")
    multi(args)