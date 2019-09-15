from scipy.optimize import linear_sum_assignment
import numpy as np
from .score import score_exponential


def _build_score_matrix(tasks, prefs, score_fn=score_exponential):
    '''Build a cost matrix of assigning agents to tasks based on preferences'''
    agents = list(prefs.keys())
    assert(len(agents) == len(tasks))

    n = len(agents)
    cost_matrix = np.zeros((n, n))

    for agent in agents:
        agent_prefs = prefs[agent]
        for task in tasks:
            i = agents.index(agent)
            j = tasks.index(task)
            cost_matrix[i, j] = score_fn(task, agent_prefs)

    return agents, tasks, cost_matrix


def _score_to_cost_matrix(cost_matrix):
    return np.max(cost_matrix) - cost_matrix


def solve(w_prefs, m_prefs, w_weight=0.5, m_weight=0.5):
    '''Solve matching women and men together based on scoring from their preferences'''
    women = list(w_prefs.keys())
    men = list(m_prefs.keys())

    w_score_matrix = _build_score_matrix(men, w_prefs)
    m_score_matrix = _build_score_matrix(women, m_prefs)

    score_matrix = w_weight * w_score_matrix + m_weight * m_score_matrix

    # Convert score matrix into cost matrix (minimize cost -> maximize score)
    cost_matrix = _score_to_cost_matrix(score_matrix)

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Build matches dict
    matches = {}
    for r, c in zip(row_ind, col_ind):
        matches[women[r]] = men[c]

    return matches

