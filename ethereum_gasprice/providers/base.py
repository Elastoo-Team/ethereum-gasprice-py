from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

from ethereum_gasprice.consts import GaspriceStrategy


class BaseGaspriceProvider(ABC):
    provider_title = NotImplemented

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
