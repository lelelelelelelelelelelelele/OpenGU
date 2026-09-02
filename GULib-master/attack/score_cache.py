"""Score consumers use the same immutable Cache V2 store as Selection/Result."""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from attack.cache_identity import model_fingerprint, producer_version, resolve_store_root
from experiments.selection_inputs import graph_fingerprint
from cache_v2 import ArtifactType
from cache_v2.formal_artifacts import ScorePayload, build_score_recipe
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact

@dataclass
class ScoreResult:
    candidates: np.ndarray
    scores: np.ndarray
    key: str
    source: str

class ScoreCache:
    def __init__(self, namespace, cache_dir="./results/cache_v2"):
        self.namespace = namespace
        self.root = resolve_store_root(cache_dir)
        strategy = "tracin" if namespace == "if" else "im"
        self.producer = producer_version("score-" + namespace,
            ["attack/score_cache.py", "attack/cache_identity.py",
             "attack/attack_strategies/" + strategy + "_strategy.py"])

    def request(self, identity):
        parameters = {key: value for key, value in identity.items()
                      if key not in {"graph_fingerprint", "candidate_set_hash", "candidate_nodes", "num_nodes"}}
        recipe = build_score_recipe(graph_fingerprint=identity["graph_fingerprint"],
            candidate_set_hash=identity["candidate_set_hash"], num_nodes=identity["num_nodes"],
            node_id_space="opengu-node-id", selector_identity={"namespace": self.namespace},
            score_algorithm={"name": self.namespace}, parameters=parameters,
            producer_version=self.producer)
        return FormalArtifactRequest(ArtifactType.SCORE, recipe, self.producer)

    def build_key(self, identity):
        return self.request(identity).recipe.recipe_hash

    def get(self, identity):
        request = self.request(identity)
        result = resolve_formal_artifact(self.root, request)
        key = request.recipe.recipe_hash
        if result is None:
            return None, key
        return ScoreResult(result.payload.ordered_node_ids.copy(),
            result.payload.scores.astype(np.float32), key,
            str(self.root / result.semantic_path)), key

    def save(self, candidates, scores, identity):
        request = self.request(identity)
        candidates = np.asarray(candidates, dtype=np.int64)
        if not set(candidates.tolist()).issubset(identity["candidate_nodes"]):
            raise ValueError("Score nodes are outside the requested candidate set")
        payload = ScorePayload.build(ordered_node_ids=candidates, scores=np.asarray(scores),
            graph_fingerprint=identity["graph_fingerprint"],
            candidate_set_hash=identity["candidate_set_hash"], node_id_space="opengu-node-id", score_kind="scores")
        result = store_formal_artifact(self.root, request, payload)
        return str(self.root / result.semantic_path)
