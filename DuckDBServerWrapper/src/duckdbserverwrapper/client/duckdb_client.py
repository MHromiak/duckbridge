from duckdbserverwrapper.client.client import Client
from duckdbserverwrapper.enum.authentication_enum import AuthenticationEnum

import requests
import json
import pandas as pd

class DuckDBClient(Client):

	def __init__(self, ssh_host: str, ssh_port: int, ssh_username: str = None, ssh_password: str = None, ssh_key : str = None):
		self.__ssh_host = ssh_host
		self.__ssh_port = ssh_port
		self.__ssh_username = ssh_username
		self.__ssh_password = ssh_password
		self.__ssh_key = ssh_key

	def execute(self, body : str, headers : dict = {'Content-Type': 'application/json'}, auth=AuthenticationEnum.NOTHING):
		authorization = self._handle_authentication(auth, headers)
		connection_string : str = "http://" + self.__ssh_host + ":" + str(self.__ssh_port)

		if authorization:
			try:
				response = requests.post(connection_string, data=body, auth=authorization, headers=headers)
				return self._convert(response)
			except Exception as e:
				raise Exception(f"Error executing request: {e}")
		else:
			try:
				response = requests.post(connection_string, data=body, headers=headers)
				return self._convert(response)
			except Exception as e:
				raise Exception(f"Error executing request: {e}")
	
	def _handle_authentication(self, auth: AuthenticationEnum, headers: dict) -> str:
		if auth.value == AuthenticationEnum.PASSWORD.value:
			return requests.auth.HTTPBasicAuth(self.__ssh_username, self.__ssh_password)
		elif auth.value == AuthenticationEnum.SSH.value:
			headers['X-API-Key'] = self.__ssh_key
			return None
		else:
			return requests.auth.HTTPBasicAuth(None, None)

	def _convert(self, response):
		if response.status_code == 200:
			fetched_data = []
			for data in response.iter_lines():
				if data:
					fetched_data.append(json.loads(data))	
			return pd.DataFrame(fetched_data)
		else:
			raise Exception(f"Error converting request: {response.status_code} - {response.text}")