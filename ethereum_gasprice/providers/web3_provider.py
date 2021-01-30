from os import getenv
from typing import Dict, Tuple, Optional

from web3 import Web3, HTTPProvider, WebsocketProvider, IPCProvider
from eth_utils import currency

from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["Web3Provider"]


class Web3Provider(BaseGaspriceProvider):
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

    def get_gasprice(self) -> Tuple[bool, Dict[str, int]]:
        success = False
        data = {
            "slow": 0,
            "regular": 0,
            "fast": 0,
            "fastest": 0,
        }

        web3 = self._init_web3()

        if not web3:
            return success, data

        success = True
        data.update({
            "regular": int(currency.from_wei(web3.eth.gasPrice, "gwei")),
            "fast": 0,
            "fastest": 0,
        })

        return success, data
