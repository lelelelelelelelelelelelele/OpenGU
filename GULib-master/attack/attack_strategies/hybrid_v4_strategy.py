from .hybrid_strategy import HybridStrategy
from .im_v4_strategy import IMV4Strategy


class HybridV4Strategy(HybridStrategy):
    """
    Hybrid strategy variant bound to IM V4 backend.

    Keeps the same fusion mechanism as HybridStrategy while swapping IM backend.
    """

    def __init__(self, args: dict):
        super().__init__(args)
        self.im = IMV4Strategy(args)
