Parameters
===========

This section provides a comprehensive list of all command-line parameters available for the OpenGU main script. The parameters are organized into categories for easy reference and are presented in code blocks for clarity. Parameters with predefined choices have their options listed inline to enhance readability and avoid long lines.

General Parameters
------------------

.. code-block:: bash

    --cuda <cuda_device>               # Specify GPU device (e.g., 0)
    --num_threads <num_threads>       # Number of threads to utilize
    --root_path <root_path>           # Set the root path for the project

Data Parameters
---------------

.. code-block:: bash

    --dataset_name <dataset_name>      # Choose the graph dataset

**Choices:** cora, citeseer, pubmed, CS, Physics, flickr, Photo, Computers, DBLP, ogbl, ogbn-arxiv, ogbn-products, Squirrel, Chameleon, Actor, Minesweeper, Tolokers, Amazon-ratings, Roman-empire, Questions, MUTAG, COX2, AIDS, BZR, DD, PROTEINS, ENZYMES, DHFR, NCI1, PTC_MR, ogbg-molhiv, ogbg-molpcba, ogbg-ppa, MNISTSuperpixels, ShapeNet, IMDB-BINARY, IMDB-MULTI

.. code-block:: bash

    --is_transductive <True/False>    # Specify if the task is transductive or inductive
    --cal_mem <True/False>            # Run experiment to calculate memory usage
    --is_balanced <True/False>        # Split dataset with balanced classes
    --use_batch <True/False>          # Train model with minibatch
    --poison <True/False>             # Enable poisoned edges

Model Parameters
----------------

.. code-block:: bash

    --base_model <base_model>          # Select GNN backbone

**Choices:** SIGN, SGC, S2GC, SAGE, GAT, Cluster_GCN, GCN, GIN, GST, SAINT, Projector, Cheb, APPNP, GCN2, GATv2, TAG, LightGCN

.. code-block:: bash

    --unlearning_methods <method>      # Choose unlearning method

**Choices:** GraphEraser, GUIDE, GNNDelete, CEU, GIF, SGU, CGU, GST, Projector, MEGU, GraphRevoker, UTU, GUKD, D2DGN, IDEA, ScaleGUN

.. code-block:: bash

    --fl_algorithm <method>            # Federated Learning algorithm

**Choices:** isolate, fedavg, fedprox, scaffold, moon, feddc, fedproto, fedtgp, fedpub, fedstar, fedgta, fedtad, gcfl_plus, fedsage_plus, adafgl, feddep, fggp, fgssl, fedgl

.. code-block:: bash

    --train_ratio <float>              # Proportion of training data (default=0.8)
    --val_ratio <float>                # Proportion of validation data (default=0)
    --test_ratio <float>               # Proportion of test data (default=0.2)

Task Parameters
---------------

.. code-block:: bash

    --exp <experiment_type>            # Specify experiment type

**Choices:** partition, unlearning, node_edge_unlearning, attack_unlearning, sequence

.. code-block:: bash

    --unlearn_trainer <trainer>        # Specify unlearning trainer (default=BaseTrainer)

.. code-block:: bash

    --parameter_task <mode>            # Parameter task mode

**Choices:** normal, optuna

.. code-block:: bash

    --downstream_task <task>           # Specify downstream task

**Choices:** node, edge, graph

.. code-block:: bash

    --unlearn_task <task>              # Specify unlearning task

**Choices:** feature, node, edge

Training Parameters
-------------------

.. code-block:: bash

    --num_epochs <int>                 # Number of training epochs (default=100)
    --test_freq <int>                  # Frequency of testing during training (default=5)
    --batch_size <int>                 # Batch size for training (default=1024)
    --opt_lr <float>                   # Learning rate for optimizers (default=0.001)
    --opt_decay <float>                # Weight decay for optimizers (default=0.0001)
    --std <float>                      # Standard deviation for objective perturbation (default=1e-2)
    --alpha <float>                    # Alpha value in loss function (default=0.5)
    --optimizer <optimizer>            # Choice of optimizer (default=Adam)

