from bs4 import BeautifulSoup
import pickle,csv,urllib2,re

def createSoup(url,domain=""):
	completeUrl = domain + url
	req = urllib2.Request(completeUrl)
	response = urllib2.urlopen(req)
	content = response.read()

	soup = BeautifulSoup(content,'html.parser')
	return soup

def getStats(url,bat,bowl,name):
	player={}
	if(not bat and not bowl):
		return None
	soup = createSoup(url)
	#Basic Details -> Age,Playing Role
	player['general']={}
	basicInfo = soup.find_all("p",class_='ciPlayerinformationtxt')
	for row in basicInfo:
		if "age" in row.find("b").contents[0]:
			 player['general']['Age'] = row.find("span").contents[0].split()[0]
		elif "Playing role" in row.find("b").contents[0]:
			player['general']['Role'] = row.find("span").contents[0].strip()
		elif "Batting style" in row.find("b").contents[0]:
			player['general']['Batting Style'] = row.find("span").contents[0].strip()
		elif "Bowling style" in row.find("b").contents[0]:
			player['general']['Bowling Style'] = row.find("span").contents[0].strip()		
	engineTables = soup.find_all("table",class_='engineTable')
	if(bat):
		player['bat']={}
		table = engineTables[0]
		for row in table.find_all("tr",class_='data1'):
			format = row.find("td",class_='left').find("b").contents[0]
			if(format == 'Twenty20'):
				elements = row.find_all("td")[1:]
				try:
					player['bat']['Matches'] = elements[0].contents[0]
					player['bat']['Innings'] = elements[1].contents[0]
					player['bat']['Runs'] = elements[3].contents[0]
					player['bat']['Highest Score'] = re.search(r'\d+', elements[4].contents[0]).group() #regex to remove the * if not out
					player['bat']['Average'] = elements[5].contents[0]
					player['bat']['Strike Rate'] = elements[7].contents[0]
				except IndexError: 
					#contents is an empty list. That means data is not available because I presume he's  bad batsman.
					#Remove him from batsman set.
					del player['bat']
					batsmen.remove(name)

	if(bowl):
		player['bowl']={}
		table = engineTables[1]
		for row in table.find_all("tr",class_='data1'):
			format = row.find("td",class_='left').find("b").contents[0]
			if(format == 'Twenty20'):
				elements = row.find_all("td")[1:]
				try:
					player['bowl']['Matches'] = elements[0].contents[0]
					player['bowl']['Innings'] = elements[1].contents[0]
					player['bowl']['Wickets'] = elements[4].contents[0]
					player['bowl']['Best Figures'] = elements[5].contents[0]
					player['bowl']['Average'] = elements[7].contents[0]
					player['bowl']['Economy'] = elements[8].contents[0]
					player['bowl']['Strike Rate'] = elements[9].contents[0]
				except IndexError:
					#Same as for batsman
					del player['bowl']
					bowlers.remove(name)	
	return player

def saveStats(dict,name):
	keys = dict[dict.keys()[0]].keys()
	filename = name+".csv"
	with open('Dataset/'+filename, 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(dict.values())

def savePlayerInfo(dict,name):
	keys = dict[0].keys()
	filename = name+".csv"
	with open('Dataset/'+filename, 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(dict.values())	    


if(__name__=="__main__"):
	with open('playerLinks.csv','rb') as fp:
		players = dict(csv.reader(fp))
	with open('batsmen.pkl','r') as fp:
		batsmen = pickle.load(fp)
	with open('bowlers.pkl','r') as fp:
		bowlers = pickle.load(fp)	
	stats={}
	bat_stats,bowl_stats = {},{}	
	#Use Cricinfo ID for each player and get the stats!
	count = 0
	newPlayers = dict()
	for name,link in sorted(players.items()):
		print "Fetching",name
		stats[name] = getStats(link,name in batsmen,name in bowlers,name)
		if(stats[name]==None):
			del stats[name]
			continue
		if name in batsmen:
			bat_stats[name] = stats[name]['bat']
			bat_stats[name]['Name'] = name
		if name in bowlers:
			bowl_stats[name] = stats[name]['bowl']
			bowl_stats[name]['Name'] = name
		newPlayers[count]={'Name':name}
		newPlayers[count].update(stats[name]['general'])
		count+=1
		if count%50==0:
			print "-------------------------------------Intermediate Save at",count,"---------------------------------------------"
			savePlayerInfo(newPlayers,'playerDetails')	
			saveStats(bat_stats,'batsmanStats')
			saveStats(bowl_stats,'bowlerStats')
	print "-------------------------------------Final Save at",count,"---------------------------------------------"		
	savePlayerInfo(newPlayers,'playerDetails')	
	saveStats(bat_stats,'batsmanStats')
	saveStats(bowl_stats,'bowlerStats')			
