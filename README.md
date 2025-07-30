# DuckBridge
Lightweight Python library enabling fully pythonic interfacing with the DuckDB extension `httpserver` (extension developed by @quackscience). 

[![PyPI](https://img.shields.io/pypi/v/duckbridge.svg)](https://pypi.org/project/duckbridge/)
[![Build](https://github.com/mhromiak/duckbridge/actions/workflows/cd_pypi_publish.yml/badge.svg)](https://github.com/mhromiak/duckbridge/actions/workflows/cd_pypi_publish.yml)
[![codecov](https://codecov.io/gh/mhromiak/duckbridge/branch/develop/graph/badge.svg)](https://codecov.io/gh/mhromiak/duckbridge)

## What is duckbridge?
DuckDB's httpserver extension turns databases into HTTP OLAP servers; however, setup and access require unix commands and SQL in order to properly set up authentication, install the extension, and communicate. 

`duckbridge` spans this gap, providing a way to natively use `httpserver` with full pythonic scripting. The `DuckDBServer` class acts as the bridge operator, connecting to the database, initializing `httpserver`, and setting authentication values and read/write privileges. `DuckDBClient` provides a tidy handler which stores client-side authentication and endpoint information, ensuring one-factor authentication by way of knowledge while returning information as a Pandas DataFrame. 

## How do I use duckbridge?
Duckbridge is split into two main portions: `DuckbridgeServer`, which handles extension installation/activation, database connection, and client request processing, and `DuckbridgeClient`, which formats and sends requests to an assumed endpoint, unmarshalling returned data into a convenient format (currently only a Pandas DataFrame).

Examples of how to set up a server or client can be found in more depth at ![duckbridge-demo](https://github.com/MHromiak/duckbridge-demo), a repository of tutorials that is constantly being updated.

If you have a use case that you would like to have considered, please ![open an issue](https://github.com/MHromiak/duckbridge-demo/issues) and it will be addressed!

### Quick start copy-and-paste

```python

####################
### Server setup ###
####################
from duckbridge import *
import os

my_ssh_key_auth : str = "mySuperSecretSSHString"
ssh_userpass_auth : str = "username:password" # !!!The colon is mandatory!!!
my_host : str = "127.0.0.1" # Replace with 0.0.0.0 for public ip access
my_port : int = 8080

bridge : DuckbridgeServer = DuckbridgeServer()
# Assumes readonly permissions and that the database doesn't have `httpserver` installed yet
# If an empty string is provided for auth_info, then no security will be used
bridge.start(os.cwd() + "/path/to/db.db", host=my_host, port=my_port, auth_info=my_ssh_key_auth)


####################
### Client setup ###
####################
from duckbridge import *
import pandas as pd

my_username : str = "username"
my_password : str = "password"

client : DuckbridgeClient = DuckbridgeClient(my_host, my_port, my_username, my_password, my_ssh_key_auth)
data : pd.DataFrame = client.execute("Select * from concept limit 3;", auth="ssh")
```