**Choices:** LBFGS, Adam

.. code-block:: bash

    --lam <float>                      # L2 regularization (default=1e-2)
    --eps <float>                      # Epsilon for certified removal (default=1.0)
    --verbose <True/False>             # Enable verbosity (default=False)
    --compare_gnorm <True/False>       # Compute gradient norms (default=False)

Unlearning Parameters
----------------------

.. code-block:: bash

    --num_unlearned_nodes <int>            # Number of nodes to unlearn (default=270)
    --proportion_unlearned_nodes <float>   # Proportion of nodes to unlearn (default=0.1)
    --proportion_unlearned_edges <float>   # Proportion of edges to unlearn (default=0.1)
    --proportion_unlearned_edges_num <float># Proportion of edge numbers to unlearn (default=1e-4)
    --unlearn_ratio <float>                 # Ratio of unlearning (default=0.1)
    --unlearn_lr <float>                    # Learning rate for unlearning (default=0.01)

GUIDE Parameters
-----------------

.. code-block:: bash

    --GUIDE_methods <method>                # GUIDE method to use

**Choices:** Fast, SR

.. code-block:: bash

    --GUIDE_repair_methods <method>         # GUIDE repair method

**Choices:** Zero, Mirror, MixUp, NoneR

GraphEraser Parameters
------------------------

.. code-block:: bash

    --num_shards <int>                      # Number of shards for partitioning (default=10)
    --partition_method <method>             # Graph partitioning method

**Choices:** sage_km, random, lpa, metis, lpa_base, sage_km_base, gpa, graph_km

.. code-block:: bash

    --opt_num_epochs <int>                  # Number of optimization epochs (default=20)
    --ratio_deleted_edges <float>           # Ratio of edges to delete (default=0)
    --aggregator <aggregator>               # Aggregator method

**Choices:** mean, majority, optimal, contrastive, kernel_similarity

.. code-block:: bash

    --shard_size_delta <float>              # Shard size delta (default=0.005)
    --terminate_delta <int>                  # Termination delta (default=0)
    --is_prune <True/False>                 # Enable pruning (default=False)
    --is_partition <True/False>             # Enable partitioning (default=True)
    --is_constrained <True/False>           # Enable constraints (default=True)
    --is_train_target_model <True/False>     # Train the target model (default=True)
    --is_gen_embedding <True/False>          # Generate embeddings (default=True)
    --num_runs <int>                         # Number of runs (default=1)
    --num_opt_samples <int>                  # Number of optimization samples (default=1000)

GNNDelete Parameters
---------------------

.. code-block:: bash

    --checkpoint_dir <path>                  # Directory for saving checkpoints (default=./data/GNNDelete/checkpoint_node)
    --random_seed <int>                      # Random seed for reproducibility (default=42)
    --hidden_dim <int>                       # Hidden dimension size (default=64)
    --in_dim <int>                           # Input dimension size (default=128)
    --out_dim <int>                          # Output dimension size (default=64)
    --unlearning_model <model>                # Unlearning method model name (default=gnndelete_nodeemb)
    --df <str>                               # Df set to use (default=out)
    --df_idx <str>                           # Indices of data to be deleted (default=none)
    --df_size <float>                        # Df size (default=0.5)
    --neg_sample_random <type>               # Type of negative samples for randomness (default=non_connected)
    --loss_fct <loss_function>               # Loss function to use

**Choices:** mse, kld, cosine

.. code-block:: bash

    --loss_type <type>                       # Type of loss

**Choices:** both_all, both_layerwise, only2_layerwise, only2_all, only1

CEU Parameters
---------------

