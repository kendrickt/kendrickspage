from make_game_files import combine_games
import comp_teams
from plot_stats import plot_data_comparison_app as plot_app


def get_games(filename, startyear, endyear):
    """
    Given two years, the game files for all the years in between (inclusive)
    is combined and out to a file.
    """
    years = [str(year) for year in range(int(startyear), int(endyear)+1)]
    combine_games(filename, years)


def make_stat_array(filename):
    """
    Given a game file, an array of Team objects for all teams in that
    game file is returned.
    """
    team_dict = comp_teams.get_team_dict('games/games_%s.csv' % filename)
    team_stats = [comp_teams.Team(team, team_dict[team]) for team in team_dict]
    return team_stats


def get_stats(filename, axis, team_stats):
    """
    Assumes that games/games_filename.csv contains game data,
    i.e. that get_games(filename, ....) has been called.
    Outputs stats to data/filename_stat.dat for a stat.
    """

    # Write the desired stat files.
    fout = file('bin/homefieldadvantage/data/%s_%s.dat' % (filename, axis), 'w')
    comp_teams.func_dict[axis](team_stats, 32, f=fout)


def run(filename, startyear, endyear, xaxis, yaxis):
    if 'Pick' in startyear:
        return "start-year must be selected"
    if 'Pick' in endyear:
        return "end-year must be selected"
    if int(startyear) > int(endyear):
        return "start year must be less than or equal to end year"
    if xaxis not in comp_teams.func_dict.keys():
        return "x-axis must be selected."
    if yaxis not in comp_teams.func_dict.keys():
        return "y-axis must be selected."

    get_games(filename, startyear, endyear)
    team_stats = make_stat_array(filename)
    get_stats(filename, xaxis, team_stats)
    get_stats(filename, yaxis, team_stats)
    plot_app(filename, startyear, endyear, xaxis, yaxis)
    return ""
