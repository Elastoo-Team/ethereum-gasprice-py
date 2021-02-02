from os import getenv
from typing import Dict, Optional, Tuple

from eth_utils import currency
from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["Web3Provider"]


class Web3Provider(BaseGaspriceProvider):
    """Provider for Web3 RPC."""

    provider_title = "web3"
    env_var_title: str = "ETHGASPRICE_WEB3"

    def __init__(self, provider_link: str = None):
        """

        :param provider_link: HTTP, Websocket or IPC provider
        """
        self.provider_link: str = provider_link or getenv(self.env_var_title)

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
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        web3 = self._init_web3()

        if not web3:
            return success, data

        success = True
        data[GaspriceStrategy.REGULAR] = int(currency.from_wei(web3.eth.gasPrice, "gwei"))

        return success, data
