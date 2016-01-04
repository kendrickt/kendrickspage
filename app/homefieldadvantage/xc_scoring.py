from collections import defaultdict
import sys


def combine_scores(scores, f):
    """
    Given a dictionary of scores, goes through a sorted file and
    adds the placement of each team to that team's score.
    """
    count = 0
    for line in f:
        count += 1
        team = line.split(',')[0]
        scores[team] += count


def dict_to_list(d):
    """
    Takes a dictionary that maps keys to the real numbers,
    and creates a list containing 2-tuples of keys and their respective value.
    Then the list is sorted WRT to the values.
    """
    l = []
    for key in d.keys():
        l.append((key, d[key]))

    l.sort(key=lambda x: x[1])
    return l


if __name__ == '__main__':
    scores = defaultdict(int)
    filenames = sys.argv[1:]
    for filename in filenames:
        f = file(filename, 'r')
        combine_scores(scores, f)

    list_of_scores = dict_to_list(scores)
    print list_of_scores
