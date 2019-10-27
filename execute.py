import subprocess;
import multiprocessing as mp;


def function(name):
	subprocess.call(name);

def multi(list):
	p = mp.Pool(mp.cpu_count());
	p.map(function,list);
	p.close();

if __name__ == "__main__":

	first = ["CI", "NI", "PI"];
	last = ["HS", "MS", "LS"]
	list = [];

	for f, l in zip(first, last):
		list.append(["java -jar NSGAII-main.jar" + f + l]); 									
		
	multi(list);
	