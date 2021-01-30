from typing import Literal, Optional, Dict

from ethereum_gasprice.consts import *
from ethereum_gasprice.providers import *

__all__ = ["GaspriceController"]


class GaspriceController:
    def __init__(
            self,
            etherscan_api_key: str = None,
            ethgasstation_api_key: str = None,
            web3_provider_url: str = None,
            return_unit: Literal[EthereumUnit.WEI, EthereumUnit.GWEI, EthereumUnit.ETH] = EthereumUnit.WEI,
            providers: tuple = (EtherscanProvider, EthGasStationProvider, Web3Provider)
    ):
        self.return_unit: str = return_unit
        self.providers: tuple = providers

        self.etherscan_api_key: Optional[str] = etherscan_api_key
        self.ethgasstation_api_key: Optional[str] = ethgasstation_api_key
        self.web3_provider_url: Optional[str] = web3_provider_url

    def get_gasprice_by_strategy(self, strategy: GaspriceStrategy = GaspriceStrategy.FAST) -> int:
        pass

    def get_gasprices(self) -> Dict[str, int]:
        pass

    def get_gasprice_from_all_sources(self) -> Dict[str, Dict[str, int]]:
        pass
