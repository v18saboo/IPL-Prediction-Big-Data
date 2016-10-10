import csv,urllib2,pickle
from bs4 import BeautifulSoup

def createSoup(url,domain=""):
	completeUrl = domain + url
	req = urllib2.Request(completeUrl)
	response = urllib2.urlopen(req)
	content = response.read()

	soup = BeautifulSoup(content,'html.parser')
	return soup

def getPVPStats(matchUrl,pvpDict,batsmanSet,bowlerSet,extension = '?view=pvp'):

	soup = createSoup(matchUrl + extension)
	print "got page"
	for table in soup.find_all("table",class_ = 'innings-table'):
		batsman = str(table.find('caption').contents[0].split('- ')[0]).strip()
		batsmanSet.add(batsman)
		if(pvpDict.get(batsman,None)==None):
				pvpDict[batsman]={}				
		for tr in table.find_all('tr'):
			if(tr.get('class',None) and tr['class'][0] == 'tr-heading'):
				continue
			bowler = str(tr.find('td',class_= 'bowler-name').contents[0])
			if(pvpDict[batsman].get(bowler,None)==None):
				pvpDict[batsman][bowler] = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,'wickets':0,'runs':0,'balls':0}
			bowlerSet.add(bowler)
			stats = tr.find_all('td',class_=None)
			for i in range(len(stats)-1):
				#If wicket taken:
				if(i==8):
					if(len(stats[i].contents)!=0):
						pvpDict[batsman][bowler]['wickets']+=1
				elif(i==9):
					pvpDict[batsman][bowler]['runs']+=int(stats[i].contents[0])
				elif(i==10):
					pvpDict[batsman][bowler]['balls']+=int(stats[i].contents[0])			
				else:		
					pvpDict[batsman][bowler][i]+=int(stats[i].contents[0])
	return pvpDict,batsmanSet,bowlerSet		

def formatDict(pvp):
	l=[]
	for batsman in pvp.keys():
		for bowler in pvp[batsman].keys():
			entry = {}
			entry['Batsman'] = batsman
			entry['Bowler'] = bowler
			entry['0'] = pvp[batsman][bowler][0]
			entry['1'] = pvp[batsman][bowler][1]
			entry['2'] = pvp[batsman][bowler][2]
			entry['3'] = pvp[batsman][bowler][3]
			entry['4'] = pvp[batsman][bowler][4]
			entry['5'] = pvp[batsman][bowler][5]
			entry['6'] = pvp[batsman][bowler][6]
			entry['7+'] = pvp[batsman][bowler][7]
			entry['Wickets'] = pvp[batsman][bowler]['wickets']
			entry['Runs'] = pvp[batsman][bowler]['runs']
			entry['Balls'] = pvp[batsman][bowler]['balls']
			l.append(entry)
	return l		


if(__name__=="__main__"):
	pvpDict= {}
	bowlerSet = set()
	batsmanSet = set()
	year=['2014','2015','2016']
	'''with open('playerVplayer.pkl','r') as fp:
		pvpDict = pickle.load(fp)
	with open('batsmen.pkl','r') as fp:
		batsmanSet = pickle.load(fp)
	with open('bowlers.pkl','r') as fp:
		bowlerSet = pickle.load(fp)'''	
	for y in year:
		print "For year",y
		with open('Dataset/IPLMatches'+y+'.csv','rb') as csvFile:
			reader = csv.DictReader(csvFile)
			for match in reader:
				print "Getting data for Match No.",int(match['MatchID'])+1
				print match['Home'],'vs',match['Away']
				pvpDict,batsmanSet,bowlerSet = getPVPStats(match['Href'],pvpDict,batsmanSet,bowlerSet)
			with open('playerVplayer.pkl','w') as fp:
				pickle.dump(pvpDict,fp)
			with open('batsmen.pkl','w') as fp:
				pickle.dump(batsmanSet,fp)
			with open('bowlers.pkl','w') as fp:
				pickle.dump(bowlerSet,fp)	
	
	with open('Dataset/InternationalMatches.csv','rb') as csvFile:
		reader = csv.DictReader(csvFile)
		for match in reader:
			print "Getting data for Match No.",match['MatchID']
			print match['Home'],'vs',match['Away']
			pvpDict,batsmanSet,bowlerSet = getPVPStats(match['Href'],pvpDict,batsmanSet,bowlerSet)

	with open('playerVplayer.pkl','w') as fp:
		pickle.dump(pvpDict,fp)

	with open('batsmen.pkl','w') as fp:
		pickle.dump(batsmanSet,fp)
	with open('bowlers.pkl','w') as fp:
		pickle.dump(bowlerSet,fp)	

	print len(batsmanSet),len(bowlerSet)

	with open('Dataset/PlayerVPlayer.csv','wb') as fp:
		fieldnames = ['Batsman','Bowler','0','1','2','3','4','5','6','7+','Wickets','Runs','Balls']
		writer = csv.DictWriter(fp,fieldnames)
		writer.writeheader()
		data = formatDict(pvpDict)
		writer.writerows(data)
		