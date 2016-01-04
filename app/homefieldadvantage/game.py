class Game(object):
    """
    For a specific team, the Game object contains information about a specific
    Game's year, week, whether the team was at home, the points scored,
    and points allowed.
    """

    def __init__(self, year, week, team, ishome, pts, ptsallowed):
        """
        Game object constructor
        """
        self.year = year
        self.week = week
        self.team = team
        self.ishome = ishome
        self.pts = pts
        self.ptsallowed = ptsallowed

    def __repr__(self):
        return '%d,%s,%d,%d' % (self.year, self.team, self.ishome, self.week)
