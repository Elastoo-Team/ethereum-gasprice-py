Ethereum gasprice: Actual gasprice for ethereum blockchain
=======================================

[![PyPI](https://img.shields.io/pypi/v/ethereum-gasprice)](https://pypi.org/project/ethereum-gasprice/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/ethereum-gasprice)](https://pypi.org/project/ethereum-gasprice/)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FElastoo-Team%2Fethereum-gasprice-py%2Fbadge&style=flat)](https://actions-badge.atrox.dev/Elastoo-Team/ethereum-gasprice-py/goto)

Library for fetching actual ethereum blockchain gasprice from different sources:
[Etherscan Gas Tracker](https://etherscan.io/gastracker), [Eth Gas Station](https://ethgasstation.info/),
[Etherchain Gasprice Oracle](https://www.etherchain.org/tools/gasPriceOracle),
[Web3 RPC Method](https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.gasPrice).

Read more about gas and fee from [this article](https://ethereum.org/en/developers/docs/gas/)

# Installation

```bash
poetry add ethereum-gasprice
```

or

```bash
pip3 install ethereum-gasprice
```

# Quickstart

```python
from ethereum_gasprice import GaspriceController, GaspriceStrategy, EthereumUnit

ETHERSCAN_API_KEY = "..."

# Pass api key to GaspriceController to initialize provider
controller = GaspriceController(
    etherscan_api_key=ETHERSCAN_API_KEY,
    return_unit=EthereumUnit.WEI,
)

# Get gasprice by one of these strategies:
# GaspriceStrategy.SLOW, GaspriceStrategy.REGULAR, GaspriceStrategy.FAST, GaspriceStrategy.FASTEST
actual_gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)  # output: 69000000000

# Get all gasprice straregies from first available source:
actual_gasprices = controller.get_gasprices()  # output: {'slow': 10, 'regular': 15, 'fast': 20, 'fastest': 21}
```

# Documentation

TBD

# License

Ethereum gasprice is licensed under the terms of the MIT License (see the file LICENSE).