.. code-block:: bash

    --train_batch <int>                     # Training batch size (default=10)
    --test_batch <int>                      # Testing batch size (default=5)
    -l2 <float>                             # L2 regularization factor (default=1E-5)
    --early_stop <True/False>               # Enable early stopping (default=True)
    -patience <int>                         # Patience for early stopping (default=5)
    --feature <True/False>                  # Enable embedding feature (default=False)
    --feature_update <True/False>           # Enable embedding feature update (default=True)
    --emb_dim <int>                         # Embedding dimension size (default=32)
    -max-degree <True/False>                # Enable maximum degree (default=False)
    -damping <float>                        # Damping factor (default=0.0)
    -hidden <ints>                          # Hidden layer sizes (default=[])
    -approx <str>                            # Approximation method

**Choices:** cg

.. code-block:: bash

    -depth <int>                            # Depth parameter (default=300)

GIF Parameters
---------------

.. code-block:: bash

    --GIF_method <method>                   # GIF method to use

**Choices:** GIF, Retrain, IF

.. code-block:: bash

    --GIF_exp <experiment_type>             # GIF experiment type (default=unlearning)
    --is_split <True/False>                 # Enable splitting of train/test data (default=True)
    --iteration <int>                       # Number of iterations (default=100)
    --scale <int>                           # Scaling factor (default=1000000)
    --damp <float>                          # Damping factor (default=0.0)

SGU Parameters
---------------

.. code-block:: bash

    --GNN_layer <int>                       # Number of GNN layers (default=3)
    --unlearning_epochs <int>                # Number of unlearning epochs (default=50)
    --Budget <float>                        # Budget parameter (default=0.01)
    --para1 <float>                         # Parameter 1 (default=2.5)
    --para2 <float>                         # Parameter 2 (default=0.01)
    --para3 <float>                         # Parameter 3 (default=200)
    --para4 <float>                         # Parameter 4 (default=0.1)
    --para5 <float>                         # Parameter 5 (default=10)

GST Parameters
---------------

.. code-block:: bash

    --folds <int>                           # Number of folds for cross-validation (default=10)
    --display_step <int>                    # Display frequency (default=10)
    --rm_disp_step <int>                    # Removal display step (default=1)
    --J <int>                                # Parameter J (default=5)
    --Q <int>                                # Parameter Q (default=4)
    --L <int>                                # Parameter L (default=3)
    --remove_guo <True/False>                # Remove Guo method (default=False)
    --retrain <True/False>                   # Retrain GST from scratch (default=False)

**Note:**

- If `--retrain` is `True`, then `--remove_guo` should be `False`.

.. code-block:: bash

    --GST_delta <float>                      # Delta coefficient for certified removal (default=1e-4)

Projector Parameters
---------------------

.. code-block:: bash

    --hop_neighbors <int>                   # Number of hop neighbors (default=20)
    --dropout_times <int>                   # Number of dropout times (default=2)
    --use_cross_entropy <True/False>         # Enable cross-entropy loss (default=False)
    --use_adapt_gcs <True/False>             # Enable adaptive GCS (default=False)
    --x_iters <int>                         # Number of X iterations (default=3)
    --y_iters <int>                         # Number of Y iterations (default=3)
    --require_linear_span <True/False>       # Require linear span (default=True)
    --regen_model <True/False>               # Regenerate the model (default=True)
    --parallel_unlearning <int>              # Number of parallel unlearning processes (default=1)

CGU Parameters
---------------

.. code-block:: bash

    --result_dir <path>                      # Directory for saving results (default=./result/CGU)
    --dataset <str>                          # Dataset to use (default=null)
    --train_mode <mode>                      # Training mode

**Choices:** ovr, binary

.. code-block:: bash

    --train_sep <True/False>                  # Train binary classifiers separately (default=False)
    --XdegNorm <True/False>                   # Apply degree normalization trick (default=False)
    --add_self_loops <True/False>             # Add self-loops in propagation matrix (default=True)
    --wd <float>                              # Weight decay factor for Adam (default=5e-4)
    --featNorm <True/False>                   # Row normalize features to norm 1 (default=False)
    --GPR <True/False>                        # Use GPR model (default=False)
    --balance_train <True/False>              # Subsample training set to balance classes (default=False)
    --Y_binary <str>                          # Y_binary class or Y_binary_1 vs Y_binary_2 (default=0)
    --noise_mode <mode>                       # Type of noise

