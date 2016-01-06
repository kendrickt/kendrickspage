import numpy as np
from math import sqrt
from make_dat_files import get_data

"""
This file calculates the t-value to determine whether home ppgs is
different from away ppgs in an unpaired and paired t-test.

Both tests result with very large t-values, mainly because the sample size
is so large (over 1500 games). I don't find this very interesting.
"""


def get_std(dat1, dat2):
    mean1 = np.mean(dat1)
    mean2 = np.mean(dat2)
    summed = (sum((x - mean1)**2 for x in dat1) +
              sum((x - mean2)**2 for x in dat2))
    return summed / (len(dat1) + len(dat2) - 2.0)


if __name__ == "__main__":
    home = get_data('data/home_ppg.dat')
    home_mean, home_n = np.mean(home), len(home)

    away = get_data('data/away_ppg.dat')
    away_mean, away_n = np.mean(away), len(away)

    std = get_std(home, away)
    print (home_mean - away_mean) / sqrt(std * (1.0/home_n + 1.0/away_n))

    spread = []
    for i in xrange(len(home)):
        spread.append(home[i] - away[i])
    spread_mean = np.mean(spread)
    spread_std = np.std(spread)
    f = file('data/home_spread.dat', 'w')
    for val in spread:
        f.write(str(val) + '\n')
    f.close()
    print spread_mean / sqrt(spread_std / (len(spread)-1.0))
