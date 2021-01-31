Ethereum gasprice: Actual gasprice for ethereum blockchain
=======================================

# Installation

TBD

# Quickstart

```python
from ethereum_gasprice import GaspriceController, GaspriceStrategy

ETHERSCAN_API_KEY = "..."

controller = GaspriceController(etherscan_api_key=ETHERSCAN_API_KEY)
actual_gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)  # output: 69
```

# Documentation

TBD


# License

Ethereum gasprice is licensed under the terms of the MIT License (see the file LICENSE).
