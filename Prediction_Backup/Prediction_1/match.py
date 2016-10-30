from batsman import Batsman
from bowler import Bowler
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
			self.firstInnings=Innings(self.awayBatsman,self.homeBowlers,awayTeam,homeTeam)
			self.secondInnings=Innings(self.homeBatsmen,self.awayBowlers,homeTeam,awayTeam)
		else:
			self.firstInnings=Innings(self.homeBatsmen,self.awayBowlers,homeTeam,awayTeam)
			self.secondInnings=Innings(self.awayBatsman,self.homeBowlers,awayTeam,homeTeam)

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

	def swapBatsman(self):
		self.onStrike,self.nonStrike=self.nonStrike,self.onStrike
		self.onStrikeProbs,self.nonStrikeProbs=self.nonStrikeProbs,self.onStrikeProbs

	def setProbs(self,metadata):
		events=[i for i in range(0,8)]
		events.append("Wickets")
		probs=dict()
		l=[metadata[i] for i in range(0,8)]
		l.append(metadata["Wickets"])
		total=sum(map(lambda x:float(x),l))
		for event in events:
			probs[event]=float(metadata[event])/float(total)
		probs["Wickets"]=float(metadata["Wickets"])/float(total)
		probs["NotOut"]=1-float(probs["Wickets"])
		probs["InitNotOut"] = probs["NotOut"]
		return probs

	def calculateProbs(self):
		self.onStrikeProbs={self.onStrike.clusterNumber+"-"+str(i):self.setProbs(self.clusterStats[self.onStrike.clusterNumber+"-"+str(i)]) for i in range(0,10)}
		'''{"0-1":{1:,2:,3:},"0-0":{},}'''
		self.nonStrikeProbs={self.nonStrike.clusterNumber+"-"+str(i):self.setProbs(self.clusterStats[self.nonStrike.clusterNumber+"-"+str(i)])for i in range(0,10)}
		#print self.nonStrikeProbs.keys()
	
	def getNewBatsman(self):
		self.onStrike=self.awayBatsmen[self.awayWickets+1]		
		self.onStrikeProbs={self.onStrike.clusterNumber+"-"+str(i):self.setProbs(self.clusterStats[self.onStrike.clusterNumber+"-"+str(i)]) for i in range(0,10)}

	def getMaxKey(self,d):
		maxVal=0
		maxKey=0
		for key in d:	
			if key not in ['NotOut','Wickets','InitNotOut']:
				if maxVal<d[key]:
					maxVal=d[key]
					maxKey=key
		return int(maxKey)

	def simulateOver(self,currentBowler):
		count=0
		total=0
		wickets=0
		while(count<6):
			onStrikeProbs=self.onStrikeProbs[self.onStrike.clusterNumber+"-"+currentBowler.clusterNumber]
			maxProb=self.getMaxKey(onStrikeProbs)
			print "On strike",self.onStrike
			runsScored=maxProb
			#print "Not out probability = ",onStrikeProbs["NotOut"]
			if onStrikeProbs["NotOut"]>0.5:
				onStrikeProbs[runsScored]=onStrikeProbs[runsScored]*onStrikeProbs[runsScored]
				total+=runsScored
				onStrikeProbs["NotOut"]=onStrikeProbs["NotOut"]*onStrikeProbs["InitNotOut"]
				if not runsScored%2==0:
					#print "Swapping",runsScored
					self.swapBatsman()
				else:
					pass
					#print runsScored
					#print self.onStrikeProbs
					#print "No swap",runsScored
			else:
				#get new batsman
				self.awayWickets+=1
				print "Wicket",self.onStrike
				if(self.awayWickets == 10):
					print "All Out"
					return True
				self.getNewBatsman()
				print "New batsman",self.onStrike
				#print "Not out prob for new batsman = ",onStrikeProbs["InitNotOut"]
			count+=1
				
		self.swapBatsman()	
		self.awayScore += total
		print self.awayScore,self.awayWickets
		return False
		#print "***********"
		#print self.onStrikeProbs[self.onStrike.clusterNumber+"-"+currentBowler.clusterNumber]
		#print self.nonStrikeProbs[self.nonStrike.clusterNumber+"-"+currentBowler.clusterNumber]
		#print onStrikeProbs

	def simulate(self,clusterStats):
		self.clusterStats=clusterStats
		self.onStrike=self.awayBatsmen[0]
		self.nonStrike=self.awayBatsmen[1]
		currentBowler=self.homeBowlers[-1]
		print self.homeBowlers
		self.calculateProbs()
		#print self.onStrikeProbs
		'''
		written for testing purposes
		l=[2,1,3,4,6,1]
		count=0
		while(count<6):
			print "On strike",self.onStrike,self.nonStrike
			if not l[count]%2==0:
				print "Swapping"
				self.swapBatsman()
			else:
				print l[count]
			count+=1'''
		fullTotal=0
		fullWickets=0
		for i in range(20):
			print self.homeBowlers
			index = int(raw_input("Enter bowler index"))
			print "Bowler = ",self.homeBowlers[index]
			if self.simulateOver(self.homeBowlers[index]):
				break
			else:
				print "End of over",i+1	
		print "Innings Total",self.awayWickets,self.awayScore


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