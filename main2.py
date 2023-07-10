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
		self.verbose = args.verbose
		self.max_retries = args.trials 

	def get_shortened_url(self):
		self.endpoint = "https://api-ssl.bitly.com/v4/shorten"
		self.headers = {
			'Authorization': f'Bearer {self.access_token}',
			'Content-type': 'application/json'
		}
		self.data = {'long_url':self.url}

		trials = 0
		while trials < self.max_retries:
			response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(self.data))
			trials += 1
			if response.status_code == 200:
				if self.verbose:
					self.logger.info("Successfully shortened one(1) url.")
				return json.loads(response.content)['link']
			if self.verbose:
				self.logger.info(f"Unsuccesful shorten after {trials} trial(s), retrying...")

		raise Exception(f"Failed. Status code: {response.status_code}")



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Command line helper for a url shortener application.")
	parser.add_argument('-a', '--token', help="Bity access token.")
	parser.add_argument('-u', '--url', help="The url to be shortened.")
	parser.add_argument('-t', '--trials', help="Maximum number of retries.", nargs='?', const=float('inf'), default=3, type=int)
	parser.add_argument('-v', '--verbose', help="View logs.", action='store_true')
	args = parser.parse_args()

	if args.token and args.url:
		ins = UrlShortener(args)
		print(ins.get_shortened_url())
	else:
		filename = __file__.split('\\')[-1]
		print(f"This application has a CLI, run `python {filename} -h` to view the help option.")