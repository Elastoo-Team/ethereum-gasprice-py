ethereum_gasprice_py
============================================================

Library for fetching actual ethereum blockchain gasprice from different sources:

* Etherscan Gas Tracker - https://etherscan.io/gastracker

* Eth Gas Station - https://ethgasstation.info/

* Etherchain Gasprice Oracle - https://www.etherchain.org/tools/gasPriceOracle

* Web3 RPC Method - https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.gasPrice)

Read more about gas and fee from - https://ethereum.org/en/developers/docs/gas/

Installation
-------------

.. code-block:: bash

    poetry add ethereum-gasprice


or

.. code-block:: bash

    pip3 install ethereum-gasprice


Quickstart
------------

.. code-block:: python

    from ethereum_gasprice import GaspriceController, GaspriceStrategy, EthereumUnit
    from ethereum_gasprice.providers import EtherscanProvider

    ETHERSCAN_API_KEY = "..."

    # Pass api key to GaspriceController to initialize provider
    controller = GaspriceController(
        settings={EtherscanProvider.title: ETHERSCAN_API_KEY},
    )

    # Get gasprice by one of these strategies:
    gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)
    print(gasprice)  # output: 69


Usage
-----

Gasprice controller
********************

Main entrypoint to fetching gasprice from providers. Has sync and async implementations.

It is recommended to initialize controller with `with ... as controller:` method

.. code-block:: python

    from ethereum_gasprice import GaspriceController, AsyncGaspriceController

Parameters:

* `return_unit` - return gasprice in given ethereum unit. It is recommended to use `EthereumUnit` class
  from `ethereum_gasprice.consts` to choose unit
* `providers` - tuple of providers what will be used in fetching gasprice. Order of providers is important

- gasprice will be fetch in given priority. Providers must be a subclass of `BaseGaspriceProvider`

* `settings` - dict containing secrets for providers. Key is provider title slug, value is a secret for provider.

.. code-block:: python

    from ethereum_gasprice.consts import EthereumUnit
    from ethereum_gasprice.providers import (
        EtherscanProvider, EthGasStationProvider, AsyncEtherscanProvider, AsyncEthGasStationProvider
    )

    settings = {
        EtherscanProvider.title: "API_KEY",
        EthGasStationProvider.title: "API_KEY"
    }

    sync_providers = (EtherscanProvider, EthGasStationProvider)
    async_providers = (AsyncEtherscanProvider, AsyncEthGasStationProvider)

    with GaspriceStrategy(
            return_unit=EthereumUnit.GWEI,
            providers=sync_providers,
            settings=settings
    ) as controller:
        # Do something
        pass

    async with  AsyncGaspriceController(
            return_unit=EthereumUnit.WEI,
            providers=async_providers,
            settings=settings
    ) as async_controller:
        # Do something
        pass


Methods
*********

* `.get_gasprice_by_strategy()` - get gasprices from first available provider and return only one gasprice strategy.

available strategies: slow (`GaspriceStrategy.SLOW`), regular (`GaspriceStrategy.REGULAR`),
fast (`GaspriceStrategy.FAST`), fastest (`GaspriceStrategy.FASTEST`).

Some providers does not have info for some strategies. For example, Etherscan does not provide gasprice for slow
strategy.

In any case method will return dict with these for strategies. If fail case strategy (when all provides is unavailable)
dict with `None` values will be returned.

.. code-block:: python

    from ethereum_gasprice.consts import GaspriceStrategy

    gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)  # type: int, example: 69

* `.get_gasprices()` - gets gasprices for all strategies from first available provider. Returns a dict.

.. code-block:: python

    gasprices = await async_controller.get_gasprices()  # type: dict
    print(gasprices)

    # {'slow': None, 'regular': 17, 'fast': 19, 'fastest': 20}

* `.get_gasprice_from_all_sources()` - get gasprices for all strategies from all available provider.

It can be useful to calculate an average gasprice value from all providers to get the most objective gasprice value.

.. code-block:: python

    gasprices = controller.get_gasprice_from_all_sources()  # type: dict
    print(gasprices)
    # {
    #   'etherscan': {'slow': None, 'regular': 17, 'fast': 19, 'fastest': 29},
    #   'ethgasstation': {'slow': 16, 'regular': 17, 'fast': 19, 'fastest': 20}
    # }



Contents
==========================

Practice
----------------
Coming Soon

.. toctree::
   :maxdepth: 3

API Reference
-------------

.. toctree::
   :maxdepth: 3

   api



Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
