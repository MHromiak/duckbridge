
## [0.4.1]

### Added/Modified
- Added documentation for all implemented classes
- Updated workflows to automate tes-pypi version bumping and production tagging

## [0.4.0]

### Added/Modified
- Moved changelog to top-level directory for Github display
- Added Github Actions workflow to deploy new versions to PyPI via automation
- Added a .coveragerc for easier unittest coverage calculations
- Completed testing for new logging functionality
- Updated UML class diagram

### Removed
- Removed AuthenticationEnum and Enum module, replacing options with string inputs instead

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