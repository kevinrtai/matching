from typing import List, Dict, Tuple

import numpy as np


################
# Base Scorers #
################

def one_zero(match: str, prefs: List[str]) -> int:
    """Score 1 if the match is in the prefs list and 0 otherwise

    Args:
         match: name of the match
         prefs: ordered list of preferences

    Returns:
        float: the score
    """
    return 1 if match in prefs else 0


def frac(match: str, prefs: List[str]) -> float:
    """Earn a score equivalent to (n - i) / n. Earn 0 if match is not in prefs

    Args:
         match: name of the match
         prefs: ordered list of preferences

    Returns:
        float: the score
    """
    if match not in prefs:
        return 0

    n = len(prefs)
    i = prefs.index(match)
    return (n - i) / n


#################
# Score Warpers #
#################

def boost(base_score: float, b: float = 1) -> float:
    """"Boost" non-zero scores by some amount b

    Args:
         base_score: score to augment
         b: amount to augment the score by

    Returns:
        float: the score
    """
    return base_score + b if base_score > 0 else 0


def identity(base_score: float) -> float:
    """Identity function

    Args:
         base_score: score to augment

    Returns:
        float: the score
    """
    return base_score


def exponential(base_score: float) -> float:
    """Given a base score in the range [0, 1], map to an exponential in the range [0, 1]

    Args:
         base_score: score to warp

    Returns:
          float: the score
    """
    return (np.exp(base_score) - 1) / (np.exp(1) - 1)


###########
# Scoring #
###########

def score(match: str, prefs: List[str], score_fn=one_zero, warp_fn=identity, b=0) -> float:
    """Return the uni-directional score earned by a match between a and b given a's preference list

    Args:
        match: name of the match
        prefs: ordered preference list
        score_fn: scoring function to use
        warp_fn: warping function to use
        b: boost level

    Returns:
        float: the score
    """
    return boost(warp_fn(score_fn(match, prefs)), b=b)


def score_exponential(match: str, prefs: List[str]) -> float:
    """Default exponential scoring function

    Args:
        match: name of the match
        prefs: ordered preference list

    Returns:
        float: the score
    """
    return score(match, prefs, score_fn=frac, warp_fn=exponential, b=1)


def score_assignment(
        matches: Dict[str, str],
        prefs: Dict[str, List[str]],
        score_fn=one_zero,
        warp_fn=identity,
        b=0,
) -> Tuple[Dict[str, float], np.ndarray]:
    """Return the score earned by each match and the aggregate sum

    Args:
         matches: dictionary of matches
         prefs: ordered preference lists keyed by person
         score_fn: scoring function
         warp_fn: warping function
         b: boost level

    Returns:
        (dict, float): scores of each individual and overall score
    """
    def score_individual(m: str, p: List[str]) -> float:
        return score(m, p, score_fn=score_fn, warp_fn=warp_fn, b=b)
    scores = {x: score_individual(matches[x], prefs[x]) for x in matches}
    return scores, np.sum([scores[x] for x in scores])
