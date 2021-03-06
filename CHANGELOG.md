# Changelog

## [Unreleased]
_

## [0.1.0]
### Added
- retrieve all execsnoop services
- execsnoop/services/<name> for start/stop/restart operations
    - separate systemd management class

- default route '/' to retrieve version and other future info
- bug fixes
- bulk request '/execsnoop/services/_all' to manage all services
- fswatch and tcptracer API endpoints same as for execsnoop
- reset-failed systemd service after each operation execution
- file stats API

### Modified
- move main object adapters (execsnoop and systemd adapters) to a separate class/file
- execsnoop service management
- unified the API responses for execsnoop blueprint

### Removed
- execsnoop/load api call and integrated it to the execsnoop/status api call

## [0.0.4]
### Modified
- package name: change underscore to colon
  - rename config dir accordingly

## [0.0.3]
### Modified
- hotfix: setup procedure in readme

## [0.0.2]
### Modified
- fix configure.sh script for both dev and prod environments
  - also modify and work with config.yml file instead of config_example.yml, because config.yml is in gitignore

### Removed
- configuration of the debug parameter

## [0.0.1]
### Added
- execsnoop related routes
  - get process status utilizing pgrep and psutil
  - load all execsnoop process to objects

- process related routes
  - get arbitrary process status utilizing pgrep and psutil

- redis integration
- docker testing with redis container
- pytests
  - configuration
  - execsnoop instances manipulation

- serialize all existing execsnoop instances

[Unreleased]: https://github.com/tomas321/sneakctl_server/compare/0.1.0...develop
[0.1.0]: https://github.com/tomas321/sneakctl_server/compare/0.0.4...0.1.0
[0.0.4]: https://github.com/tomas321/sneakctl_server/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/tomas321/sneakctl_server/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/tomas321/sneakctl_server/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/tomas321/sneakctl_server/releases/tag/0.0.1
