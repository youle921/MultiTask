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

    interval = ["5", "10"]
    size = ["10", "20"]

    args = [["java", "-jar", "NSGAII-main.jar"] \
            + list(elem) for elem in itertools.product(names, interval, size)]

    multi(args)