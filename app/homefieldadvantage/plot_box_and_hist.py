from matplotlib import pyplot as plt
import numpy as np
import sys
from make_dat_files import get_data


def plot_box_and_hist(filename, xlabel, comparison_val):
    """
    Makes a box plot and histogram of the data contained in the filename.
    Also draws in a line for a comparision value.

    For example, if plotting the at-home point spreads, a good comparison
    value would be 0.0.
    """
    data = get_data(filename)
    average = np.mean(data)

    fig = plt.figure(figsize=(6, 4))
    boxplot_axes = fig.add_axes([0.1, 0.7, 0.7, 0.15])
    histplot_axes = fig.add_axes([0.1, 0.1, 0.7, 0.6])
    histplot_axes.xaxis.label.set_fontsize(13)
    histplot_axes.yaxis.label.set_fontsize(13)
    for item in (histplot_axes.get_xticklabels() +
                 histplot_axes.get_yticklabels()):
        item.set_fontsize(13)

    boxplot_axes.boxplot(data, notch=True, vert=False)
    boxplot_axes.plot([average, average], [0, 3], lw=3, color='g')
    boxplot_axes.plot(
        [comparison_val, comparison_val], [0, 3], lw=3, color='b')

    hist = histplot_axes.hist(data, bins=12, color='gray')
    maxval = max(hist[0])
    histplot_axes.plot(
        [average, average],
        [0, maxval+maxval/6],
        lw=3,
        color='g'
    )
    histplot_axes.plot(
        [comparison_val, comparison_val],
        [0, maxval+maxval/6],
        lw=3,
        color='b'
    )

    histplot_axes.set_ylim(0, maxval+maxval/6)

    boxplot_axes.set_xticklabels([])
    boxplot_axes.set_yticks([])
    histplot_axes.set_yticks([])

    plt.xlabel(xlabel, size='large')

    plt.show()


if __name__ == '__main__':
    func = sys.argv[1]
    if func == 'winrating':
        plot_box_and_hist(
            'data/home_win_rating.dat', 'weekly at-home win rating', 0.5)
    elif func == 'spread':
        plot_box_and_hist('data/home_spread.dat', 'at-home point spread', 0.0)
    else:
        print "invalid function: %s" % func
