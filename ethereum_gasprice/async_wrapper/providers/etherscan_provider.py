from typing import Dict, Optional, Tuple

from aiohttp import ClientSession

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers.etherscan_provider import EtherscanProvider

__all__ = ["AsyncEtherscanProvider"]


class AsyncEtherscanProvider(EtherscanProvider):
    async def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success = False
        data = self._data_template.copy()

        try:
            async with ClientSession() as session:
                async with session.get(
                    url=self.api_url, params={"module": "gastracker", "action": "gasoracle", "apikey": self.api_key}
                ) as response:
                    response_data = await response.json()

        except Exception:
            return success, data

        if response.status != 200 or not response_data.get("status") == "1":
            return success, data

        success = True
        data.update(
            {
                GaspriceStrategy.REGULAR: response_data["result"].get("SafeGasPrice"),
                GaspriceStrategy.FAST: response_data["result"].get("ProposeGasPrice"),
                GaspriceStrategy.FASTEST: response_data["result"].get("FastGasPrice"),
            }
        )

        return success, data
