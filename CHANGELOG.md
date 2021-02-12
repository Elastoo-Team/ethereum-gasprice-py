# Changelog

## [1.2.2] - 2021-02-13

### Changed

- Fixed docs API reference
- Issue [#7](https://github.com/Elastoo-Team/ethereum-gasprice-py/issues/7)
- Issue [#8](https://github.com/Elastoo-Team/ethereum-gasprice-py/issues/8)


## [1.2.1] - 2021-02-11

### Added

- [Docs to readthedocs](https://ethereum-gasprice.readthedocs.io/en/latest/). Special thanks to
  [@Egnod](https://github.com/Egnod)

### Changed

- Poetry core requirements

## [1.2.0] - 2021-02-05

### Added

- [HTTPX](https://github.com/encode/httpx) as http client
- docs in README.md

### Changed

- make web3 dependency options
- refactored sync and async providers
- refactored sync and async controller
- base classes of controller, providers

### Removed

- requests, aiohttp dependencies

## [1.1.0] - 2021-02-01

### Added

- Docstrings
- Etherchain provider

### Changed

- updated requirements.

## [1.0.1] - 2021-02-01

### Added

- Gasprice Controller and providers async implementation

### Changed

- updated README.md with badges and other useful info
- optimized gasprice from all sources method with asyncio.gather

## [1.0.0] - 2021-01-31

### Added

- README.md, pre-commit config

### Changed

- String literals to consts
- Completed type hinting
- updated meta in pyproject.toml

## [0.1.0] - 2021-01-30

### Added

- Initial release.
- Gasprice Controller.
- Etherscan, EthGasPrice and Web3 providers
