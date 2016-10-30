from batsman import Batsman
from bowler import Bowler
from Innings import Innings
import copy
import csv
class Match():
	def __init__(self,homeTeam,awayTeam,homeTeamPlayers,awayTeamPlayers,batsmanMapping,bowlerMapping,isHomeBatting=False):
		self.homeTeam=homeTeam
		self.awayTeam=awayTeam
		self.homeScore,self.awayScore,self.homeWickets,self.awayWickets = 0,0,0,0
		'''Unpack the players and make Batsman And bowler Objects'''
		self.homeBatsmen=self.createBastman(homeTeamPlayers,batsmanMapping)
		self.homeBowlers=self.createBowler(homeTeamPlayers,bowlerMapping)
		self.awayBatsmen=self.createBastman(awayTeamPlayers,batsmanMapping)
		self.awayBowlers=self.createBowler(awayTeamPlayers,batsmanMapping)
		if not isHomeBatting:
			self.firstInnings=Innings(self.awayBatsmen,self.homeBowlers,awayTeam,homeTeam)
			self.secondInnings=Innings(self.homeBatsmen,self.awayBowlers,homeTeam,awayTeam)
		else:
			self.firstInnings=Innings(self.homeBatsmen,self.awayBowlers,homeTeam,awayTeam)
			self.secondInnings=Innings(self.awayBatsmen,self.homeBowlers,awayTeam,homeTeam)

	def createBastman(self,players,batsmanMapping):
		'''param: players- List of players containing tuples to indicate their name,position''' 
		batsmen=[]
		for player in players:
			if player[0] in batsmanMapping:
				batsman=Batsman(player[0],player[1],batsmanMapping[player[0]])
				batsmen.append(batsman)
		return batsmen

	def createBowler(self,players,bowlerMapping):
		'''param: players - List of players containing name'''
		bowlers=[]
		for player in players:
			if player[0] in bowlerMapping:
				bowler=Bowler(player[0],bowlerMapping[player[0]])
				bowlers.append(bowler)
		return bowlers

	def simulate(self,clusterStats):
		self.firstInnings.simulateInnings(clusterStats)
		#self.clusterStats=clusterStats
		self.secondInnings.simulateInnings(clusterStats,target=self.firstInnings.score)
		print "First Inings"
		print self.firstInnings.score,self.firstInnings.wickets
		print "Seconf Innings"
		print self.secondInnings.score,self.secondInnings.wickets


def loadFromCSV(file):
	with open(file,'rb') as f:
		Lines=csv.reader(f)
		allLines=[]
		for line in Lines:
			allLines.append(line)
	return allLines

def mapPlayerToCluster(allLines):
	mapping=dict()
	for line in allLines:
		mapping[line[0]]=line[1]
	return mapping

def getClusterVClusterStats(file):
	'''Return : cluster stats is a dictionary with key as batsmanCluster-Blowler cluster
	Value is a dictionary with meta data like 4s and 6s'''
	allLines=loadFromCSV(file)
	allLines.pop(0)
	clusterStats=dict()
	for line in allLines:
		clusterStats[line[0]+"-"+line[1]]=dict()
		clusterStats[line[0]+"-"+line[1]][0]=line[2]
		clusterStats[line[0]+"-"+line[1]][1]=line[3]
		clusterStats[line[0]+"-"+line[1]][2]=line[4]
		clusterStats[line[0]+"-"+line[1]][3]=line[5]
		clusterStats[line[0]+"-"+line[1]][4]=line[6]
		clusterStats[line[0]+"-"+line[1]][5]=line[7]
		clusterStats[line[0]+"-"+line[1]][6]=line[8]
		clusterStats[line[0]+"-"+line[1]][7]=line[9]
		clusterStats[line[0]+"-"+line[1]]["Wickets"]=line[10]
		clusterStats[line[0]+"-"+line[1]]["Runs"]=line[11]
		clusterStats[line[0]+"-"+line[1]]["Balls"]=line[12]
	return clusterStats



if __name__=="__main__":
	allLines=loadFromCSV("Dataset/batsmanMapping.csv")
	allLines.pop(0) #To remove the header line
	batsmanMapping=mapPlayerToCluster(allLines)
	allLines=loadFromCSV("Dataset/bowlerMapping.csv")
	allLines.pop(0) #To remove the header line
	bowlerMapping=mapPlayerToCluster(allLines)
	#print batsmanMapping
	homeTeam=[('CH Gayle',1),('V Kohli',2),('AB de Villiers',3),('KL Rahul',4),('SR Watson',5),('Sachin Baby',6),('STR Binny',7),('MA Starc',8),('Iqbal Abdulla',9),('S Aravind',10),('YS Chahal',11)]
	awayTeam=[('DA Warner',1),('S Dhawan',2),('MC Henriques',3),('Yuvraj Singh',4),('DJ Hooda',5),('BCJ Cutting',6),('NV Ojha',7),('Bipul Sharma',8),('B Kumar',9),('BB Sran',10),('DW Steyn',11)]	
	final=Match("RCB","SRH",homeTeam,awayTeam,batsmanMapping,bowlerMapping)
	#print final.homeBatsmen
	#print final.homeBowlers
	clusterStats=getClusterVClusterStats("Dataset/clusterVcluster.csv")
	#print clusterStats
	final.simulate(clusterStats)