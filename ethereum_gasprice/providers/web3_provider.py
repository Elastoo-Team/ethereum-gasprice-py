from os import getenv
from typing import Dict, Tuple, Optional

from eth_utils import currency
from web3 import Web3, HTTPProvider, WebsocketProvider, IPCProvider

from ethereum_gasprice.providers.base import BaseGaspriceProvider
from ethereum_gasprice.consts import GaspriceStrategy

__all__ = ["Web3Provider"]


class Web3Provider(BaseGaspriceProvider):
    provider_title = "web3"

    def __init__(
            self,
            provider_link: str = None
    ):
        self.provider_link: str = provider_link or self._secret_from_env_var()

    def _secret_from_env_var(self) -> Optional[str]:
        return getenv("WEB3_PROVIDER")

    def _init_web3(self) -> Optional[Web3]:
        if not self.provider_link:
            return None
        elif self.provider_link.startswith("http"):
            return Web3(HTTPProvider(self.provider_link))
        elif self.provider_link.startswith("ws"):
            return Web3(WebsocketProvider(self.provider_link))
        elif self.provider_link.endswith("ipc"):
            return Web3(IPCProvider(self.provider_link))
        else:
            return None

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        success = False
        data = self._data_template.copy()

        web3 = self._init_web3()

        if not web3:
            return success, data

        success = True
        data[GaspriceStrategy.REGULAR] = int(currency.from_wei(web3.eth.gasPrice, "gwei"))

        return success, data
