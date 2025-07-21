
## [0.3.0]

### Added/Modified
- Refactored unit tests to use new logging functionality
- Added suggested scripts for starting a bridge in Render
- Renamed duckdbserverwrapper to duckbridge for conciseness.

## [0.2.0]

### Added/Modified
- Refactored Internal/Remote server logic into a client-server architecture to reflect changing use cases
- Added an authentication enum class to allow for flexible inclusion of different httpserver authentication methods

## [0.1.0]

### Added
- Create Server, DuckDBServer, and DuckDBInternalServer classes
- Add most unit tests for DuckDBInternalServer
- Initialize dependency management with poetry