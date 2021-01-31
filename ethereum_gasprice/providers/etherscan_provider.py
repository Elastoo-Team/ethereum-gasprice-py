from os import getenv
from typing import Dict, Tuple, Optional

import requests

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["EtherscanProvider"]


class EtherscanProvider(BaseGaspriceProvider):
    provider_title = "etherscan"

    def __init__(
            self,
            api_key: str = None,
    ):
        self.api_url: str = "https://api.etherscan.io/api/"
        self.api_key: str = api_key or self._secret_from_env_var()

    def _secret_from_env_var(self) -> Optional[str]:
        return getenv("ETHERSCAN_API_KEY")

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        success = False
        data = self._data_template.copy()

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
            GaspriceStrategy.REGULAR: response_data["result"].get("SafeGasPrice"),
            GaspriceStrategy.FAST: response_data["result"].get("ProposeGasPrice"),
            GaspriceStrategy.FASTEST: response_data["result"].get("FastGasPrice"),
        })

        return success, data
