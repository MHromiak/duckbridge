from duckbridge.client.client import Client

import requests
import json
import pandas as pd
import logging

class DuckbridgeClient(Client):
	"""
	A class enabling Python HTTP querying of a DuckDB
	server running the httpserver extension.

	Attributes
	----------
	__ssh_port : int
		The exposed port of the server host ip.
	__ssh_host : str
		The server host ip exposed to requests.
	__ssh_username : str, optional
		Username used in user:pass authentication
	__ssh_password : str, optional
		Password used in user:pass authentication
	__ssh_key : str, optional
		SSH key string used in X-API-Key header authentication


	Methods
	-------
	execute(body, headers, auth) -> pd.DataFrame | None:
		Send an HTTP request to a registered host and port, 
		retrieving data in the form of a DataFrame.
	_handle_authentication(auth, headers) -> requests.auth.HTTPBasicAuth | None:
		Populate headers or create an authentication object based on
			authentication type.
	_convert(response) -> pd.DataFrame | None:
		Convert fetched response data to a pandas DataFrame.
	"""

	logger = logging.getLogger(__name__)
	logger.addHandler(logging.NullHandler())

	def __init__(self, ssh_host: str, ssh_port: int, ssh_username: str = "", ssh_password: str = "", ssh_key : str = ""):
		self.__ssh_host = ssh_host
		self.__ssh_port = ssh_port
		self.__ssh_username = ssh_username
		self.__ssh_password = ssh_password
		self.__ssh_key = ssh_key

	def execute(self, body : str, headers : dict = {'Content-Type': 'application/json'}, auth="") -> pd.DataFrame | None:
		"""
		Send an HTTP request to a registered host and port, 
		retrieving data in the form of a DataFrame.

		Parameters
		----------
			body : str - SQL query to be run on the database.
			headers : dict - Dictionary of request headers. Defaults
				to content type.
			auth : str - Type of authentication to be used. Accepted values are
				'ssh', 'userpass'. Other values assume no authentication.
		
		Returns
		-------
			pandas.DataFrame | None - DataFrame of retrieved information. Returns
				an empty DataFrame if no data was retrieved, or None upon
				failure.
		"""
		authorization = self._handle_authentication(auth, headers)
		connection_string : str = "http://" + self.__ssh_host + ":" + str(self.__ssh_port)

		if authorization:
			try:
				response : requests.Response = requests.post(connection_string, data=body, auth=authorization, headers=headers)
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
	
	def _handle_authentication(self, auth: str, headers: dict) -> requests.auth.HTTPBasicAuth | None:
		"""
		Populate headers or create an authentication object based on
			authentication type.

		Parameters
		----------
			headers : dict - Dictionary of request headers. Populated with
			X-API-KEY header if authentication is 'ssh".
			auth : str - Type of authentication to be used. Accepted values are
				'ssh', 'userpass'. Other values assume no authentication.
		
		Returns
		-------
			requests.auth.HTTPBasicAuth | None - HTTPBasicAuth object. None is returned
				upon ssh authentication as this requires only header additions.
		"""
		if auth == "userpass":
			return requests.auth.HTTPBasicAuth(self.__ssh_username, self.__ssh_password)
		elif auth == "ssh":
			headers['X-API-Key'] = self.__ssh_key
			return None
		else:
			return requests.auth.HTTPBasicAuth(None, None)

	def _convert(self, response) -> pd.DataFrame | None:
		"""
		Convert fetched response data to a pandas DataFrame.

		Parameters
		----------
			response : requests.Response - Response object containing a 
				status code, body, and headers among other fields.
		
		Returns
		-------
			pandas.DataFrame | None - DataFrame of retrieved data. None is returned
				upon parsing error.
		"""
		if response.status_code == 200:
			fetched_data = []
			for data in response.iter_lines():
				if data:
					fetched_data.append(json.loads(data))	
			return pd.DataFrame(fetched_data)
		else:
			self.logger.error("DuckbridgeClient | convert | " + f"Error converting request: {response.status_code} - {response.text}")
			return None