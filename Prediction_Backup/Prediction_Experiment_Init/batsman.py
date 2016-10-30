import csv
class Batsman:
	def __init__(self,name,position,clusterNo):
		self.name=name
		self.position=position
		self.runsScored=0
		self.strikeRate=0
		self.ballsPlayed=0
		self.clusterNumber=clusterNo

	'''Update stats after every ball'''
	def updateStats(runsScored):
		self.runsScored+=runsScored
		self.ballsPlayed+=1
		self.strikeRate=self.runsScored/float(self.ballsPlayed)*100

	def __repr__(self):
		return self.name























def loadFromCSV(file):
	with open(file,'rb') as f:
		Lines=csv.reader(f)
		allLines=[]
		for line in Lines:
			allLines.append(line)
	return allLines

