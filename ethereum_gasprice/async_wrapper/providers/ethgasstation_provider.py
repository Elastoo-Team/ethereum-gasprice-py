from typing import Dict, Optional, Tuple

from aiohttp import ClientSession

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.ethgasstation_provider import EthGasStationProvider

__all__ = ["AsyncEthGasStationProvider"]


class AsyncEthGasStationProvider(EthGasStationProvider):
    async def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        if not self.api_key:
            return success, data

        try:
            async with ClientSession() as session:
                async with session.get(url=self.api_url, params={"api-key": self.api_key}) as response:
                    response_data = await response.json()

        except Exception:
            return success, data

        if response.status != 200:
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
