import argparse
import smp as smp 
from utils import complete
from pprint import pprint
from score import score, one_zero, frac, boost, identity, exponential
import pickle
import datetime
from tqdm import tqdm

scorers = {
    'one_zero': one_zero,
    'frac': frac
}

warpers = {
    'identity': identity,
    'exponential': exponential
}

def parse_args():
    parser = argparse.ArgumentParser(description='Solve the Stable Marriage Problem')
    parser.add_argument('women_prefs', metavar='W', type=str)
    parser.add_argument('men_prefs', metavar='M', type=str)
    parser.add_argument('-n', '--num_exp', dest='n', default=1000, type=int)
    parser.add_argument('--weight', default=0.5, type=float, help='weight to be assigned to the women\'s score')
    parser.add_argument('--scorer', default='one_zero', choices=scorers)
    parser.add_argument('--warper', default='identity', choices=warpers)
    parser.add_argument('--boost', default=0.0, type=float)

    return parser.parse_args()

def read_input(f_path):
    prefs = {}
    with open(f_path, 'r') as f:
        line = f.readline()
        while line:
            person, prefs_csv = line.split(':')
            prefs[person] = prefs_csv.strip().split(',')
            line = f.readline()
    return prefs

def main():
    # Read arguments
    args = parse_args()

    # Get the requested scoring function and warping function
    score_fn = scorers[args.scorer]
    warp_fn = warpers[args.warper]
    compute_score = lambda matches, prefs: score(matches, prefs, score_fn=score_fn, warp_fn=warp_fn, b=args.boost)

    # Get preferences lists
    w = read_input(args.women_prefs)
    m = read_input(args.men_prefs)
    problem_size = len(m)
   
    print(f'Solving...')

    results = []
    best_score = best = None
    for i in tqdm(range(args.n)):
        # Complete any incomplete lists
        w_c, m_c = complete(w, m)
   
        # Solve the SMP
        reverse_matches = smp.solve(w_c, m_c)
        matches = {reverse_matches[m]: m for m in reverse_matches}

        # Get the scores
        w_scores, w_total = compute_score(matches, w)
        m_scores, m_total = compute_score(reverse_matches, m)
        overall_raw = args.weight * w_total + (1 - args.weight) * m_total
        overall = overall_raw / problem_size

        # Update best result
        if best_score == None or overall > best_score:
            best_score = overall
            best = matches

        results.append({
            'w_c': w_c,
            'm_c': m_c,
            'match': matches, 
            'overall': overall,
            'w_scores': w_scores,
            'm_scores': m_scores
        })

    print('')
    print('###########')
    print('# RESULTS #')
    print('###########')
    print(f'Top Score: {best_score:.2%}')
    print(f'Best Matches:')
    for w in sorted(best.keys()):
        print(f'    {w} - {best[w]}')

    # Save parameters, outputs in dict
    output = {
        'scorer': args.scorer,
        'warper': args.warper,
        'boost': args.boost,
        'weight': args.weight,
        'women_prefs': w,
        'men_prefs': m,
        'problem_size': problem_size,
        'best': best,
        'best_score': best_score,
        'results': results
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    pickle.dump(output, open(f'outputs/results{timestamp}.smp', 'wb'))

    print('\nfin')

if __name__ == '__main__':
    main()
