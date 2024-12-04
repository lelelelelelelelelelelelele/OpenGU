import logging

import config
from model.base_gnn.graphsage import SAGENet
from utils.dataset_utils import *
from utils.dataset_utils import _extract_embedding_method
from model.model_zoo import  model_zoo

class NodeEmbedding:
    def __init__(self, args,logger, graph, data):
        super(NodeEmbedding, self)

        self.logger = logging.getLogger(__name__)
        self.args = args
        self.graph = graph
        self.data = data
        self.logger  = logger

    def sage_encoder(self):
        embedding_name = '_'.join(('embedding', _extract_embedding_method(self.args['partition_method']),
                                   str(self.args['ratio_deleted_edges'])))
        embedding_path = config.PROCESSED_DATA_PATH + self.data.name + "/" + embedding_name
        if self.args['is_gen_embedding']:
            self.logger.info("generating node embeddings with GraphSage...")

            node_to_embedding = {}
            # run sage

            #self.target_model = SAGENet(self.data.num_features, len(self.data.y.unique()), self.data)
            self.target_model = model_zoo(self.args,self.data)

            # self.target_model.train_model(50)

            # load a pretrained GNN models for generating node embeddings
            # target_model_name = '_'.join((self.args['base_model'], 'random_1',
            #                               str(self.args['shard_size_delta']),
            #                               str(self.args['ratio_deleted_edges']), '0_0_1'))
            target_model_file = config.MODEL_PATH + self.args['dataset_name'] + '/' + self.args['base_model']
            self.target_model.model.load_model(target_model_file)

            logits = self.target_model.generate_embeddings().detach().cpu().numpy()
            for node in self.graph.nodes:
                node_to_embedding[node] = logits[node]

            save_embeddings(node_to_embedding,embedding_path)
        else:
            node_to_embedding = load_embeddings(embedding_path)

        return node_to_embedding
