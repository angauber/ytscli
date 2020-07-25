import sys
import argparse
import requests
import pyfiglet
from tabulate import tabulate

import config

def getDescription():
	fupper = pyfiglet.figlet_format('Ytscli', font='slant')
	description = '\nA yts torrent search CLI\n'
	print(fupper+description)

def getYtsResults(query, page):
	baseUrl = config.YTS_URL+'/list_movies.json'
	res = requests.get(baseUrl+'?query_term='+query+'&page='+str(page))
	table = []
	if res.status_code == 200 and 'movies' in res.json()['data']:
		table = res.json()['data']['movies']
	results = []
	for el in table:
		for torrent in el['torrents']:
			element = [el['title_long']+' - '+torrent['quality'], torrent['size'], torrent['seeds'], torrent['peers'], 'magnet:?xt=urn:btih:'+torrent['hash']]
			results.append(element)
	return results

def search(query):
	headers = ['Title', 'Size', 'Seeds', 'Peers', 'Magnet']
	yts = getYtsResults(query, 0)
	
	print(tabulate(yts, headers))

if __name__ == '__main__':
	version = '0.1.0'

	parser = argparse.ArgumentParser(getDescription())
	parser.add_argument('query', help='the query string you are searching for', type=str)
	parser.add_argument('-v', '--version', action='version', version='%(prog)s'+version)
	
	args = parser.parse_args()
	search(args.query)
