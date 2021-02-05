from abc import ABC, abstractmethod
from os import getenv
from typing import Dict, Optional, Tuple

from httpx import AsyncClient, Client

from ethereum_gasprice.consts import GaspriceStrategy

__all__ = [
    "BaseGaspriceProvider",
    "BaseAPIGaspriceProvider",
    "BaseSyncAPIGaspriceProvider",
    "BaseAsyncAPIGaspriceProvider",
]


class BaseGaspriceProvider(ABC):
    title: str = NotImplemented
    secret_env_var_title: str = NotImplemented

    def __init__(self, secret: Optional[str] = None, *args, **kwargs):
        self.secret: Optional[str] = secret

    def get_secret(self) -> Optional[str]:
        return self.secret or getenv(self.secret_env_var_title)

    @property
    def _data_template(self) -> Dict[GaspriceStrategy, Optional[int]]:
        return {
            GaspriceStrategy.SLOW: None,
            GaspriceStrategy.REGULAR: None,
            GaspriceStrategy.FAST: None,
            GaspriceStrategy.FASTEST: None,
        }

    @abstractmethod
    def get_gasprice(self) -> Tuple[bool, Dict[str, int]]:
        pass


class BaseAPIGaspriceProvider(BaseGaspriceProvider, ABC):
    api_url: str = NotImplemented

    @abstractmethod
    def request(self, *args, **kwargs):
        pass

    @abstractmethod
    def _proceed_response_data(self, *args, **kwargs):
        pass


class BaseSyncAPIGaspriceProvider(BaseAPIGaspriceProvider, ABC):
    def __init__(self, *, secret: Optional[str] = None, client: Optional[Client] = None, **kwargs):
        super().__init__(secret=secret, **kwargs)
        self.client: Client = client

    def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success, response_data = self.request()
        return success, self._proceed_response_data(response_data)


class BaseAsyncAPIGaspriceProvider(BaseAPIGaspriceProvider, ABC):
    def __init__(self, *, secret: Optional[str] = None, client: Optional[AsyncClient] = None, **kwargs):
        super().__init__(secret=secret, **kwargs)
        self.client: AsyncClient = client

    async def get_gasprice(self) -> Tuple[bool, Dict[GaspriceStrategy, Optional[int]]]:
        """Get gasprice from provider and prepare data."""
        success, response_data = await self.request()
        return success, self._proceed_response_data(response_data)
