# Stable Marriage Problem
Solves the stable marriage problem with the caveat that the preference lists may not be complete. To compensate for this, we complete everyone's preference lists with a random permutation of each person's remaining choices. For example, suppose person a has choices {w, x, y, z} and submits [y, w] as her preference list. A completed preference list in this case can be either [y, w, x, z] or [y, w, z, x]. 

Due to this randomness, some solutions will be more desirable than others; better solutions will include more matches from the "real" part of the preferences list and not the "hallucinated" part. To compensate, we try many different configurations and select the best according to one of the scoring functions below.

There (apparently) is a way to optimize directly for some notion of fairness. This is described here: https://arxiv.org/pdf/1905.06626.pdf. Future versions of this tool may include an implementation.

## Usage
```
python smp/main.py WOMEN_PREFS MEN_PREFS --b=BLACKLIST --scorer=SCORER --warper=WARPER --weight=FLOAT -n=INT
```

## Algorithm
https://www.geeksforgeeks.org/stable-marriage-problem

## Scoring
See `scoring.pdf`
