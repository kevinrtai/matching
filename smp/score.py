import numpy as np

################
# Base Scorers #
################

def one_zero(match, prefs):
    '''Score 1 if the match is in the prefs list and 0 otherwise'''
    return 1 if match in prefs else 0

def frac(match, prefs):
    '''Earn a score equivalent to (n - i) / n. Earn 0 if match is not in prefs'''
    if match not in prefs:
        return 0

    n = len(prefs)
    i = prefs.index(match)
    return (n - i) / n


#################
# Score Warpers #
#################

def boost(base_score, b=1):
    '''"Boost" non-zero scores by some amount b'''
    return base_score + b if base_score > 0 else 0

def identity(base_score):
    return base_score

def exponential(base_score, boost=0):
    '''Given a base score in the range [0, 1], map to an exponential in the range [0, 1]'''
    return (np.exp(base_score) - 1) / (np.exp(1) - 1)

###########
# Scoring #
###########

def score(matches, prefs, score_fn=one_zero, warp_fn=identity, b=0):
    '''Return the score earned by each match and the aggregate sum'''
    scores = { x: boost(warp_fn(score_fn(matches[x], prefs[x])), b=b) for x in matches }
    return scores, np.sum([scores[x] for x in scores])

