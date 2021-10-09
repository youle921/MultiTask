# -*- coding: utf-8 -*-
import numpy as np
from . import RE21, RE22, RE23, RE24, RE25, RE31, RE32, RE33, RE34, RE35, RE36, RE37, RE41, RE42, RE61, RE91
from ...base_class.base_problem_set import problem_set

all_probs = [RE21.RE21(), RE22.RE22(), RE23.RE23(), RE24.RE24(), RE25.RE25(), RE31.RE31(), RE32.RE32(), RE33.RE33(),
             RE34.RE34(), RE35.RE35(), RE36.RE36(), RE37.RE37(), RE41.RE41(), RE42.RE42(), RE61.RE61(), RE91.RE91()]


def get_prob_pairs(prob_list=None):

    if prob_list is None:
        p = np.array(all_probs).reshape(-1, 2).tolist()
    else:
        p = np.array(prob_list).reshape(-1, 2).tolist()

    p_set = [problem_set(t) for t in p]
    for i, ps in enumerate(p_set):
        ps.problem_name = f'problem set{i + 1}'

    return p_set


def get_random_prob_pairs(prob_list):
    np.random.shuffle(prob_list)
    return get_prob_pairs(prob_list)
