from bs4 import BeautifulSoup
from datetime import date
import os
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import argparse
import re

ESPN_ROOT = 'http://espn.go.com'

SPORTS = {
	'NFL': {
		'base_url': 'http://espn.go.com/nfl/teams',
		'team_names_selector': '.logo-nfl-medium h5 a[href^="http://www.espn.com/nfl/team/_/name/"]',
		'id_capture_regex': '/nfl/team/roster/_/name/(.*)/.*',
		'json_file': 'nfl.json'
	},
	'NBA': {
		'base_url': 'http://espn.go.com/nba/teams',
		'team_names_selector': '.logo-nba-medium h5 a[href^="http://www.espn.com/nba/team/_/name/"]',
		'id_capture_regex': '/nba/teams/roster\?team=(.*)',
		'json_file': 'nba.json'
	},
	'NCAA_FOOTBALL': {
		'base_url': 'http://espn.go.com/college-football/teams',
		'team_names_selector': '.medium-logos h5 a[href^="http://www.espn.com/college-football/team/_/id/"]',
		'id_capture_regex': '/ncf/teams/roster\?teamId=(.*)',
		'json_file': 'ncaa_football.json'
	},
	'NCAA_BASKETBALL': {
		'base_url': 'http://espn.go.com/mens-college-basketball/teams',
		'team_names_selector': '.medium-logos h5 a[href^="http://www.espn.com/mens-college-basketball/team/_/id/"]',
		'id_capture_regex': '/ncb/teams/roster\?teamId=(.*)',
		'json_file': 'ncaa_basketball.json'
	},
}

def getHtml(url):
	req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	return urllib.request.urlopen(req)

def getImage(url):
	soup = BeautifulSoup(getHtml(url), 'html.parser')
	sub_branding_span = soup.findAll("span", { "class" : "brand-logo" })
	img_tags = soup.select('span.brand-logo img')
	urllib.request.urlretrieve(img_tags[0].get("src"), "images/" + os.path.basename(re.sub('&h=150&w=150', '', img_tags[0].get("src"))))

def get_team_id_from_url(sport, url):
	regex = re.compile(SPORTS[sport]['id_capture_regex'])
	match = regex.match(url['href'])
	return match.groups()[0]

def getImages(sport):
	soup = BeautifulSoup(getHtml(SPORTS[sport]['base_url']), 'html.parser')
	team_names = soup.select(SPORTS[sport]['team_names_selector'])

	all_rosters = {}
	i = 0
	for url in team_names:
		print(("Scraping: " + url.contents[0]))
		getImage(url.get("href"))

def main():
	parser = argparse.ArgumentParser(description='Get images for all teams of a specified sport')
	parser.add_argument('-s', '--sport', type=str, help='Sport name (NFL, NBA, NCAA_FOOTBALL, or NCAA_BASKETBALL', default='NFL')
	args = parser.parse_args()
	getImages(args.sport)

if __name__ == "__main__":
	main()