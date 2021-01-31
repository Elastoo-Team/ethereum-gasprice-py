from enum import Enum

__all__ = ["EthereumUnit", "GaspriceStrategy"]


class EthereumUnit(str, Enum):
    WEI = "wei"
    GWEI = "gwei"
    ETH = "eth"


class GaspriceStrategy(str, Enum):
    SLOW = "slow"
    REGULAR = "regular"
    FAST = "fast"
    FASTEST = "fastest"

    def __repr__(self):
        return "<{}: {!r}>".format(self.__class__.__name__, self._value_)
