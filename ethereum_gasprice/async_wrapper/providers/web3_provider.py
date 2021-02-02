from typing import Dict, Optional, Tuple

from ethereum_gasprice.consts import GaspriceStrategy
from ethereum_gasprice.providers import Web3Provider

__all__ = ["AsyncWeb3Provider"]


class AsyncWeb3Provider(Web3Provider):
    async def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        return super().get_gasprice()