**Choices:** data, worst

.. code-block:: bash

    --removal_mode <mode>                     # Removal mode

**Choices:** feature, edge, node

.. code-block:: bash

    --delta <float>                           # Delta coefficient for certified removal (default=1e-4)
    --disp <int>                              # Display frequency (default=5)
    --fix_random_seed <True/False>            # Use fixed random seed for removal queue (default=False)
    --compare_retrain <True/False>            # Compare accuracy with retraining each round (default=False)
    --compare_guo <True/False>                # Compare performance with Guo et al. (default=False)

MEGU Parameters
----------------

.. code-block:: bash

    --kappa <float>                           # Kappa parameter (default=0.01)
    --alpha1 <float>                          # Alpha1 parameter (default=0.8)
    --alpha2 <float>                          # Alpha2 parameter (default=0.5)

GraphRevoker Parameters
------------------------

.. code-block:: bash

    --is_use_train_batch <True/False>         # Use training batches (default=False)
    --is_use_test_batch <True/False>          # Use testing batches (default=False)

IDEA Parameters
----------------

.. code-block:: bash

    --unlearn_feature_partial_ratio <float>   # Partial ratio for unlearning features (default=0.5)
    --gaussian_mean <float>                    # Mean for Gaussian noise (default=0.0)
    --gaussian_std <float>                     # Standard deviation for Gaussian noise (default=0.0)
    --l <float>                                # Lipschitz constant of the loss (default=0.25)
    --lambda <float>                           # Lambda for loss function (default=1.0)
    --c <float>                                # Numerical bound of training loss per sample (default=0.5)
    --M <float>                                # M for loss function (default=0.25)
    --c1 <float>                               # Bounded derivative of loss (default=1.0)
    --lambda_edge_unlearn <float>              # Regularization weight for edge unlearning (default=1.0)
    --gamma_2 <float>                          # Lipschitz constant of first-order derivative for edge unlearning (default=1.0)
    --file_name <str>                           # File name for results (default=unlearning_results)
    --write <True/False>                        # Enable writing results (default=True)

UTULink Parameters
-------------------

.. code-block:: bash

    --eval_on_cpu <True/False>                 # Evaluate on CPU (default=False)

ScaleGUN Parameters
--------------------

.. code-block:: bash

    --path <path>                              # Path for ScaleGUN data (default=./data/ScaleGUN)
    --del_path_suffix <suffix>                 # Suffix for deletion path (default=unlearning_data/)
    --analysis_path <path>                     # Path for analysis (default=analysis)
    --trials <int>                             # Number of trials (default=3)
    --axis_num <int>                           # Axis number

**Choices:** 1, 0

.. code-block:: bash

    --prop_algo <algorithm>                    # Propagation algorithm

**Choices:** power, push, MC

.. code-block:: bash

    --prop_step <int>                          # Number of propagation steps (default=3)
    --r <float>                                # Parameter r (default=0.5)
    --decay <float>                            # Decay factor (default=0.1)
    --RW <int>                                 # Number of random walk times (default=10000)
    --rmax <float>                             # Maximum r value (default=0.0)
    --ppr <True/False>                         # Use PPR model (default=False)
    --weight_mode <mode>                       # Weight mode

**Choices:** decay, avg, test, hetero

.. code-block:: bash

    --optuna <True/False>                      # Use Optuna for hyperparameter optimization (default=False)
    --del_postfix <str>                         # Postfix for deletion (default='')
    --del_only <True/False>                     # Enable delete-only mode (default=False)
    --lr <float>                                # Learning rate (default=1)
    --num_batch_removes <int>                    # Number of batch removals (default=5)
    --no_retrain <True/False>                    # Disable retraining (default=False)
    --edge_idx_start <int>                       # Starting index for edge removal (default=0)
    --num_removes <int>                           # Number of removed edges/nodes per batch (default=1)
