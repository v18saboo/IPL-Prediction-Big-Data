class Bowler:
	def __init__(self,name,cluserNo):
		self.overs=0
		self.name=name
		self.runsConceded=0
		self.wicketsTaken=0
		self.economy=0
		self.clusterNumber=cluserNo

	'''Update stats at the end of each over'''
	def updateStats(runsConceded,wicketsTaken):
		self.runsConceded+=runsConceded
		self.wicketsTaken+=wicketsTaken

	def __repr__(self):
		return self.name
