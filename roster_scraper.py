from bs4 import BeautifulSoup
from datetime import date
import urllib2
import json
import argparse
import re

ESPN_ROOT = 'http://espn.go.com'

SPORTS = {
	'NFL': {
		'base_url': 'http://espn.go.com/nfl/teams',
		'roster_links_selector': '.logo-nfl-medium span a[href^="/nfl/team/roster/"]',
		'team_names_selector': '.logo-nfl-medium h5 a[href^="http://www.espn.com/nfl/team/_/name/"]',
		'id_capture_regex': '/nfl/team/roster/_/name/(.*)/.*',
		'json_file': 'nfl.json'
	},
	'NBA': {
		'base_url': 'http://espn.go.com/nba/teams',
		'roster_links_selector': '.logo-nba-medium span a[href^="/nba/teams/roster?team="]',
		'team_names_selector': '.logo-nba-medium h5 a[href^="http://www.espn.com/nba/team/_/name/"]',
		'id_capture_regex': '/nba/teams/roster\?team=(.*)',
		'json_file': 'nba.json'
	},
	'NCAA_FOOTBALL': {
		'base_url': 'http://espn.go.com/college-football/teams',
		'roster_links_selector': '.medium-logos span a[href^="/ncf/teams/roster?teamId="]',
		'team_names_selector': '.medium-logos h5 a[href^="http://www.espn.com/college-football/team/_/id/"]',
		'id_capture_regex': '/ncf/teams/roster\?teamId=(.*)',
		'json_file': 'ncaa_football.json'
	},
	'NCAA_BASKETBALL': {
		'base_url': 'http://espn.go.com/mens-college-basketball/teams',
		'roster_links_selector': '.medium-logos span a[href^="/ncb/teams/roster?teamId="]',
		'team_names_selector': '.medium-logos h5 a[href^="http://www.espn.com/mens-college-basketball/team/_/id/"]',
		'id_capture_regex': '/ncb/teams/roster\?teamId=(.*)',
		'json_file': 'ncaa_basketball.json'
	},
}

def getHtml(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	return urllib2.urlopen(req)

def getRoster(url):
	soup = BeautifulSoup(getHtml(ESPN_ROOT + url['href']), 'html.parser')
	header = soup.find('tr', 'colhead')

	category_elements = header.find_all('td')
	categories = []
	for ele in category_elements:
		categories.append(ele.string)

	players = soup.select('tr.oddrow, tr.evenrow')
	roster = {}
	for player_row in players:
		player = {}
		i = 0
		for td in player_row.find_all('td'):
			player[categories[i]] = td.string
			i += 1
		player['LINK'] = player_row.find('a')['href']
		roster[player['NAME']] = player

	return roster

def get_team_id_from_url(sport, url):
	regex = re.compile(SPORTS[sport]['id_capture_regex'])
	match = regex.match(url['href'])
	return match.groups()[0]

def getRosters(sport):
	soup = BeautifulSoup(getHtml(SPORTS[sport]['base_url']), 'html.parser')
	roster_links = soup.select(SPORTS[sport]['roster_links_selector'])
	team_names = soup.select(SPORTS[sport]['team_names_selector'])

	all_rosters = {}
	i = 0
	for url in roster_links:
		team_id = get_team_id_from_url(sport, url)
		team_name = team_names[i].string
		i += 1
		print("Scraping: " + team_name)
		all_rosters[team_id] = {
			"name": team_name,
			"roster": getRoster(url)
		}

	return all_rosters

def main():
	parser = argparse.ArgumentParser(description='Get rosters for all teams of a specified sport')
	parser.add_argument('-s', '--sport', type=str, help='Sport name (NFL, NBA, NCAA_FOOTBALL, or NCAA_BASKETBALL', default='NFL')
	args = parser.parse_args()
	with open(SPORTS[args.sport]['json_file'], 'w') as outfile:
		json.dump(getRosters(args.sport), outfile)

if __name__ == "__main__":
	main()