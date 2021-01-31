from typing import Literal, Optional, Dict, Type, Tuple, Union

from eth_utils import from_wei, to_wei

from ethereum_gasprice.consts import *
from ethereum_gasprice.providers import *

__all__ = ["GaspriceController"]


class GaspriceController:
    def __init__(
            self,
            return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = EthereumUnit.WEI,
            etherscan_api_key: Optional[str] = None,
            ethgasstation_api_key: Optional[str] = None,
            web3_provider_url: Optional[str] = None,
            providers_priority: Tuple[Type[BaseGaspriceProvider]] = (
                    EtherscanProvider, EthGasStationProvider, Web3Provider
            )
    ):
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
    ) -> Union[EtherscanProvider, EthGasStationProvider, Web3Provider]:
        if provider == EtherscanProvider:
            return EtherscanProvider(self.etherscan_api_key)
        elif provider == EthGasStationProvider:
            return EthGasStationProvider(self.ethgasstation_api_key)
        elif provider == Web3Provider:
            return Web3Provider(self.web3_provider_url)
        else:
            raise ValueError("no provider implementation found")

    @staticmethod
    def _convert_units(
            unit_from: EthereumUnit = EthereumUnit.GWEI,
            unit_to: EthereumUnit = EthereumUnit.WEI,
            value: int = None
    ) -> Optional[int]:
        if value is None or unit_from == unit_to:
            return value
        if unit_to == EthereumUnit.WEI:
            return int(to_wei(value, unit_from))

        return int(from_wei(to_wei(value, unit_from), unit_to))

    def get_gasprice_by_strategy(
            self,
            strategy: Union[GaspriceStrategy, str] = GaspriceStrategy.FAST
    ) -> Optional[int]:
        for provider in self.providers_priority:
            provider_instance = self._init_provider(provider)
            status, gasprice_data = provider_instance.get_gasprice()
            if not status or gasprice_data.get(strategy) is None:
                continue
            else:
                return self._convert_units(EthereumUnit.GWEI, self.return_unit, gasprice_data[strategy])

        return None

    def get_gasprices(self) -> Optional[Dict[GaspriceStrategy, Optional[int]]]:
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
