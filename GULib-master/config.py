import os

from parameter_parser import parameter_parser
args = parameter_parser()
split_ratio = str(args['train_ratio']) + '_' + str(args['val_ratio']) + '_' + str(args['test_ratio'])
root_path = os.path.normpath(str(args.get("root_path") or "."))
runtime_root = os.path.normpath(str(args.get("runtime_root") or root_path))
###for Graph Eraser and GraphRevoker###
RAW_DATA_PATH = root_path + '/data/raw/'
# PROCESSED_DATA_PATH = './data/GraphEraser/processed/'
PROCESSED_DATA_PATH = runtime_root + '/data/' + args["unlearning_methods"] + "/processed/"
if args["unlearning_methods"] == "GIF":
    PROCESSED_DATA_PATH2 = runtime_root + '/data/processed/GIF/'
else:
    if args["is_transductive"]:
        PROCESSED_DATA_PATH2 = runtime_root + '/data/processed/transductive/'
    else:
        PROCESSED_DATA_PATH2 = runtime_root + '/data/processed/inductive/'
# MODEL_PATH = './data/GraphEraser/'
MODEL_PATH = runtime_root + '/data/' + args["unlearning_methods"] + "/"
# ANALYSIS_PATH = './data/GraphEraser/analysis_data/'
ANALYSIS_PATH = runtime_root + '/data/'+ args["unlearning_methods"] +'/analysis_data/'

embedding_name = '_'.join(('embedding', args["partition_method"],str(args['ratio_deleted_edges'])))

community_name = '_'.join(('community', args['partition_method'], str( args['num_shards']),str(args['ratio_deleted_edges'])))

shard_name = '_'.join(('shard_data', args['partition_method'], str(args['num_shards']),str(args['shard_size_delta']), str(args['ratio_deleted_edges'])))

target_model_name = '_'.join((args['base_model'], args['partition_method'], str( args['num_shards']),str(args['shard_size_delta']), str(args['ratio_deleted_edges'])))

optimal_weight_name = '_'.join((args['base_model'],args['partition_method'], str(args['num_shards']),str(args['shard_size_delta']), str(args['ratio_deleted_edges'])))

processed_data_prefix = PROCESSED_DATA_PATH + args['dataset_name'] + "/"
shard_file = processed_data_prefix + shard_name
train_data_file = processed_data_prefix + "train_data"
train_graph_file = processed_data_prefix + "train_graph"
if args['is_balanced']:
    train_test_split_file = PROCESSED_DATA_PATH2 + args['dataset_name'] + split_ratio + "_balanced.pkl"
else:
    train_test_split_file = PROCESSED_DATA_PATH2 + args['dataset_name'] + split_ratio + ".pkl"
load_community_data = processed_data_prefix +community_name
embedding_file = processed_data_prefix + embedding_name
community_file = processed_data_prefix + community_name
community_path = PROCESSED_DATA_PATH + args['dataset_name'] + "/" + community_name
# unlearned_file = processed_data_prefix+ '_'.join(('unlearned', str(args['num_unlearned_nodes'])))
unlearned_file = processed_data_prefix+ '_'.join(('unlearned', str(args['unlearn_ratio'])))
model_path =MODEL_PATH + args['dataset_name'] + "/" + target_model_name
GIF_logger_name = "_".join((args['dataset_name'], str(args['test_ratio']), args['base_model'], args['unlearn_task'],str(args['proportion_unlearned_nodes'])))
target_model_file = MODEL_PATH + args['dataset_name'] + '/' + target_model_name


#for SGU
# root_path = "./GULib"
# unlearning_path = root_path + "/data/unlearning_nodes_" + str(args["proportion_unlearned_nodes"]) + "_" + args["dataset_name"] + ".txt"
if args["is_transductive"]:
    if args["is_balanced"]:
        unlearning_path = runtime_root + "/data/unlearning_task/transductive/balanced/unlearning_nodes_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
        unlearning_edge_path = runtime_root + "/data/unlearning_task/transductive/balanced/unlearning_edges_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
    else:       
        unlearning_path = runtime_root + "/data/unlearning_task/transductive/imbalanced/unlearning_nodes_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
        unlearning_edge_path = runtime_root + "/data/unlearning_task/transductive/imbalanced/unlearning_edges_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
else:
    if args["is_balanced"]:
        unlearning_path = runtime_root + "/data/unlearning_task/inductive/balanced/unlearning_nodes_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
        unlearning_edge_path = runtime_root + "/data/unlearning_task/inductive/balanced/unlearning_edges_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
    else:       
        unlearning_path = runtime_root + "/data/unlearning_task/inductive/imbalanced/unlearning_nodes_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]
        unlearning_edge_path = runtime_root + "/data/unlearning_task/inductive/imbalanced/unlearning_edges_" + str(args["unlearn_ratio"]) + "_" + args["dataset_name"]

if args["poison"]:
    unlearning_edge_path = unlearning_edge_path + "_poison"

noise_path = root_path + "/data/noise/" + args["dataset_name"] + "/"+ args["process"] +"_"+ str(args["noise_ratio"]) +".txt"
sparsity_path = root_path + "/data/sparsity/" + args["dataset_name"] + "/"+ args["process"] +"_"+ str(args["sparsity_ratio"]) +".txt"

BLUE_COLOR = "\033[34m"
RESET_COLOR = "\033[0m"
