from typing import Dict, Optional, Tuple

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseAsyncAPIGaspriceProvider, BaseSyncAPIGaspriceProvider

__all__ = ["EtherscanProvider", "AsyncEtherscanProvider"]


class EtherscanProvider(BaseSyncAPIGaspriceProvider):
    """Provider for Etherscan Gas Tracker (https://etherscan.io/gasTracker)"""

    title: str = "etherscan"
    api_url: str = "https://api.etherscan.io/api/"
    secret_env_var_title: str = "ETHGASPRICE_ETHERSCAN_SECRET"

    def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = self.client.get(
                url=self.api_url, params={"module": "gastracker", "action": "gasoracle", "apikey": self.get_secret()}
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "1":
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
                GaspriceStrategy.REGULAR: response_data["result"].get("SafeGasPrice"),
                GaspriceStrategy.FAST: response_data["result"].get("ProposeGasPrice"),
                GaspriceStrategy.FASTEST: response_data["result"].get("FastGasPrice"),
            }
        )
        return data


class AsyncEtherscanProvider(BaseAsyncAPIGaspriceProvider, EtherscanProvider):
    async def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = await self.client.get(
                url=self.api_url, params={"module": "gastracker", "action": "gasoracle", "apikey": self.get_secret()}
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "1":
                return True, response_data

        except Exception:
            pass

        return False, {}
