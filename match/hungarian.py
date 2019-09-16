from typing import List, Dict, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment

from .score import score_exponential


def _build_score_matrix(
        agents: List[str],
        tasks: List[str],
        prefs: Dict[str, List[str]],
        score_fn=score_exponential,
) -> np.ndarray:
    """Build a cost matrix of assigning agents to tasks based on preferences

    Args:
        agents: list of agents
        tasks: list of tasks
        prefs: dictionary of preference lists, keyed by agent
        score_fn: scoring function

    Returns:
        np.ndarray: score matrix
    """
    assert(len(agents) == len(tasks))

    n = len(agents)
    cost_matrix = np.zeros((n, n))

    for agent in agents:
        agent_prefs = prefs[agent]
        for task in tasks:
            i = agents.index(agent)
            j = tasks.index(task)
            cost_matrix[i, j] = score_fn(task, agent_prefs)

    return cost_matrix


def _score_to_cost_matrix(score_matrix: np.ndarray) -> np.ndarray:
    """Converts score matrix to cost matrix

    Args:
        score_matrix: score matrix

    Returns:
        np.ndarray: cost matrix
    """
    return np.max(score_matrix) - score_matrix


def solve(
        w_prefs: Dict[str, List[str]],
        m_prefs: Dict[str, List[str]],
        score_fn=score_exponential,
        weight: float = 0.5
) -> Tuple[Dict[str, str], float]:
    """Solve matching women and men together based on scoring from their preferences

    Args:
        w_prefs: preference lists of the women
        m_prefs: preference lists of th men
        score_fn: scoring function
        weight: float in the range [0.0, 1.0] that shows how much weight to assign to the women's preferences
    """
    women = list(w_prefs.keys())
    men = list(m_prefs.keys())

    w_score_matrix = _build_score_matrix(women, men, w_prefs, score_fn=score_fn)
    # Have to take the transpose to make sure the proper entries line up
    m_score_matrix = _build_score_matrix(men, women, m_prefs, score_fn=score_fn).T

    score_matrix = weight * w_score_matrix + (1 - weight) * m_score_matrix

    # Convert score matrix into cost matrix (minimize cost -> maximize score)
    cost_matrix = _score_to_cost_matrix(score_matrix)

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Build matches dict
    score = 0.0
    matches = {}
    for r, c in zip(row_ind, col_ind):
        score += score_matrix[r][c]
        matches[women[r]] = men[c]

    return matches, score
