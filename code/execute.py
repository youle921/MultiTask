import subprocess
import multiprocessing as mp
import itertools

def function(name):
	subprocess.call(name)

def multi(l):
	p = mp.Pool(mp.cpu_count())
	p.map(function, l)
	p.close()

if __name__ == "__main__":

    names = [f + l for f in ["CI", "PI", "NI"] for l in ["HS", "MS", "LS"]]

    interval = ["1"]
    size = ["30"]
    migration_operator = ["Random", "Shortest"]
    mating_operator = ["Random", "Neighbor"]

    args1 = [["java", "-jar", "island_shortnote_200gen.jar"] \
            + list(elem) for elem in itertools.product(names, interval, size, migration_operator, mating_operator)]

    multi(args1)
    
    args2 = [["java", "-jar", "island_shortnote_500gen.jar"] \
            + list(elem) for elem in itertools.product(names, interval, size, migration_operator, mating_operator)]

    multi(args2)