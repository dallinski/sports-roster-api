from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import json
import argparse
import re

ESPN_ROOT = 'https://espn.com'

SPORTS = {
	'NFL': {
		'name': 'nfl',
		'use_id_for_team_names_selector': 'false',
		'base_url': 'http://espn.com/nfl/teams'
	},
	'NBA': {
		'name': 'nba',
		'use_id_for_team_names_selector': 'false',
		'base_url': 'http://espn.com/nba/teams'
	},
	'NCAA_FOOTBALL': {
		'name': 'college-football',
		'use_id_for_team_names_selector': 'true',
		'base_url': 'http://espn.com/college-football/teams'
	},
	'NCAA_BASKETBALL': {
		'name': 'mens-college-basketball',
		'use_id_for_team_names_selector': 'true',
		'base_url': 'http://espn.com/mens-college-basketball/teams'
	},
}


def get_teams_url(sport):
	return '{}/{}/teams'.format(ESPN_ROOT, SPORTS[sport]['name'])


def get_roster_links_selector(sport):
	return '.TeamLinks__Link a[href^="/{}/team/roster/"]'.format(SPORTS[sport]['name'])


def get_team_names_selector(sport):
	use_id_for_name_selector = SPORTS[sport]['use_id_for_team_names_selector'] == 'true'
	return '.TeamLinks a[href^="/{}/team/_/{}/"] h2'.format(SPORTS[sport]['name'], 'id' if use_id_for_name_selector else 'name')


def get_id_capture_regex(sport):
	use_id_for_name_selector = SPORTS[sport]['use_id_for_team_names_selector'] == 'true'
	return '/{}/team/roster/_/{}/(.*){}'.format(SPORTS[sport]['name'], 'id' if use_id_for_name_selector else 'name', '' if use_id_for_name_selector else '/.*')


def get_html(url):
	req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
	return urllib.request.urlopen(req)


def get_roster(url):
	soup = BeautifulSoup(get_html(ESPN_ROOT + url['href']), 'html.parser')
	header = soup.find('tr', 'Table__sub-header')

	category_elements = header.find_all('th')
	categories = []
	for ele in category_elements:
		if ele.string is not None:
			categories.append(ele.string)

	table_content = soup.find('tbody')
	players = table_content.select('tr')
	roster = {}
	for player_row in players:
		player = {}
		i = 0
		for td in player_row.find_all('td'):
			if td.string is not None:
				player[categories[i - 1]] = td.string
			elif td.contents[0].contents[0].string is not None:
				player[categories[i - 1]] = td.contents[0].contents[0].string
			i += 1
		player['LINK'] = player_row.find('a')['href']
		roster[player['Name']] = player

	return roster


def get_team_id_from_url(sport, url):
	regex = re.compile(get_id_capture_regex(sport))
	match = regex.match(url['href'])
	return match.groups()[0]


def get_rosters(sport):
	soup = BeautifulSoup(get_html(get_teams_url(sport)), 'html.parser')
	roster_links = soup.select(get_roster_links_selector(sport))
	team_names = soup.select(get_team_names_selector(sport))

	all_rosters = {}
	i = 0
	for url in roster_links:
		team_id = get_team_id_from_url(sport, url)
		team_name = team_names[i].string
		i += 1
		print("Scraping: " + team_name)
		all_rosters[team_id] = {
			"name": team_name,
			"roster": get_roster(url)
		}

	return all_rosters

def main():
	parser = argparse.ArgumentParser(description='Get rosters for all teams of a specified sport')
	parser.add_argument('-s', '--sport', type=str, help='Sport name (NFL, NBA, NCAA_FOOTBALL, or NCAA_BASKETBALL)', default='NFL')
	args = parser.parse_args()
	sport = args.sport
	with open('{}.json'.format(sport.lower()), 'w') as outfile:
		json.dump(get_rosters(sport), outfile)

if __name__ == "__main__":
	main()
