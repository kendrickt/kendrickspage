from make_dat_files import get_data
from matplotlib import pyplot as plt
import sys


def plot_data(years, stat, win_type):
    data = get_data('bin/homefieldadvantage/data/%s_top_%s.dat' % (years, stat))
    plt.figure(1)
    min_x, max_x = sys.maxint, 0
    min_y, max_y = sys.maxint, 0

    for datum in data:
        name, value, passes_filter, home_wins, total_wins = datum
        if win_type == 'home':
            wins = home_wins
        elif win_type == 'total':
            wins = total_wins
        else:
            print "Warning: invalid win_type. Defaulted to 'home'."
            wins = home_wins

        if passes_filter:
            color = 'k'
        else:
            color = 'r'
        plt.text(wins, value, name, size='large', color=color)
        min_x, max_x = min(min_x, wins), max(max_x, wins)
        min_y, max_y = min(min_y, value), max(max_y, value)

    plt.xlim(min_x - max_x/10.0, max_x + max_x/10.0)
    plt.ylim(min_y - max_y/10.0, max_y + max_y/10.0)

    # X and Y labels
    plt.ylabel(stat, size='large')
    plt.xlabel('# of %s wins' % win_type, size='large')

    plt.show()


def plot_data_comparison(years_x, stat_x, years_y, stat_y, square):
    data_x = get_data(
        'bin/homefieldadvantage/data/%s_top_%s.dat' % (years_x, stat_x))
    data_y = get_data(
        'bin/homefieldadvantage/data/%s_top_%s.dat' % (years_y, stat_y))
    plt.figure(1)
    min_x, max_x = sys.maxint, 0
    min_y, max_y = sys.maxint, 0

    data = {}

    # Links a team with their stat_x.
    for datum in data_x:
        name, value = datum[0], datum[1]
        data[name] = [value]

    # Links a team with their stat_y.
    for datum in data_y:
        name, value = datum[0], datum[1]
        data[name].append(value)

    # Plot
    for team in data:
        x_val, y_val = data[team]
        plt.text(x_val, y_val, team, size='large')

        min_x, max_x = min(min_x, x_val), max(max_x, x_val)
        min_y, max_y = min(min_y, y_val), max(max_y, y_val)

    if square:
        min_x, min_y = min(min_x, min_y), min(min_x, min_y)
        max_x, max_y = max(max_x, max_y), max(max_x, max_y)

    x_diff = max_x - min_x
    y_diff = max_y - min_y
    plt.xlim(min_x - x_diff/6.0, max_x + x_diff/6.0)
    plt.ylim(min_y - y_diff/6.0, max_y + y_diff/6.0)

    # X and Y labels
    plt.ylabel(stat_y, size='large')
    plt.xlabel(stat_x, size='large')

    plt.show()


def plot_data_comparison_app(filename, startyear, endyear, xaxis, yaxis):
    data_x = get_data(
        'bin/homefieldadvantage/data/%s_%s.dat' % (filename, xaxis))
    data_y = get_data(
        'bin/homefieldadvantage/data/%s_%s.dat' % (filename, yaxis))
    plt.figure(1)
    min_x, max_x = sys.maxint, 0
    min_y, max_y = sys.maxint, 0

    data = {}

    # Links a team with their stat_x.
    for datum in data_x:
        name, value = datum[0], datum[1]
        data[name] = [value]
    x_avg = sum([datum[1] for datum in data_x]) / 32.0

    # Links a team with their stat_y.
    for datum in data_y:
        name, value = datum[0], datum[1]
        data[name].append(value)
    y_avg = sum([datum[1] for datum in data_y]) / 32.0

    # Plot teams
    for team in data:
        x_val, y_val = data[team]
        plt.text(x_val, y_val, team, size='large')

        min_x, max_x = min(min_x, x_val), max(max_x, x_val)
        min_y, max_y = min(min_y, y_val), max(max_y, y_val)

    # Determine plot size.
    x_diff = max_x - min_x
    y_diff = max_y - min_y
    min_x, max_x = min_x - x_diff/6.0, max_x + x_diff/6.0
    min_y, max_y = min_y - y_diff/6.0, max_y + y_diff/6.0

    # Plot quartile lines.
    plt.plot([x_avg, x_avg], [min_y, max_y], lw=2, color='g')  # avg of x values
    plt.plot([min_x, max_x], [y_avg, y_avg], lw=2, color='b')  # avg of y values

    # Set plot size.
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    # Title
    plt.title('%s-%s' % (startyear, endyear))

    # X and Y labels
    plt.xlabel(xaxis, size='large')
    plt.ylabel(yaxis, size='large')

    plt.savefig(
        'app/static/images/20160103_homefieldadvantage3/%s.png' % filename
    )

    plt.close()


if __name__ == '__main__':
    func = sys.argv[1]
    if func == 'plot':
        years, stat, win_type = sys.argv[2:]
        plot_data(years, stat, win_type)
    elif func == 'compare':
        years_x, stat_x, years_y, stat_y = sys.argv[2:]
        plot_data_comparison(years_x, stat_x, years_y, stat_y, False)
    elif func == 'comparesquare':
        years_x, stat_x, years_y, stat_y = sys.argv[2:]
        plot_data_comparison(years_x, stat_x, years_y, stat_y, True)
    else:
        print 'Invalid func: %s' % func
