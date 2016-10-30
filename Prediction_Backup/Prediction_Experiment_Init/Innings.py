from bowler import Bowler
from batsman import Batsman
class Innings:
	def __init__(self,batsmen,bowlers,battingTeam,bowlingTeam):
		self.batsmen=batsmen
		self.bowlers=bowlers
		self.battingTeam=battingTeam
		self.bowlingTeam=bowlingTeam
		self.score=0
		self.wickets=0

	def swapBatsman(self):
		self.onStrike,self.nonStrike=self.nonStrike,self.onStrike
		self.onStrikeProbs,self.nonStrikeProbs=self.nonStrikeProbs,self.onStrikeProbs

	def setProbs(self,metadata):
		events=[i for i in range(0,8)]
		#events.append("Wickets")
		probs=dict()
		l=[metadata[i] for i in range(0,8)]
		l.append(metadata["Wickets"])
		total=sum(map(lambda x:float(x),l))
		for event in events:
			probs[event]=float(metadata[event])/float(total)
			probs["Init"+str(event)]=probs[event]
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
		self.onStrike=self.batsmen[self.wickets+1]		
		self.onStrikeProbs={self.onStrike.clusterNumber+"-"+str(i):self.setProbs(self.clusterStats[self.onStrike.clusterNumber+"-"+str(i)]) for i in range(0,10)}

	def getMaxKey(self,d):
		maxVal=0
		maxKey=0
		initList=['Init'+str(event) for event in range(0,8)]
		initList.append("InitNotOut")
		initList.append('NotOut')
		initList.append('Wickets')
		for key in d:	
			if key not in initList:
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
				onStrikeProbs[runsScored]=onStrikeProbs[runsScored]*onStrikeProbs["Init"+str(runsScored)]
				self.score+=runsScored
				if self.score>self.target and self.target!=-1:
					return True
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
				self.wickets+=1
				print "Wicket",self.onStrike
				if(self.wickets == 10):
					print "All Out"
					return True
				self.getNewBatsman()
				print "New batsman",self.onStrike
				#print "Not out prob for new batsman = ",onStrikeProbs["InitNotOut"]
			count+=1
				
		self.swapBatsman()	
		print self.score,self.wickets
		return False
		#print "***********"
		#print self.onStrikeProbs[self.onStrike.clusterNumber+"-"+currentBowler.clusterNumber]
		#print self.nonStrikeProbs[self.nonStrike.clusterNumber+"-"+currentBowler.clusterNumber]
		#print onStrikeProbs

	def simulateInnings(self,clusterStats,target=-1):
		self.clusterStats=clusterStats
		self.onStrike=self.batsmen[0]
		self.nonStrike=self.batsmen[1]
		currentBowler=self.bowlers[-1]
		self.target=target
		print self.bowlers
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
			print self.bowlers
			#index = int(raw_input("Enter bowler index"))
			index=-1
			print "Bowler = ",self.bowlers[index]
			if self.simulateOver(self.bowlers[index]):
				break
			else:
				print "End of over",i+1	
		print "Innings Total",self.wickets,self.score

