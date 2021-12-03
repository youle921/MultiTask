import numpy as np
import matplotlib.pyplot as plt

import pathlib

names = ["NSGA-II_tracing/1119"]
names.extend([f'{alg}_tracing/1109' for alg in ["MO-MFEA", "MO-MFEA-II"]])
names.extend([f'{alg}_tracing/1117' for alg in ["EMEA", "Island_Model"]])


probs = pathlib.Path(names[-1]).glob("*design/")
prob_name = [p.stem for p in probs]
plain_name = [n.split("_")[1] for n in prob_name]

# %%
plt.rcParams["font.size"] = 9

for n, pname in zip(plain_name, prob_name):

    fig = plt.figure(figsize = (9, 4.5 + 1/16))

    for i, alg in enumerate(names):

        if "NSGA-II" in alg:
            ratio = np.loadtxt(f'{alg}/{n}/trial1_trace_log.csv', delimiter = ",")[:49]
        else:
            ratio = np.loadtxt(f'{alg}/{pname}/trial1_trace_log.csv', delimiter = ",")[:49]

        ratio = np.array([np.sum(ratio == status, axis = 1) for status in range(4)])

        ax = fig.add_subplot(2, 3, i + 1)
        ax.stackplot(np.arange(2, 51), ratio)
        ax.set_title(alg.split("/")[0].split("_tracing")[0])

    fig.suptitle(n, fontsize = 13)
    fig.tight_layout()

    fig.savefig(f'{n}_trace_log.svg')