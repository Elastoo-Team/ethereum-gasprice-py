import asyncio
from typing import Any, Dict, Literal, Optional, Tuple, Type, Union

from httpx import AsyncClient

from ethereum_gasprice.consts import EthereumUnit, GaspriceStrategy
from ethereum_gasprice.providers import AsyncEtherchainProvider, AsyncEtherscanProvider, AsyncEthGasStationProvider
from ethereum_gasprice.providers.base import BaseAsyncAPIGaspriceProvider, BaseGaspriceProvider

from .sync_wrapper import GaspriceController

__all__ = ["AsyncGaspriceController"]


class AsyncGaspriceController(GaspriceController):
    """Entrypoint for fetching gasprice."""

    def __init__(
        self,
        *,
        return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = EthereumUnit.WEI,
        providers: Tuple[Type[BaseGaspriceProvider]] = (
            AsyncEtherscanProvider,
            AsyncEthGasStationProvider,
            AsyncEtherchainProvider,
        ),
        settings: Optional[Dict[str, Optional[str]]] = None,
    ):
        super().__init__(return_unit=return_unit, providers=providers, settings=settings)

    async def __aenter__(self):
        """Init http client and return self."""
        self._http_client = self._init_http_client()
        return self

    async def __aexit__(self, *args):
        if not self._http_client.is_closed:
            await self._http_client.aclose()

    @classmethod
    def _init_http_client(cls) -> AsyncClient:
        return AsyncClient()

    def _init_provider(
        self,
        provider: Type[BaseGaspriceProvider],
    ) -> Any:
        if not issubclass(provider, BaseAsyncAPIGaspriceProvider):
            raise TypeError(
                f"provider must be instance of {BaseAsyncAPIGaspriceProvider.__name__} and implement async functions"
            )

        return super()._init_provider(provider)

    # TODO follow DRY, unify functions
    async def get_gasprice_by_strategy(
        self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST
    ) -> Optional[int]:
        """Get gasprice with chosen strategy from first available provider.

        :param strategy:
        :return:
        """
        for provider in self.providers:
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
        for provider in self.providers:
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
        providers = [self._init_provider(provider) for provider in self.providers]
        results = await asyncio.gather(*[provider.get_gasprice() for provider in providers])

        for result, provider in zip(results, providers):
            status, gasprice_data = result
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            data[provider.title] = gasprice_data

        return data
