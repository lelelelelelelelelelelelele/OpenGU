"""Aggregate attack metrics stored as a Selection-dependent V2 Evaluation."""
from pathlib import Path
from attack.attack_result import AttackResult
from attack.cache_identity import resolve_store_root
from cache_v2 import ArtifactRecipe, ArtifactType
from cache_v2.attack_evaluation import ATTACK_EVALUATION_CONTRACT, AttackEvaluationPayload
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact

class ResultCache:
    def __init__(self, cache_dir="./results/cache_v2"):
        self.root = resolve_store_root(cache_dir)

    @staticmethod
    def request(selection, graph_fingerprint, selected_nodes_hash, target, producer):
        recipe = ArtifactRecipe({"artifact_contract": ATTACK_EVALUATION_CONTRACT,
            "selection_artifact_id": selection.artifact_id,
            "selected_nodes_hash": selected_nodes_hash,
            "graph_fingerprint": graph_fingerprint,
            "target": target, "producer_version": producer.to_dict()})
        return FormalArtifactRequest(ArtifactType.EVALUATION, recipe, producer)

    def get_with_provenance(self, request):
        resolved = resolve_formal_artifact(self.root, request)
        if resolved is None:
            return None, {}
        return AttackResult.from_dict(resolved.payload.metrics), {
            "cache_key": resolved.artifact_id,
            "source_file": str(self.root / resolved.semantic_path),
            "recipe_hash": request.recipe.recipe_hash,
            "content_hash": resolved.content_hash,
            "lookup_policy": "cache_v2_exact_recipe"}

    def get(self, request):
        return self.get_with_provenance(request)[0]

    def save(self, result, request):
        fields = request.recipe.fields
        payload = AttackEvaluationPayload(fields["selection_artifact_id"],
            fields["graph_fingerprint"], fields["selected_nodes_hash"], result.to_dict())
        return store_formal_artifact(self.root, request, payload)
