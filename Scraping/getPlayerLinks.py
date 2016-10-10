from bs4 import BeautifulSoup
import pickle,csv,urllib2

def createSoup(url,domain=""):
	completeUrl = domain + url
	req = urllib2.Request(completeUrl)
	response = urllib2.urlopen(req)
	content = response.read()

	soup = BeautifulSoup(content,'html.parser')
	return soup

def getPlayerIDs(url,domain):
	matchPlayers={}
	soup = createSoup(url)
	for table in soup.find_all("table",class_ = 'batting-table'):
		for link in table.find_all("a",href=True):
			name = link.contents[0]
			matchPlayers[name] = domain+link['href']
	for table in soup.find_all("table",class_ = 'bowling-table'):
		for link in table.find_all("a",href=True):
			name = link.contents[0]
			matchPlayers[name] = domain+link['href']
	return matchPlayers		


#In scorecard page, class = batting-table, bowling-table
#Then get all links from those tables table. Store content and href. 


if(__name__=="__main__"):

	players={}

	year=['2014','2015','2016']
	domain = 'http://www.espncricinfo.com'

	for y in year:
		print "For year",y
		with open('Dataset/IPLMatches'+y+'.csv','rb') as csvFile:
			reader = csv.DictReader(csvFile)
			for match in reader:
				print "Getting data for Match No.",int(match['MatchID'])+1
				print match['Home'],'vs',match['Away']
				mPlayers = getPlayerIDs(match['Href'],domain)
				players.update(mPlayers)
	with open('Dataset/InternationalMatches.csv','rb') as csvFile:
		reader = csv.DictReader(csvFile)
		for match in reader:
			print "Getting data for ",(match['MatchID'])
			print match['Home'],'vs',match['Away']
			mPlayers = getPlayerIDs(match['Href'],domain)
			players.update(mPlayers)		
	with open('playerLinks.csv', 'wb') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in players.items():
			writer.writerow([key, value])			
