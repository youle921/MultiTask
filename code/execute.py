import subprocess
import multiprocessing as mp

def function(name):
	subprocess.call(name)

def multi(l):
	p = mp.Pool(mp.cpu_count())
	p.map(function, l)
	p.close()

if __name__ == "__main__":

    first = ["CI", "PI", "NI"]
    last = ["HS", "MS", "LS"]
    namelist = []
    names = [f + l for f in first for l in last]

    for n in names:
        namelist.append(["java", "-jar", "NSGAII-main.jar", n])

    multi(namelist)