import requests
from decouple import config 
import logging
import json

logging.basicConfig(
	level=logging.NOTSET,
	format="%(asctime)+17s ... %(name)-18s : %(levelname)-10s : %(message)s",
	datefmt="%D %I:%M %p"
)

class UrlShortener:
	def __init__(self):
		self.logger = logging.getLogger(__file__.split('\\')[-1])
		self.access_token = config("BITLY_ACCESS_TOKEN")
		self.endpoint = "https://api-ssl.bitly.com/v4/shorten"
		self.max_retries = 3


	def shorten(self, url):
		self.headers = {
			'Authorization': f'Bearer {self.access_token}',
			'Content-type': 'application/json'
		}
		self.data = { 
			'long_url':url 
		}

		trials = 0
		while trials != self.max_retries:
			response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(self.data))
			trials += 1
			if response.status_code == 200:
				self.logger.info("Successfully shortened one(1) url.")
				return json.loads(response.content)['link']
			else:
				self.logger.info(f"Unsuccesful shorten after {trials} trial(s), retrying...")

		raise Exception(f"Failed. Status code: {response.status_code}")



if __name__=="__main__":
	ins = UrlShortener()
	print(ins.shorten("https://leetcode.com/problems/top-k-frequent-elements/submissions/987274867/"))