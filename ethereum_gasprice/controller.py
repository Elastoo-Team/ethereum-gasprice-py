from typing import Any, Dict, Literal, Optional, Tuple, Type, Union

from eth_utils import from_wei, to_wei

from ethereum_gasprice.consts import EthereumUnit, GaspriceStrategy
from ethereum_gasprice.providers import (
    BaseGaspriceProvider,
    EtherchainProvider,
    EtherscanProvider,
    EthGasStationProvider,
)

__all__ = ["GaspriceController"]


class GaspriceController:
    """Entrypoint for fetching gasprice."""

    def __init__(
        self,
        return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = EthereumUnit.WEI,
        etherscan_api_key: Optional[str] = None,
        ethgasstation_api_key: Optional[str] = None,
        web3_provider_url: Optional[str] = None,
        providers_priority: Tuple[Type[BaseGaspriceProvider]] = (
            EtherscanProvider,
            EthGasStationProvider,
            EtherchainProvider,
        ),
    ):
        """
        :param return_unit: ethereum unit, which
        :param etherscan_api_key: api key for etherscan
        :param ethgasstation_api_key: api key for ethgasstation
        :param web3_provider_url: url for web3
        :param providers_priority: tuple of providers classes, which will be initialized and used in given order
        """
        self.return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = return_unit
        self.providers_priority: Tuple[Type[BaseGaspriceProvider]] = providers_priority

        self.etherscan_api_key: Optional[str] = etherscan_api_key
        self.ethgasstation_api_key: Optional[str] = ethgasstation_api_key
        self.web3_provider_url: Optional[str] = web3_provider_url

        if len(self.providers_priority) < 1:
            raise ValueError("providers priority tuple is empty")

        if self.return_unit not in (EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH):
            raise ValueError("invalid return unit")

    def _init_provider(
        self,
        provider: Type[BaseGaspriceProvider],
    ) -> Any:
        """Initialize provider class with correct parameter.

        :param provider:
        :return:
        """
        if provider == EtherscanProvider:
            return EtherscanProvider(self.etherscan_api_key)
        elif provider == EthGasStationProvider:
            return EthGasStationProvider(self.ethgasstation_api_key)
        elif provider == EtherchainProvider:
            return EtherchainProvider()
        else:
            raise ValueError("no provider implementation found")

    @staticmethod
    def _convert_units(
        unit_from: EthereumUnit = EthereumUnit.GWEI, unit_to: EthereumUnit = EthereumUnit.WEI, value: int = None
    ) -> Optional[int]:
        """Convert gasprice from provider to chosen unit.

        :param unit_from: Origin gasprice unit. Usually it is in gwei
        :param unit_to: Target gasprice unit
        :param value: Gasprice itselt
        :return:
        """
        if value is None or unit_from == unit_to:
            return value
        if unit_to == EthereumUnit.WEI:
            return int(to_wei(value, unit_from))

        return int(from_wei(to_wei(value, unit_from), unit_to))

    def get_gasprice_by_strategy(self, strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST) -> Optional[int]:
        """Get gasprice with chosen strategy from first available provider.

        :param strategy:
        :return:
        """
        for provider in self.providers_priority:
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
        for provider in self.providers_priority:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()
            if not status:
                continue

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

        for provider in self.providers_priority:
            data[provider.provider_title] = {}
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()
            if not status:
                continue

            for k, v in gasprice_data.items():
                gasprice_data[k] = self._convert_units(EthereumUnit.GWEI, self.return_unit, v)

            data[provider.provider_title] = gasprice_data

        return data
