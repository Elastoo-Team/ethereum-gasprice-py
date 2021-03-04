from typing import Dict, Optional, Tuple

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseAsyncAPIGaspriceProvider, BaseSyncAPIGaspriceProvider

__all__ = ["PoaProvider", "AsyncPoaProvider"]


class PoaProvider(BaseSyncAPIGaspriceProvider):
    """Provider for Etherscan Gas Tracker (https://etherscan.io/gasTracker)"""

    title: str = "etherchain"
    api_url: str = "https://gasprice.poa.network/"

    def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = self.client.get(url=self.api_url)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("health") is True:
                return True, response_data

        except Exception:
            pass

        return False, {}

    def _proceed_response_data(self, response_data: dict) -> Dict[GaspriceStrategy, Optional[int]]:
        """Unify data from response."""
        data = self._data_template.copy()

        if not response_data:
            return data

        data.update(
            {
                GaspriceStrategy.SLOW: response_data.get("slow"),
                GaspriceStrategy.REGULAR: response_data.get("standard"),
                GaspriceStrategy.FAST: response_data.get("fast"),
                GaspriceStrategy.FASTEST: response_data.get("instant"),
            }
        )
        return data


class AsyncPoaProvider(BaseAsyncAPIGaspriceProvider, PoaProvider):
    async def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = await self.client.get(url=self.api_url)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("health") is True:
                return True, response_data

        except Exception:
            pass

        return False, {}
