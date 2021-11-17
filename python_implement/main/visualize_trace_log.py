import numpy as np
import matplotlib.pyplot as plt

import pathlib

names = [f'{alg}_tracing/1109' for alg in ["MO-MFEA", "MO-MFEA-II"]]
names.extend([f'{alg}_tracing/1117' for alg in ["EMEA", "Island_Model"]])

probs = pathlib.Path(names[0]).glob("*design/")
prob_name = [p.stem for p in probs]
plain_name = [n.split("_")[1] for n in prob_name]

plt.rcParams["font.size"] = 8

for n, pname in zip(plain_name, prob_name):

    fig = plt.figure()

    for i, alg in enumerate(names):

        ratio = np.loadtxt(f'{alg}/{pname}/trial1_trace_log.csv', delimiter = ",")[:49]

        ratio = np.array([np.sum(ratio == status, axis = 1) for status in range(4)])
        if(alg == "EMEA_tracing/1109"):
            print(ratio)

        ax = fig.add_subplot(2, 2, i + 1)
        ax.stackplot(np.arange(2, 51), ratio)
        ax.set_title(alg.split("/")[0].split("_tracing")[0])

    fig.suptitle(n, fontsize = 13)
    fig.tight_layout()

    fig.savefig(f'{n}_trace_log.svg')