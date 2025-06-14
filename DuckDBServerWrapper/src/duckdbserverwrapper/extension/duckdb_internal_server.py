from duckdbserverwrapper.server.duckdb_server import DuckDBServer
from duckdbserverwrapper.constant.constants import Constants

import duckdb
import pandas as pd
import requests
import json

class DuckDBInternalServer(DuckDBServer):

	def __init__(self):
		self.connection = None
		self.port = None
		self.host = None

	def start(self, path: str, host : str = "localhost", port : int = 8080, readonly = True, extension_downloaded = True):
		self.__create_connection(path)
		self.host = host
		self.port = port

		if not extension_downloaded:
			self._setup_extension(self.connection)
			extension_downloaded = True

		if readonly:
			self.__load_httpserver()
			
		self.connection.execute(Constants.HTTPSERVER_START_QUERY.format(host=host, port=port))
		print(Constants.SERVER_START_SUCCESS_MESSAGE)

	def stop(self):
			self.__load_httpserver()
			self.connection.execute(Constants.HTTPSERVER_STOP_QUERY)
			print(Constants.SERVER_STOP_SUCCESS_MESSAGE)
			self.__close_connection()

	#TODO: Remove this functionality and move to a client
	def execute(self, url : str, body : str, headers : dict = {'Content-Type': 'application/json'}):
		response = requests.post(url, data=body, headers=headers)
		return self.__convert(response)

	def _setup_extension(self, connection):
		connection.execute(Constants.HTTPSERVER_PLUGIN_DOWNLOAD_QUERY)
		print(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)
	
	def __convert(self, response):
		if response.status_code == 200:
			fetched_data = []
			for data in response.iter_lines():
				if data:
					fetched_data.append(json.loads(data))	
			return pd.DataFrame(fetched_data)
		else:
			raise Exception(f"Error executing request: {response.status_code} - {response.text}")

	def __create_connection(self, path : str):
		try:
			self.connection = duckdb.connect(path)
		except Exception as e:
			raise Exception("Could not create connection to DuckDB database. Exception: " + e)
		
	def __close_connection(self):
		try:
			self.connection.close()
			self.connection= None
			print(Constants.CLOSE_CONNECTION_SUCCESS_MESSAGE.format(host=self.host, port=self.port))
		except Exception as e:
			raise Exception("Exception encountered when attempting to close DB connection to " + self.host + ":" + str(self.port) \
				+ ". Connection may still be open. Exception: " + e)
		
	def __load_httpserver(self):
		try:
			self.connection.execute(Constants.LOAD_HTTPSERVER_QUERY)
			print(Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)
		except Exception as e:
			raise Exception(Constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)