from typing import Dict, Optional, Tuple

from eth_utils import currency
from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["Web3Provider"]


class Web3Provider(BaseGaspriceProvider):
    """Provider for Web3 RPC."""

    title = "web3"
    secret_env_var_title: str = "ETHGASPRICE_WEB3_SECRET"

    def _init_web3(self) -> Optional["Web3"]:
        web_provider = self.get_secret()

        if not web_provider:
            return None
        elif web_provider.startswith("http"):
            return Web3(HTTPProvider(web_provider))
        elif web_provider.startswith("ws"):
            return Web3(WebsocketProvider(web_provider))
        elif web_provider.endswith("ipc"):
            return Web3(IPCProvider(web_provider))
        else:
            return None

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        web3 = self._init_web3()

        if not web3:
            return success, data

        data[GaspriceStrategy.REGULAR] = int(currency.from_wei(web3.eth.gasPrice, "gwei"))
        success = True

        return success, data
