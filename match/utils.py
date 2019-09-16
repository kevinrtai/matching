from typing import Dict, List, Tuple, Set

import numpy as np


def complete(
        w_prefs: Dict[str, List[str]],
        m_prefs: Dict[str, List[str]],
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Given two incomplete preference dicts, complete them with a random permutation of the remaining choices

    Args:
        w_prefs: map from woman name to ordered list of preferences
        m_prefs: map from man name to ordered list of preferences

    Returns:
        Tuple of completed preference dicts
    """
    women = set(w_prefs.keys())
    men = set(m_prefs.keys())

    w_prefs_c = {w: complete_prefs(w_prefs[w], men) for w in w_prefs}
    m_prefs_c = {m: complete_prefs(m_prefs[m], women) for m in m_prefs}

    return w_prefs_c, m_prefs_c


def complete_prefs(prefs: List[str], choices: Set[str]) -> List[str]:
    """Given a single preference list, return a completed preference list with a permutation or the remaining choices

    Args:
        prefs: incomplete map from person to ordered list of preferences
        choices: complete set of possible choices for the person

    Returns:
        Completed preference dict
    """
    remaining_choices = list(set(choices) - set(prefs))
    return prefs + list(np.random.permutation(remaining_choices).tolist())
