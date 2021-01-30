from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict


class BaseGaspriceProvider(ABC):
    provider = NotImplemented

    @abstractmethod
    def _secret_from_env_var(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_gasprice(self) -> Tuple[bool, Dict[str, int]]:
        pass
