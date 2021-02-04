from typing import Dict, Optional, Tuple

import requests

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseGaspriceProvider

__all__ = ["EtherchainProvider"]


class EtherchainProvider(BaseGaspriceProvider):
    """Provider for Etherscan Gas Tracker (https://etherscan.io/gasTracker)"""

    provider_title: str = "etherchain"
    api_url: str = "https://www.etherchain.org/api/gasPriceOracle"

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        try:
            response = requests.get(url=self.api_url)
        except Exception:
            return success, data

        response_data = response.json()

        if response.status_code != 200:
            return success, data

        success = True
        data.update(
            {
                GaspriceStrategy.SLOW: response_data.get("safeLow"),
                GaspriceStrategy.REGULAR: response_data.get("standard"),
                GaspriceStrategy.FAST: response_data.get("fast"),
                GaspriceStrategy.FASTEST: response_data.get("fastest"),
            }
        )

        return success, data
