from bowler import Bowler
from batsman import Batsman
class Innings:
	def __init__(self,batsman,bowlers,battingTeam,bowlingTeam):
		self.batsman=batsman
		self.bowlers=bowlers
		self.battingTeam=battingTeam
		self.bowlingTeam=bowlingTeam
		self.score=0
		self.wickets=0

	