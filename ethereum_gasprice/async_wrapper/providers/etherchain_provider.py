from typing import Dict, Optional, Tuple

from aiohttp import ClientSession

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers import EtherchainProvider

__all__ = ["AsyncEtherchainProvider"]


class AsyncEtherchainProvider(EtherchainProvider):
    async def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        try:
            async with ClientSession() as session:
                async with session.get(url=self.api_url) as response:
                    response_data = await response.json()

        except Exception:
            return success, data

        if response.status != 200:
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
