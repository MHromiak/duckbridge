from duckbridge.client.client import Client

import requests
import json
import pandas as pd
import logging

class DuckbridgeClient(Client):
	logger = logging.getLogger(__name__)
	logger.addHandler(logging.NullHandler())

	def __init__(self, ssh_host: str, ssh_port: int, ssh_username: str = "", ssh_password: str = "", ssh_key : str = ""):
		self.__ssh_host = ssh_host
		self.__ssh_port = ssh_port
		self.__ssh_username = ssh_username
		self.__ssh_password = ssh_password
		self.__ssh_key = ssh_key

	def execute(self, body : str, headers : dict = {'Content-Type': 'application/json'}, auth="") -> pd.DataFrame:
		authorization = self._handle_authentication(auth, headers)
		connection_string : str = "http://" + self.__ssh_host + ":" + str(self.__ssh_port)

		if authorization:
			try:
				response = requests.post(connection_string, data=body, auth=authorization, headers=headers)
				return self._convert(response)
			except Exception as e:
				self.logger.error("DuckbridgeClient | execute | " + f"Error executing request: {e}")
		else:
			try:
				response = requests.post(connection_string, data=body, headers=headers)
				return self._convert(response)
			except Exception as e:
				self.logger.error("DuckbridgeClient | execute | " + f"Error executing request: {e}")
		
		return None
	
	def _handle_authentication(self, auth: str, headers: dict) -> requests.auth.HTTPBasicAuth:
		if auth == "userpass":
			return requests.auth.HTTPBasicAuth(self.__ssh_username, self.__ssh_password)
		elif auth == "ssh":
			headers['X-API-Key'] = self.__ssh_key
			return None
		else:
			return requests.auth.HTTPBasicAuth(None, None)

	def _convert(self, response) -> pd.DataFrame:
		if response.status_code == 200:
			fetched_data = []
			for data in response.iter_lines():
				if data:
					fetched_data.append(json.loads(data))	
			return pd.DataFrame(fetched_data)
		else:
			self.logger.error("DuckbridgeClient | convert | " + f"Error converting request: {response.status_code} - {response.text}")
			return None