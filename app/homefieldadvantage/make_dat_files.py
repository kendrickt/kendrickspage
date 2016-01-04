import sys
from game import Game


def read_game_file(filename):
    """
    Reads through a .csv containing game data and creates a game for each line.
    The list of games is returned.
    """
    f = file(filename, 'r')
    games = []
    f.next()  # header
    for line in f:
        game = line_to_game(line)
        games.append(game)
    f.close()
    return games


def line_to_game(line):
    """
    Given a line of text from a .csv containing game data,
    the line is encoded into a Game object which is then returned
    """
    data = line.split(',')
    year, team, ishome, week, pts, ptsallowed = (
        int(data[0]), data[1], int(data[2]),
        int(data[3]), int(data[4]), int(data[5])
    )
    return Game(year, week, team, ishome, pts, ptsallowed)


def partition_games(games, partitioner):
    """
    Given a list of games and a way to define a key (partitioner),
    the games are partitioned with a dictionary and the dictionary is returned.
    """
    partitions = {}
    for game in games:
        key = partitioner(game)
        if key in partitions:
            partitions[key].append(game)
        else:
            partitions[key] = [game]
    return partitions


def write_stat(games, eq_class_func, get_stat, mask, filename):
    """
    Takes the game(s), partitions them according to the equivalence class func,
    filters each partition through the mask, and writes a data file containing
    the statistics of each filtered partition in the filename.
    """
    out = file(filename, 'w')
    if eq_class_func:
        partition = partition_games(games, eq_class_func)
        partition = partition.values()
    else:
        partition = games
    count = 0
    for part in partition:
        stat = get_stat(part, mask)
        if stat is not None:
            count += 1
            out.write('%1.3f\n' % stat)
    out.close()


def write_home_win_rating(games):
    """
    Given a list of games, the games are partitioned by their year and week.
    Then a .dat file containing the at-home win-rating for each partition
    is written.
    """
    write_stat(
        games,
        lambda x: (x.week, x.year),
        get_home_win_rating,
        lambda x: x.ishome,
        'data/home_win_rating.dat'
    )


def write_home_ppg(games):
    """
    Given a list of games, a .dat file containing a list of points
    scored of each home game is written.
    """
    write_stat(
        games,
        None,
        get_ppg,
        lambda x: x.ishome,
        'data/home_ppg.dat'
    )


def write_away_ppg(games):
    """
    Given a list of games, a .dat file containing a list of points
    scored of each away game is written.
    """
    write_stat(
        games,
        None,
        get_ppg,
        lambda x: not int(x.ishome),
        'data/away_ppg.dat'
    )


def write_total_ppg(games):
    """
    Given a list of games, a .dat file containing a list of points
    scored of each game is written.
    """
    write_stat(
        games,
        None,
        get_ppg,
        lambda x: True,
        'data/total_ppg.dat'
    )


def write_spread(games):
    """
    Given a list of games, a .dat file containing a list of spread
    of each home game is written.
    """
    write_stat(
        games,
        None,
        get_spread,
        lambda x: x.ishome,
        'data/home_spread.dat'
    )


def get_spread(games, mask):
    """
    Given a list of games, or a single game, the game(s) are filtered
    through the mask, and the spread per game of the remaining games
    is returned.
    """
    if type(games) is list:
        spread, num_of_games = 0.0, 0.0
        for game in games:
            if mask(game):
                spread += game.pts - game.ptsallowed
                num_of_games += 1.0
        if num_of_games:
            return spread / num_of_games
    elif mask(games):
        return games.pts - games.ptsallowed
    return None


def get_home_win_rating(games, mask):
    """
    Given a list of games, the games are filtered through the mask,
    and the percentage of wins in the filtered set is returned
    """
    wins, num_of_games = 0.0, 0.0
    for game in games:
        if mask(game):
            if game.pts > game.ptsallowed:
                wins += 1.0
            num_of_games += 1.0
    if num_of_games > 0:
        return wins / num_of_games
    return None


def get_ppg(games, mask):
    """
    Given a list of games, or a single game, the game(s) are filtered
    through the mask, and the points scored per game of the remaining games
    is returned.
    """
    if type(games) is list:
        pts, num_of_games = 0.0, 0.0
        for game in games:
            if mask(game):
                pts += game.pts
                num_of_games += 1.0
        if num_of_games > 0:
            return pts / num_of_games
    elif mask(games):
        return games.pts
    return None


def get_data(filename):
    """
    Used to retrieve a list of data from a .dat file.
    This is used externally.
    """
    f = file(filename, 'r')
    data = []
    for line in f:
        #  I have two data formats: (float), and (string,float,integer,integer)
        line_data = line.split(',')
        if len(line_data) == 1:
            data.append(float(line_data[0]))
        elif len(line_data) == 5:
            data.append(
                (str(line_data[0]),
                 float(line_data[1]),
                 int(line_data[2]),
                 int(line_data[3]),
                 int(line_data[4]))
            )
        else:
            print "Warning, invalid .dat file format."

    f.close()
    return data


if __name__ == "__main__":
    func = sys.argv[1]
    function_dict = {
        'homeppg': write_home_ppg,
        'awayppg': write_away_ppg,
        'totalppg': write_total_ppg,
        'winrating': write_home_win_rating,
        'spread': write_spread
    }

    games = read_game_file(sys.argv[2])

    if func in function_dict:
        function_dict[func](games)
    else:
        print "invalid function: %s" % func
        print "valid functions are: ", function_dict.keys()
