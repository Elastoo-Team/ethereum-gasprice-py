from os import getenv
from typing import Dict, Tuple, Optional

import requests

from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["EtherscanProvider"]


class EtherscanProvider(BaseGaspriceProvider):
    provider = "etherscan"

    def __init__(
            self,
            api_key: str = None,
    ):
        self.api_url: str = "https://api.etherscan.io/api/"
        self.api_key: str = api_key or self._secret_from_env_var()

    def _secret_from_env_var(self) -> Optional[str]:
        return getenv("ETHERSCAN_API_KEY")

    def get_gasprice(self) -> Tuple[bool, Dict[str, int]]:
        success = False
        data = {
            "slow": 0,
            "regular": 0,
            "fast": 0,
            "fastest": 0,
        }
        try:
            response = requests.get(
                url=self.api_url,
                params={
                    "module": "gastracker",
                    "action": "gasoracle",
                    "apikey": self.api_key
                })
        except Exception as e:
            return success, data

        response_data = response.json()

        if not response_data.get("status") == "1":
            return success, data

        success = True
        data.update({
            "regular": response_data["result"].get("SafeGasPrice"),
            "fast": response_data["result"].get("ProposeGasPrice"),
            "fastest": response_data["result"].get("FastGasPrice"),
        })

        return success, data
