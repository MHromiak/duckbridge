from duckdbserverwrapper import *
from unittest.mock import patch, call

import os
import pathlib as pl
import unittest

class TestInternalServer(unittest.TestCase):

	def setUp(self):
		self.internal_server = DuckDBInternalServer()
		self.internal_server.host = ""
		self.internal_server.port = 0

	def tearDown(self):
		self.internal_server._DuckDBInternalServer__close_connection()
		os.remove(os.getcwd() + "\\temp.db")

	def assertIsFile(self, path):
		if not pl.Path(path).resolve().is_file():
			raise AssertionError("File does not exist: %s" % str(path))

	#TODO - make root path-agnostic. Locate it in the resources folder
	def test_create_connection_valid_connection(self):
		self.internal_server._DuckDBInternalServer__create_connection(os.getcwd() + "\\temp.db")
		self.assertIsFile(os.getcwd() + "\\temp.db")
		self.assertIsNotNone(self.internal_server.connection)

	@patch('builtins.print')
	def test_setup_extension(self, mock_setup_print):
		self.internal_server._DuckDBInternalServer__create_connection(os.getcwd() + "\\temp.db")
		self.internal_server._setup_extension(self.internal_server.connection)
		mock_setup_print.assert_called_once_with(constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	@patch('builtins.print')
	def test_load_httpserver_when_setup(self, mock_load_print):
		self.internal_server._DuckDBInternalServer__create_connection(os.getcwd() + "\\temp.db")
		self.internal_server._setup_extension(self.internal_server.connection)
		self.internal_server._DuckDBInternalServer__load_httpserver()
		mock_load_print.assert_has_calls([call(constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE), call(constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)])

	# #TODO: Should this raise an exception if the setup hasn't yet been called?
	# def test_load_httpserver_when_not_yet_setup(self):
	# 	self.internal_server._DuckDBInternalServer__create_connection(os.getcwd() + "\\temp.db")
	# 	with self.assertRaises(Exception) as cm:
	# 		self.internal_server._DuckDBInternalServer__load_httpserver()
	# 	self.assertEqual(str(cm.exception), constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)

	@patch('builtins.print')
	def test_start(self, mock_start_print):
		self.internal_server.start(os.getcwd() + "\\temp.db", extension_downloaded=False)
		self.assertEqual("localhost", self.internal_server.host)
		self.assertEqual(8080, self.internal_server.port)
		mock_start_print.assert_has_calls([call(constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE),
									 call(constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE),
									 call(constants.SERVER_START_SUCCESS_MESSAGE)])
	
		
if __name__ == "__main__":
	unittest.main()
	


