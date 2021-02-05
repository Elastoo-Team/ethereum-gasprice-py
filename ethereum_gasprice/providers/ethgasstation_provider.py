from typing import Dict, Optional, Tuple

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.base import BaseAsyncAPIGaspriceProvider, BaseSyncAPIGaspriceProvider

__all__ = ["EthGasStationProvider", "AsyncEthGasStationProvider"]


class EthGasStationProvider(BaseSyncAPIGaspriceProvider):
    """Provider for Eth Gas Station (https://ethgasstation.info/)"""

    title: str = "ethgasstation"
    api_url: str = "https://ethgasstation.info/api/ethgasAPI.json"
    secret_env_var_title: str = "ETHGASPRICE_ETHGASSTATION_SECRET"

    def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = self.client.get(url=self.api_url, params={"api-key": self.get_secret()})
            response_data = response.json()

            if response.status_code == 200:
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
                GaspriceStrategy.SLOW: response_data.get("safeLow"),
                GaspriceStrategy.REGULAR: response_data.get("average"),
                GaspriceStrategy.FAST: response_data.get("fast"),
                GaspriceStrategy.FASTEST: response_data.get("fastest"),
            }
        )

        for k, v in data.items():
            data[k] = int(v) // 10 if v else None

        return data


class AsyncEthGasStationProvider(BaseAsyncAPIGaspriceProvider, EthGasStationProvider):
    async def request(self) -> Tuple[bool, dict]:
        """Make request to API."""
        try:
            response = await self.client.get(url=self.api_url, params={"api-key": self.get_secret()})
            response_data = response.json()

            if response.status_code == 200:
                return True, response_data

        except Exception:
            pass

        return False, {}
