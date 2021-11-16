import numpy as np
import matplotlib.pyplot as plt

import pathlib

names = [f'{alg}_tracing/1109' for alg in ["MO-MFEA", "MO-MFEA-II", "EMEA", "Island_Model"]]
probs = pathlib.Path(names[0]).glob("*design/")
prob_name = [p.stem for p in probs]
plain_name = [n.split("_")[1] for n in prob_name]

plt.rcParams["font.size"] = 8

for n, pname in zip(plain_name, prob_name):

    fig = plt.figure()

    for i, alg in enumerate(names):

        ratio = np.loadtxt(f'{alg}/{pname}/trial1_trace_log.csv', delimiter = ",")

        ratio = np.array([np.sum(ratio == status, axis = 1) for status in range(4)])
        if(alg == "EMEA_tracing/1109"):
            print(ratio)

        ax = fig.add_subplot(2, 2, i + 1)
        ax.stackplot(np.arange(ratio.shape[1]), ratio)
        ax.set_title(alg.split("/")[0])

    fig.suptitle(n)
    fig.tight_layout()