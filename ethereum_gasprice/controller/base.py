from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional, Sequence, Type, Union

from eth_utils import from_wei, to_wei
from httpx import AsyncClient, Client

from ethereum_gasprice.consts import EthereumUnit, GaspriceStrategy
from ethereum_gasprice.providers import BaseGaspriceProvider

__all__ = ["BaseGaspriceController"]


class BaseGaspriceController(ABC):
    def __init__(
        self,
        *,
        return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI] = EthereumUnit.WEI,
        providers: Sequence[Type[BaseGaspriceProvider]] = (),
        settings: Optional[Dict[str, Optional[str]]] = None
    ):
        """
        :param return_unit: ethereum unit, which
        :param providers: tuple of providers classes, which will be initialized and used in given order
        :param settings: Secrets for providers
        """
        self.return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI] = return_unit
        self.providers: Sequence[Type[BaseGaspriceProvider]] = providers

        self._http_client: Optional[Union[Client, AsyncClient]] = None

        if len(self.providers) < 1:
            raise ValueError("providers priority tuple is empty")

        if self.return_unit not in (EthereumUnit.WEI, EthereumUnit.GWEI):
            raise ValueError("invalid return unit")

        if not settings:
            self.settings = {provider.title: None for provider in providers}
        else:
            self.settings = settings

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass

    @abstractmethod
    def _init_http_client(self):
        pass

    @property
    def http_client(self):
        if not self._http_client:
            self._http_client = self._init_http_client()

        return self._http_client

    def _init_provider(
        self,
        provider: Type[BaseGaspriceProvider],
    ) -> Any:
        """Initialize provider class with secret (e.g. api key) and client.

        :param provider:
        """
        return provider(secret=self.settings.get(provider.title), client=self.http_client)

    @staticmethod
    def _convert_units(
        unit_from: EthereumUnit = EthereumUnit.GWEI, unit_to: EthereumUnit = EthereumUnit.WEI, value: int = None
    ) -> Optional[int]:
        """Convert gasprice from provider to chosen unit.

        :param unit_from: Origin gasprice unit. Usually it is in gwei
        :param unit_to: Target gasprice unit
        :param value: Gasprice itselt
        """
        if value is None:
            return None
        elif unit_from == unit_to:
            return int(value)
        elif unit_to == EthereumUnit.WEI:
            return int(to_wei(value, unit_from))
        else:
            return int(from_wei(to_wei(value, unit_from), unit_to))

    @abstractmethod
    def get_gasprice_by_strategy(self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST) -> Optional[int]:
        """Get gasprice with chosen strategy from first available provider.

        :param strategy: strategy class or identifier (str)
        """

    @abstractmethod
    def get_gasprices(self) -> Optional[Dict[GaspriceStrategy, Optional[int]]]:
        """Get all gasprice strategies values from first available provider."""

    @abstractmethod
    def get_gasprice_from_all_sources(self) -> Dict[str, Dict[str, int]]:
        """Get all gasprices from all available providers.

        It is useful when you don't trust single provider and what to
        verify gasprice with other providers. It is a good pratice to
        calculate an average gasprice for every strategy and take the
        average gasprice value.
        """
