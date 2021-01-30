from os import getenv
from typing import Dict, Tuple, Optional

import requests

from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["EthGasStationProvider"]


class EthGasStationProvider(BaseGaspriceProvider):
    def __init__(
            self,
            api_key: str = None,
    ):
        self.api_url: str = "https://ethgasstation.info/api/ethgasAPI.json"
        self.api_key: str = api_key or self._secret_from_env_var()

    def _secret_from_env_var(self) -> Optional[str]:
        return getenv("ETHGASSTATION_API_KEY")

    def get_gasprice(self) -> Tuple[bool, Dict[str, int]]:
        success = False
        data = {
            "slow": 0,
            "regular": 0,
            "fast": 0,
            "fastest": 0,
        }

        if not self.api_key:
            return success, data

        try:
            response = requests.get(
                url=self.api_url,
                params={"api-key": self.api_key}
            )

        except Exception as e:
            return success, data

        response_data = response.json()

        if response.status_code != 200:
            return success, data

        success = True
        data.update({
            "slow": response_data.get("safeLow"),
            "regular": response_data.get("average"),
            "fast": response_data.get("fast"),
            "fastest": response_data.get("fastest"),
        })

        for k, v in data.items():
            data[k] = int(v) // 10

        return success, data
