import urllib2,csv
from bs4 import BeautifulSoup


def createSoup(url,domain=""):
	completeUrl = domain + url
	req = urllib2.Request(completeUrl)
	response = urllib2.urlopen(req)
	content = response.read()

	soup = BeautifulSoup(content,'html.parser')
	return soup

urls = ['http://www.espncricinfo.com/indian-premier-league-2016/content/series/968923.html?template=fixtures',
		'http://www.espncricinfo.com/indian-premier-league-2015/content/series/791129.html?template=fixtures',
		'http://www.espncricinfo.com/indian-premier-league-2014/content/series/695871.html?template=fixtures'
		]
year = ['2016','2015','2014','2013','2012']
urls = ['http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=3;id='+y+';type=year' for y in year]
domain = 'http://www.espncricinfo.com'
teams = set(['New Zealand','India','Australia','Sri Lanka','Pakistan','South Africa','England','West Indies'])
matchId = 0
matchDetails = {}
for index,url in enumerate(urls):
	soup = createSoup(url)
	print "Fetching fixtures for",year[index]	
	fixtureTable = soup.find_all("table", class_="engineTable")[0]

	for fixture in fixtureTable.find_all("tr",class_="data1"):
		links = fixture.find_all("a",href=True)	
		team1,team2 = map(lambda x: x.contents[0].strip(),links[0:2])
		if(team1 not in teams or team2 not in teams):
			continue
		match = links[-1]
		matchDetails[matchId]={}
		matchDetails[matchId]['MatchID'] = match.contents[0].strip()
		matchDetails[matchId]['Href'] = domain+match['href']
		matchDetails[matchId]['Home'] = team1
		matchDetails[matchId]['Away'] = team2
		matchDetails[matchId]['Stadium'] = links[-2].contents[0].strip()
		matchId +=1		
keys = matchDetails[0].keys()
filename = 'InterationalMatches.csv'
with open('Dataset/'+filename, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(matchDetails.values())
