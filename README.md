# DuckBridge
Lightweight Python library enabling fully pythonic interfacing with the DuckDB extension `httpserver` (extension developed by @quackscience). 

[![PyPI](https://img.shields.io/pypi/v/duckbridge.svg)](https://pypi.org/project/duckbridge/)
[![Build](https://github.com/mhromiak/duckbridge/actions/workflows/publish.yml/badge.svg)](https://github.com/mhromiak/duckbridge/actions/workflows/cd_pypi_publish.yml)
[![codecov](https://codecov.io/gh/mhromiak/duckbridge/branch/main/graph/badge.svg)](https://codecov.io/gh/mhromiak/duckbridge)

## What is duckbridge?
DuckDB's httpserver extension turns databases into HTTP OLAP servers; however, setup and access require unix commands and SQL in order to properly set up authentication, install the extension, and communicate. 

`duckbridge` spans this gap, providing a way to natively use `httpserver` with full pythonic scripting. The `DuckDBServer` class acts as the bridge operator, connecting to the database, initializing `httpserver`, and setting authentication values and read/write privileges. `DuckDBClient` provides a tidy handler which stores client-side authentication and endpoint information, ensuring one-factor authentication by way of knowledge while returning information as a Pandas DataFrame. 

## How do I use duckbridge?
TBD

## What about hosting and public access?
TBD