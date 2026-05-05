from .base_strategy import BaseStrategy
from .random_strategy import RandomStrategy
from .degree_strategy import DegreeStrategy
from .pagerank_strategy import PageRankStrategy
from .tracin_strategy import TracInStrategy
from .im_strategy import IMStrategy
from .hybrid_strategy import HybridStrategy

# Backward-compat aliases — IMV4Strategy / HybridV4Strategy were merged
# into the canonical IMStrategy / HybridStrategy on 2026-05-05. Old code
# importing the V4 names still gets the (now batch-CELF) IMStrategy.
IMV4Strategy = IMStrategy
HybridV4Strategy = HybridStrategy
