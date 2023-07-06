import requests
import logging
import argparse
import json


class UrlShortener:
	def __init__(self, args):
		if args.verbose:
			logging.basicConfig(
				level=logging.NOTSET,
				format="%(asctime)+17s ... %(name)-18s : %(levelname)-10s : %(message)s",
				datefmt="%D %I:%M %p"
			)
			self.logger = logging.getLogger(__file__.split('\\')[-1])

		self.url = args.url 
		self.access_token = args.token
		self.verbose = bool(args.verbose)

	def get_shortened_url(self):
		self.endpoint = "https://api-ssl.bitly.com/v4/shorten"
		self.headers = {
			'Authorization': f'Bearer {self.access_token}',
			'Content-type': 'application/json'
		}
		self.data = {'long_url':self.url}

		response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(self.data))
		if response.status_code == 200:
			if self.verbose:
				self.logger.info("Successfully shortened one(1) url.")
			return json.loads(response.content)['link']
		raise Exception(f"Failed. Status code: {response.status_code}")



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Command line helper for a url shortener application.")
	parser.add_argument('-a', '--token', help="Bity access token.", required=True)
	parser.add_argument('-u', '--url', help="The url to be shortened.", required=True)
	parser.add_argument('-v', '--verbose', help="View logs.", action='store_true')
	args = parser.parse_args()

	ins = UrlShortener(args)
	print(ins.get_shortened_url())