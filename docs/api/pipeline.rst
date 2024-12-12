Pipeline
============

IF_based_pipeline
-----------------------
.. automodule:: pipeline.IF_based_pipeline
   :members:
   :special-members: __init__
   :exclude-members: unlearning_request, determine_target_model, train_original_model, 
                     approxi, mia_attack, get_if_grad, mia_attack_edge, unlearn
   :show-inheritance:

Learning_based_pipeline
-----------------------
.. automodule:: pipeline.Learning_based_pipeline
   :members:
   :special-members: __init__
   :exclude-members: determine_target_model, train_original_model, unlearning_request, 
                     unlearn, mia_attack, mia_attack_edge
   :show-inheritance:

Shard_based_pipeline
-----------------------
.. automodule:: pipeline.Shard_based_pipeline
   :members:
   :special-members: __init__
   :exclude-members: gen_train_graph, graph_partition, generate_shard_data, load_data, 
                     determine_target_model, train_shard_model, aggregate_shard_model, 
                     generate_requests, unlearn, attack_unlearning
   :show-inheritance: