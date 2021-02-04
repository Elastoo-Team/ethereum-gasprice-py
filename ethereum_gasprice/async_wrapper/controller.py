import asyncio
from typing import Any, Dict, Optional, Type, Union

from ethereum_gasprice.async_wrapper.providers import (
    AsyncEtherchainProvider,
    AsyncEtherscanProvider,
    AsyncEthGasStationProvider,
)
from ethereum_gasprice.consts import EthereumUnit, GaspriceStrategy
from ethereum_gasprice.controller import GaspriceController
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["AsyncGaspriceController"]


class AsyncGaspriceController(GaspriceController):
    def __init__(self, **kwargs):
        provider_priority = kwargs.get("provider_priority") or (
            AsyncEtherscanProvider,
            AsyncEthGasStationProvider,
            AsyncEtherchainProvider,
        )
        super().__init__(providers_priority=provider_priority, **kwargs)

    def _init_provider(
        self,
        provider: Type[BaseGaspriceProvider],
    ) -> Any:
        """Initialize provider class with correct parameter.

        :param provider:
        :return:
        """
        if provider == AsyncEtherscanProvider:
            return AsyncEtherscanProvider(self.etherscan_api_key)
        elif provider == AsyncEthGasStationProvider:
            return AsyncEthGasStationProvider(self.ethgasstation_api_key)
        elif provider == AsyncEtherchainProvider:
            return AsyncEtherchainProvider()
        else:
            raise ValueError("no provider implementation found")

    async def get_gasprice_by_strategy(
        self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST
    ) -> Optional[int]:
        """Get gasprice with chosen strategy from first available provider.

        :param strategy:
        :return:
        """
        for provider in self.providers_priority:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = await provider_instance.get_gasprice()
            if not status or gasprice_data.get(strategy) is None:
                continue
            else:
                return self._convert_units(EthereumUnit.GWEI, self.return_unit, gasprice_data[strategy])

        return None

    async def get_gasprices(self) -> Optional[Dict[GaspriceStrategy, Optional[int]]]:
        """Get all gasprice strategies values from first available provider.

        :return:
        """
        for provider in self.providers_priority:
            provider_instance = self._init_provider(provider)

            status, gasprice_data = await provider_instance.get_gasprice()
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            return gasprice_data

        return None

    async def get_gasprice_from_all_sources(self) -> Dict[str, Dict[str, int]]:
        """Get all gasprices from all available providers.

        Uses asyncio.gather to speed up requests

        It is useful when you don't trust single provider and what to verify gasprice with other providers.
        It is a good pratice to calculate an average gasprice for every strategy and take the average gasprice value.

        :return:
        """
        data = {}
        providers = [self._init_provider(provider) for provider in self.providers_priority]
        results = await asyncio.gather(*[provider.get_gasprice() for provider in providers])

        for result, provider in zip(results, providers):
            status, gasprice_data = result
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            data[provider.provider_title] = gasprice_data

        return data
