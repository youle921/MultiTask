import numpy as np

def sb_mating(obj, var):

    idx = np.random.randint(0, high = obj.shape[0], size = [2])
    winner = nsgaii_tornament(idx)