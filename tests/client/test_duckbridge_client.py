from duckbridge import *
from requests.auth import HTTPBasicAuth
from requests import Response
from io import BytesIO
from pandas import DataFrame

import unittest
from unittest.mock import patch

class TestDuckbridgeClient(unittest.TestCase):

	def setUp(self):
		self.client = DuckbridgeClient("127.0.0.1", 8080, "myUsername", "myPassword", "mySSHKey")
		self.server_logger_name = self.client.__class__.logger.name

	def test_handle_authentication_userpass(self):
		response : HTTPBasicAuth = self.client._handle_authentication("userpass", {'Content-Type': 'application/json'})
		self.assertEqual(self.client._DuckbridgeClient__ssh_username, response.username)
		self.assertEqual(self.client._DuckbridgeClient__ssh_password, response.password)

	def test_handle_authentication_ssh(self):
		headers = {'Content-Type': 'application/json', 'X-API-Key' : ''}
		response : HTTPBasicAuth = self.client._handle_authentication("ssh", headers)
		self.assertEqual(self.client._DuckbridgeClient__ssh_key, headers['X-API-Key'])
		self.assertIsNone(response)

	def test_handle_authentication_no_auth(self):
		headers = {'Content-Type': 'application/json', 'X-API-Key' : ''}
		response : HTTPBasicAuth = self.client._handle_authentication("somethingElse", headers)
		self.assertEqual("", headers['X-API-Key'])
		self.assertEqual(None, response.username)
		self.assertEqual(None, response.password)

	def test_convert_with_non_null_response_data(self):
		ndjson = (
			'{"id": 1, "name": "Alice"}\n'
			'{"id": 2, "name": "Bob"}\n'
			'{"id": 3, "name": "Charlie"}\n'
		)
		response : Response = Response()
		response._content = ndjson.encode('utf-8')
		response.raw = BytesIO(response._content)
		response.status_code = 200
		df : DataFrame = self.client._convert(response)
		self.assertIsNotNone(df)
		self.assertEqual("Alice", df.iloc[0]["name"])
		self.assertEqual(1, df.iloc[0]["id"])

	def test_convert_unsuccessful_response(self):
		with self.assertLogs(self.client.__class__.logger.name, level="ERROR") as l:
			response : Response = Response()
			response.status_code = 400
			df : DataFrame = self.client._convert(response)
		self.assertIsNone(df)
		self.assertTrue(l.output[0].split(":")[0] == "ERROR")

	@patch('requests.post')
	def test_execute_auth_success(self, mock_post):
		ndjson = (
			'{"id": 1, "name": "Alice"}\n'
			'{"id": 2, "name": "Bob"}\n'
			'{"id": 3, "name": "Charlie"}\n'
		)
		response : Response = Response()
		response._content = ndjson.encode('utf-8')
		response.raw = BytesIO(response._content)
		response.status_code = 200

		mock_post.return_value = response

		df : DataFrame = self.client.execute("any_body", auth="ssh")
		self.assertIsNotNone(df)
		self.assertEqual("Alice", df.iloc[0]["name"])
		self.assertEqual(1, df.iloc[0]["id"])

	@patch('requests.post')
	def test_execute_auth_exception(self, mock_post):

		mock_post.return_value = None
		mock_post.side_effect = Exception("Some Exception")
		with self.assertLogs(self.client.__class__.logger.name, level="ERROR") as l:
			df = self.client.execute("any_body", auth="ssh")
		self.assertIsNone(df)
		self.assertTrue("ERROR:" + self.client.__class__.logger.name + ":DuckbridgeClient | execute | Error executing request: Some Exception" in l.output)

	@patch('requests.post')
	def test_execute_no_auth_success(self, mock_post):
		ndjson = (
			'{"id": 1, "name": "Alice"}\n'
			'{"id": 2, "name": "Bob"}\n'
			'{"id": 3, "name": "Charlie"}\n'
		)
		response : Response = Response()
		response._content = ndjson.encode('utf-8')
		response.raw = BytesIO(response._content)
		response.status_code = 200

		mock_post.return_value = response

		df : DataFrame = self.client.execute("any_body")
		self.assertIsNotNone(df)
		self.assertEqual("Alice", df.iloc[0]["name"])
		self.assertEqual(1, df.iloc[0]["id"])

	@patch('requests.post')
	def test_execute_no_auth_exception(self, mock_post):

		mock_post.return_value = None
		mock_post.side_effect = Exception("Some Exception")
		with self.assertLogs(self.client.__class__.logger.name, level="ERROR") as l:
			df = self.client.execute("any_body")
		self.assertIsNone(df)
		self.assertTrue("ERROR:" + self.client.__class__.logger.name + ":DuckbridgeClient | execute | Error executing request: Some Exception" in l.output)
	
	
