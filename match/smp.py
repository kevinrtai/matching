from typing import Dict, List, Set

import copy
import numpy as np


def solve(w_prefs_i: Dict[str, List[str]], m_prefs_i: Dict[str, List[str]]) -> Dict[str, str]:
    """Return a dictionary of matches, keyed by men, for the stable marriage problem

    Args:
        w_prefs_i: incomplete preference dict for the women
        m_prefs_i: incomplete preference dict for the men

    Returns:
        Dictionary containing map from woman to man
    """
    validate_input(m_prefs_i, w_prefs_i)
    
    # Make a copy so we don't alter the original input
    w_prefs = copy.deepcopy(w_prefs_i)
    m_prefs = copy.deepcopy(m_prefs_i)

    n = len(w_prefs)

    # Shuffled list of women who are free
    free = list(np.random.permutation(list(w_prefs.keys())).tolist())
    # Set of women who are finished proposing
    done = set()
    # Set of matches
    matches = {}

    while len(free) and len(done) < n:
        # Get the next free woman and her top choice
        w = free.pop(0)
        m = w_prefs[w].pop(0)
        
        # If there are no more men to propose to, mark m as done
        if len(w_prefs[w]) == 0:
            done.add(w)

        if m not in matches:
            # Man is free so he accepts
            matches[m] = w
        else:
            # Jilt if current match w_prime is less desirable
            w_prime = matches[m]
            if m_prefs[m].index(w) < m_prefs[m].index(w_prime):
                matches[m] = w
                free.append(w_prime)
            else:
                free.append(w)

    return matches


def validate_input(m_prefs: Dict[str, List[str]], w_prefs: Dict[str, List[str]]) -> None:
    """Make sure that the input is valid

    Args:
        m_prefs: Dictionary of men's preferences
        w_prefs: Dictionary of women's preferences
    """
    women = set(w_prefs.keys())
    men = set(m_prefs.keys())
    
    if len(women) != len(men):
        raise Exception('number of men != number of women')

    validate_prefs(w_prefs, men)
    validate_prefs(m_prefs, women)


def validate_prefs(prefs: Dict[str, List[str]], choices: Set[str]):
    """Ensure all preference lists are complete

   Args:
        prefs: Dictionary of preferences
        choices: Set of choices
    """
    for _, pref_list in prefs.items():
        if set(pref_list) != choices:
            raise Exception('incomplete list of prefs in input')

