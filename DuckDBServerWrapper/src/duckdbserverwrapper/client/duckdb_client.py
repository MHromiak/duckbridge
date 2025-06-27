from duckdbserverwrapper.client.client import Client

import requests
import json
import pandas as pd

class DuckDBClient(Client):

	def __init__(self, ssh_host: str, ssh_port: int, ssh_username: str, ssh_password: str):
		self.__ssh_host = ssh_host
		self.__ssh_port = ssh_port
		self.__ssh_username = ssh_username
		self.__ssh_password = ssh_password


	def execute(self, body : str, headers : dict = {'Content-Type': 'application/json'}):
		try:
			response = requests.post(self.__ssh_host + ":" + str(self.__ssh_port), data=body, headers=headers)
			return self._convert(response)
		except Exception as e:
			raise Exception(f"Error executing request: {e}")
	
	def _convert(self, response):
		if response.status_code == 200:
			fetched_data = []
			for data in response.iter_lines():
				if data:
					fetched_data.append(json.loads(data))	
			return pd.DataFrame(fetched_data)
		else:
			raise Exception(f"Error converting request: {response.status_code} - {response.text}")