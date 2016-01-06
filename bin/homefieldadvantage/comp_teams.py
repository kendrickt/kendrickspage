from make_dat_files import read_game_file
from collections import defaultdict
import sys


class Team(object):
    """
    An object which keeps track of a teams home stats, away stats, total stats,
    the ratio between home and away stats,
    and the differential between home and away stats.
    """
    def __init__(self, name, games):
        self.name = name
        self.home = get_stats(filter(lambda x: x.ishome, games))
        self.away = get_stats(filter(lambda x: not x.ishome, games))
        self.total = get_stats(games)
        self.ratio = get_stat_ratio(self.home, self.away)
        self.diff = get_stat_diff(self.home, self.away)

    def __repr__(self):
        return '%s  %s  %s' % (self.name, str(self.ratio), str(self.diff))


class Stats(object):
    """
    An object which contains the points per game, points allowed per game,
    spread per game, win rating, and total wins for a set of games
    """
    def __init__(self, ppg, papg, spg, winrating, wins):
        self.ppg = ppg
        self.papg = papg
        self.spg = spg
        self.winrating = winrating
        self.wins = wins

    def __repr__(self):
        return ('%1.3f,%1.3f,%1.3f,%1.3f,%1f' %
                (self.ppg, self.papg, self.spg, self.winrating, self.wins))


def get_team_dict(filename):
    """
    Given a game file, creates a dictionary mapping a team's name to
    a list of the games they played.
    """
    games = read_game_file(filename)

    team_dict = defaultdict(list)
    for game in games:
        team_dict[game.team].append(game)
    return team_dict


def get_stats(games):
    """
    Given a list of games, returns points per game, points allowed per game,
    and spread per game
    """
    spread = 0.0
    pts = 0.0
    ptsallowed = 0.0
    wins = 0.0
    for game in games:
        pts += game.pts
        ptsallowed += game.ptsallowed
        spread += game.pts - game.ptsallowed
        if game.pts > game.ptsallowed:
            wins += 1.0
    return Stats(pts/len(games), ptsallowed/len(games),
                 spread/len(games), wins/len(games), wins)


def get_stat_ratio(homestats, awaystats):
    """
    Returns the ratio of two sets of Stats as a Stats object.
    There are +delta's everywhere to avoid dividing by zero problems.
    I don't look at the ratio of home spread per game vs away spread per game
    because I can't think of a great way to avoid division by zero.
    Instead, you can look at the home-away spread differential.
    """
    delta = 0.00001
    ppg_ratio = (homestats.ppg+delta) / (awaystats.ppg+delta)
    papg_ratio = (homestats.papg+delta) / (awaystats.papg+delta)
    winrating_ratio = (homestats.winrating+delta) / (awaystats.winrating+delta)

    spg_ratio = 0.0  # Isn't being used.
    win_ratio = 0.0  # Isn't being used.

    return Stats(ppg_ratio, papg_ratio, spg_ratio, winrating_ratio, win_ratio)


def get_stat_diff(homestats, awaystats):
    """
    Returns the difference of two sets of Stats as a Stats object.
    I'm only ever interested for differences greater than 0.
    """
    ppg_diff = homestats.ppg - awaystats.ppg
    papg_diff = homestats.papg - awaystats.papg
    spg_diff = homestats.spg - awaystats.spg
    winrating_diff = homestats.winrating - awaystats.winrating

    win_diff = 0.0  # Isn't being used.
    return Stats(ppg_diff, papg_diff, spg_diff, winrating_diff, win_diff)


def examine_stat(team_stats, n, filter_func, sort_key, reverse, f=None):
    """
    Sorts the teams by a specific key (e.g. at-home ppg).
    and then returns the n teams with the highest (reverse=True),
    or lowest (reverse=False) key value.

    The filter_func is used to mark specific teams,
    e.g. teams whose at-home ppg is less than their away ppg.
    """

    team_stats.sort(key=sort_key, reverse=reverse)

    for team in team_stats[0:n]:
        s = ('%s,%1.3f,%d,%d,%d' %
             (team.name, sort_key(team), filter_func(team),
              team.home.wins, team.total.wins))
        if f:
            f.write(s + '\n')
        else:
            print s
    return team_stats[0:n]


def examine_ppg(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.ppg > x.away.ppg,
        lambda x: x.home.ppg,
        True,
        f
    )


def examine_ppg_away(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.ppg > x.away.ppg,
        lambda x: x.away.ppg,
        True,
        f
    )


def examine_papg(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.papg < x.away.papg,
        lambda x: x.home.papg,
        False,
        f
    )


def examine_papg_away(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.papg < x.away.papg,
        lambda x: x.away.papg,
        False,
        f
    )


def examine_spg(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.spg > x.away.spg,
        lambda x: x.home.spg,
        True,
        f
    )


def examine_spg_away(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.spg > x.away.spg,
        lambda x: x.away.spg,
        True,
        f
    )


def examine_winrating(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.winrating > x.away.winrating,
        lambda x: x.home.winrating,
        True,
        f
    )


def examine_winrating_away(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.winrating > x.away.winrating,
        lambda x: x.away.winrating,
        True,
        f
    )


def examine_ppgratio(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.ppg > x.away.ppg,
        lambda x: x.ratio.ppg,
        True,
        f
    )


def examine_papgratio(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.papg < x.away.papg,
        lambda x: x.ratio.papg,
        False,
        f
    )


def examine_winratingratio(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.winrating > x.away.winrating,
        lambda x: x.ratio.winrating,
        True,
        f
    )


def examine_ppgdiff(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.ppg > x.away.ppg,
        lambda x: x.diff.ppg,
        True,
        f
    )


def examine_papgdiff(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.papg < x.away.papg,
        lambda x: x.diff.papg,
        True,
        f
    )


def examine_spgdiff(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.spg > x.away.spg,
        lambda x: x.diff.spg,
        True,
        f
    )


def examine_winratingdiff(team_stats, n, f=None):
    examine_stat(
        team_stats,
        n,
        lambda x: x.home.winrating > x.away.winrating,
        lambda x: x.diff.winrating,
        True,
        f
    )


func_dict = {
    'ppg': examine_ppg,
    'ppgaway': examine_ppg_away,
    'ppgratio': examine_ppgratio,
    'ppgdiff': examine_ppgdiff,
    'papg': examine_papg,
    'papgaway': examine_papg_away,
    'papgratio': examine_papgratio,
    'papgdiff': examine_papgdiff,
    'spg': examine_spg,
    'spgaway': examine_spg_away,
    'spgdiff': examine_spgdiff,
    'winrating': examine_winrating,
    'winratingaway': examine_winrating_away,
    'winratingratio': examine_winratingratio,
    'winratingdiff': examine_winratingdiff
}


if __name__ == '__main__':
    func, years = sys.argv[1], sys.argv[2]
    sys.argv[3]
    try:
        n = int(sys.argv[3])
    except IndexError:
        print "Warning: n is not defined. n is defaulted to 10."
        n = 10

    team_dict = get_team_dict(
        'bin/homefieldadvatnage/games/games_%s.csv' % years)
    team_stats = [Team(team, team_dict[team]) for team in team_dict]

    # Bleacher report lists SEA, CHI, MIN, DEN, and KC as the top 5 home
    # stadiums.

    if func in func_dict.keys():
        func_dict[func](team_stats, n)
    elif func == 'make':
        for func in func_dict.keys():
            fs = file(
                'bin/homefieldadvantage/data/%s_top_%s.dat' % (years, func),
                'w')
            func_dict[func](team_stats, n, f=fs)
            fs.close()
