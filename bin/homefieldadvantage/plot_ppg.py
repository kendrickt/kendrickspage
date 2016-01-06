from matplotlib import pyplot as plt
import numpy as np
import sys
from make_dat_files import get_data


def make_hist():
    """
    Makes a histogram of the at-home ppg data.
    The histogram contains lines for the at-home ppg average and
    for the total ppg average.
    """
    ppgs = get_data('data/home_ppg.dat')
    average = np.mean(ppgs)

    totalppgs = get_data('data/total_ppg.dat')
    totalppg_avg = np.mean(totalppgs)

    f, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.hist(totalppgs, bins=12, color='gray')
    ax1.plot([totalppg_avg, totalppg_avg], [0, 700], lw=3, color='g')
    ax1.text(
        totalppg_avg+1, 620, "total mean=%1.3f" % totalppg_avg, size='large')
    ax1.text(-3, 520, "all games", rotation=90, size='large')
    ax1.set_yticks([])

    ax2.hist(ppgs, bins=12, color='gray')
    ax2.plot([average, average], [0, 350], lw=3, color='b')
    ax2.text(average+1, 300, "home mean=%1.3f" % average, size='large')
    ax2.text(-3, 270, "home games", rotation=90, size='large')

    plt.yticks([])
    plt.xlabel('points per game', size='large')

    plt.show()


def make_boxplot():
    """
    Makes three boxplots for home, away, and total ppgs.
    """
    home = get_data('data/home_ppg.dat')
    away = get_data('data/away_ppg.dat')
    total = get_data('data/total_ppg.dat')

    ax = plt.subplot(111)
    plt.boxplot([home, away, total], vert=False, widths=0.8)
    plt.yticks([])
    plt.text(-3, 3.3, "all games", rotation=90, size='large')
    plt.text(-3, 2.3, "away games", rotation=90, size='large')
    plt.text(-3, 1.3, "home games", rotation=90, size='large')
    plt.xlabel("points per game")
    plt.xlim(-1, 70)
    ax.xaxis.label.set_fontsize(20)
    plt.show()


if __name__ == "__main__":
    func = sys.argv[1]
    function_dict = {
        'box': make_boxplot,
        'hist': make_hist
    }

    if func in function_dict:
        function_dict[func]()
    else:
        print "invalid function: %s" % func
        print "valid functions are: ", function_dict.keys()
