import sys
import nflgame


def combine_games(filename, years):
    """
    Given a list of years, the .csv files associated with those years
    are concatenated into a combined game csv.
    """
    combined_games = file('games/games_%s.csv' % filename, 'w')
    print_header(combined_games)

    for year in years:
        try:
            f = file('games/games_%s.csv' % year, 'r')
        except IOError:
            print year,
            print 'does not have a file associated with it'
            break

        f.next()  # header
        for line in f:
            combined_games.write(line)
        f.close()
    combined_games.close()


def print_header(f):
    """
    Writes the common header to the file f.
    """
    f.write('year,team,ishome,week,pts,ptsallowed\n')


def get_games(years):
    """
    Given a list of N years, N .csv files will be written,
    each containing game data for the regular season of that year.
    """
    for year in years:
        f = file('games/games_%s.csv' % year, 'w')
        print_header(f)

        games = nflgame.games(int(year))
        for game in games:
            home_team = game.home
            home_score = game.score_home
            away_team = game.away
            away_score = game.score_away
            week = game.schedule['week']

            f.write(
                '%s,%s,%d,%d,%d,%d\n' %
                (year, home_team, 1, week, home_score, away_score)
            )
            f.write(
                '%s,%s,%d,%d,%d,%d\n' %
                (year, away_team, 0, week, away_score, home_score)
            )
        f.close()


if __name__ == "__main__":
    func = sys.argv[1]

    if func == 'get':
        get_games(sys.argv[2:])
    elif func == 'combine':
        combine_games(sys.argv[2], sys.argv[3:])
    else:
        print "invalid function: %s" % func
        print "valid functions are: ", function_dict.keys()
