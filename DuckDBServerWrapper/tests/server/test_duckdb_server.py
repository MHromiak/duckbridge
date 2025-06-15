from duckdbserverwrapper import *
from duckdbserverwrapper.constant.constants import Constants
from unittest.mock import patch, call

import os
import pathlib as pl
import unittest

class TestInternalServer(unittest.TestCase):

	def setUp(self):
		self.internal_server = DuckDBServer()
		self.internal_server.host = ""
		self.internal_server.port = 0

	def tearDown(self):
		self.internal_server._DuckDBServer__close_connection()
		os.remove(os.getcwd() + "\\temp.db")

	def assertIsFile(self, path):
		if not pl.Path(path).resolve().is_file():
			raise AssertionError("File does not exist: %s" % str(path))

	#TODO - make root path-agnostic. Locate it in the resources folder
	def test_create_connection_valid_connection(self):
		self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
		self.assertIsFile(os.getcwd() + "\\temp.db")
		self.assertIsNotNone(self.internal_server.connection)

	@patch('builtins.print')
	def test_setup_extension(self, mock_setup_print):
		self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
		self.internal_server._setup_extension(self.internal_server.connection)
		mock_setup_print.assert_called_once_with(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	@patch('builtins.print')
	def test_load_httpserver_when_setup(self, mock_load_print):
		self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
		self.internal_server._setup_extension(self.internal_server.connection)
		self.internal_server._DuckDBServer__load_httpserver()
		mock_load_print.assert_has_calls([call(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE), call(Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)])

	@patch('builtins.print')
	def test_start(self, mock_start_print):
		self.internal_server.start(os.getcwd() + "\\temp.db", extension_downloaded=False)
		self.assertEqual("localhost", self.internal_server.host)
		self.assertEqual(8080, self.internal_server.port)
		mock_start_print.assert_has_calls([call(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE),
									 call(Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE),
									 call(Constants.SERVER_START_SUCCESS_MESSAGE)])
	
		
if __name__ == "__main__":
	unittest.main()
	


