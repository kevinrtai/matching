import numpy as np

def complete(w_prefs, m_prefs):
    '''Given two incomplete preference dicts, complete them with a random permutation of the remaining choices'''
    women = set(w_prefs.keys())
    men = set(m_prefs.keys())

    m_prefs_c = {m: complete_prefs(m_prefs[m], women) for m in m_prefs}
    w_prefs_c = {w: complete_prefs(w_prefs[w], men) for w in w_prefs}
    
    return w_prefs_c, m_prefs_c

def complete_prefs(prefs, choices):
    '''Given a single preference list, return a completed preference list with a permutation or the remaining choices'''
    remaining_choices = list(set(choices) - set(prefs))
    return prefs + np.random.permutation(remaining_choices).tolist()

