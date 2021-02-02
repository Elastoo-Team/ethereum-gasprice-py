from os import getenv
from typing import Dict, Optional, Tuple

import requests

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["EthGasStationProvider"]


class EthGasStationProvider(BaseGaspriceProvider):
    """Provider for Eth Gas Station (https://ethgasstation.info/)"""

    provider_title: str = "ethgasstation"
    api_url: str = "https://ethgasstation.info/api/ethgasAPI.json"
    env_var_title: str = "ETHGASPRICE_ETHGASSTATION"

    def __init__(
        self,
        api_key: str = None,
    ):
        self.api_key: str = api_key or getenv(self.env_var_title)

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        if not self.api_key:
            return success, data

        try:
            response = requests.get(url=self.api_url, params={"api-key": self.api_key})

        except Exception:
            return success, data

        response_data = response.json()

        if response.status_code != 200:
            return success, data

        success = True
        data.update(
            {
                GaspriceStrategy.SLOW: response_data.get("safeLow"),
                GaspriceStrategy.REGULAR: response_data.get("average"),
                GaspriceStrategy.FAST: response_data.get("fast"),
                GaspriceStrategy.FASTEST: response_data.get("fastest"),
            }
        )

        for k, v in data.items():
            data[k] = int(v) // 10 if v else None

        return success, data
