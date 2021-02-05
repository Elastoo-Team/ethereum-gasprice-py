from typing import Dict, Literal, Optional, Tuple, Type, Union

from httpx import Client

from ethereum_gasprice.consts import EthereumUnit, GaspriceStrategy
from ethereum_gasprice.providers import EtherchainProvider, EtherscanProvider, EthGasStationProvider
from ethereum_gasprice.providers.base import BaseGaspriceProvider

from .base import BaseGaspriceController

__all__ = ["GaspriceController"]


class GaspriceController(BaseGaspriceController):
    """Entrypoint for fetching gasprice."""

    def __init__(
        self,
        *,
        return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = EthereumUnit.WEI,
        providers: Tuple[Type[BaseGaspriceProvider]] = (
            EtherscanProvider,
            EthGasStationProvider,
            EtherchainProvider,
        ),
        settings: Optional[Dict[str, Optional[str]]] = None
    ):
        super().__init__(return_unit=return_unit, providers=providers, settings=settings)

    def __enter__(self):
        """Init http client and return self."""
        self._http_client = self._init_http_client()
        return self

    def __exit__(self, *args):
        if not self._http_client.is_closed:
            self._http_client.close()

    @classmethod
    def _init_http_client(cls) -> Client:
        return Client()

    # TODO follow DRY, unify functions
    def get_gasprice_by_strategy(self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST) -> Optional[int]:
        """Get gasprice with chosen strategy from first available provider.

        :param strategy:
        :return:
        """
        for provider in self.providers:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()
            if not status or gasprice_data.get(strategy) is None:
                continue
            else:
                return self._convert_units(EthereumUnit.GWEI, self.return_unit, gasprice_data[strategy])

        return None

    def get_gasprices(self) -> Optional[Dict[GaspriceStrategy, Optional[int]]]:
        """Get all gasprice strategies values from first available provider.

        :return:
        """
        for provider in self.providers:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()

            if not status:
                return gasprice_data

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            return gasprice_data

        return None

    def get_gasprice_from_all_sources(self) -> Dict[str, Dict[str, int]]:
        """Get all gasprices from all available providers.

        It is useful when you don't trust single provider and what to verify gasprice with other providers.
        It is a good pratice to calculate an average gasprice for every strategy and take the average gasprice value.

        :return:
        """
        data = {}

        for provider in self.providers:
            data[provider.title] = {}
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            data[provider.title] = gasprice_data

        return data
