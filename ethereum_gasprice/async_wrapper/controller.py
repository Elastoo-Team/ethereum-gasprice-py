from typing import Dict, Optional, Type, Union

from ethereum_gasprice.async_wrapper.providers import (
    AsyncEtherscanProvider,
    AsyncEthGasStationProvider,
    AsyncWeb3Provider,
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
            AsyncWeb3Provider,
        )
        super().__init__(providers_priority=provider_priority, **kwargs)

    def _init_provider(
        self,
        provider: Type[BaseGaspriceProvider],
    ) -> Union[AsyncEtherscanProvider, AsyncEthGasStationProvider, AsyncWeb3Provider]:
        if provider == AsyncEtherscanProvider:
            return AsyncEtherscanProvider(self.etherscan_api_key)
        elif provider == AsyncEthGasStationProvider:
            return AsyncEthGasStationProvider(self.ethgasstation_api_key)
        elif provider == AsyncWeb3Provider:
            return AsyncWeb3Provider(self.web3_provider_url)
        else:
            raise ValueError("no provider implementation found")

    async def get_gasprice_by_strategy(
        self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST
    ) -> Optional[int]:
        for provider in self.providers_priority:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = await provider_instance.get_gasprice()
            if not status or gasprice_data.get(strategy) is None:
                continue
            else:
                return self._convert_units(EthereumUnit.GWEI, self.return_unit, gasprice_data[strategy])

        return None

    async def get_gasprices(self) -> Optional[Dict[GaspriceStrategy, Optional[int]]]:
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
        data = {}

        for provider in self.providers_priority:
            data[provider.provider_title] = {}
            provider_instance = self._init_provider(provider)
            status, gasprice_data = await provider_instance.get_gasprice()
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            data[provider.provider_title] = gasprice_data

        return data
