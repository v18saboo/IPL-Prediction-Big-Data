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
year = ['2016','2015','2014']
domain = 'http://www.espncricinfo.com'

for index,url in enumerate(urls):
	print "Fetching fixtures for",year[index]
	soup = createSoup(url)	
	fixtureDiv = soup.find_all("div", class_="fixtures_list")

	matchDetails = {}

	for element in fixtureDiv:
		for fixtureList in element.find_all("ul"):
			matchId = 0
			for match in fixtureList.find_all("li"):
				matchDetails[matchId]={}
				matchDetails[matchId]['MatchID'] = int(matchId)
				for detail in match.find_all("a",href=True):
					matchDetails[matchId]['Href'] = domain+detail['href']
					name = detail.contents[0].split("- ")[1]
					matchDetails[matchId]['Home'] = name.split(' v ')[0]
					matchDetails[matchId]['Away'] = name.split(' v ')[1]
				for stadium in match.find_all("span", class_="play_stadium"):
					matchDetails[matchId]['Stadium'] = stadium.contents[0].strip()
				for dn in match.find_all("span", class_="d_n"):
					matchDetails[matchId]['D/N'] = dn.contents[0].strip()
				matchId +=1		

	keys = matchDetails[0].keys()
	filename = 'IPLMatches'+year[index]+".csv"
	with open(filename, 'wb') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(matchDetails.values())
