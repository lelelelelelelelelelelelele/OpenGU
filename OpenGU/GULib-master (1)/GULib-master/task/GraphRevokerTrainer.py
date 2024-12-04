from task.BaseTrainer import BaseTrainer
import torch.nn.functional as F
import torch
class GraphRevokerTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    def posterior(self,return_features=False,mia=False):
        self.logger.debug("generating posteriors")
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self.model.eval()
        if mia:
            if self.args["base_model"] == "SIGN":
                posteriors = F.log_softmax(self.model(self.data.xs))
            else:
                posteriors = F.log_softmax(self.model(self.data.x,self.data.edge_index))
            for _, mask in self.data('test_mask'):
                posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

            return posteriors.detach()
        else:
            z, f = self._inference()

        if return_features:
            return z[self.data_full.test_mask], f[self.data_full.test_mask]
        return z[self.data_full.test_mask, :]
    
    @torch.no_grad()
    def _inference(self, no_test_edges=False):
        assert not self.data is None and not self.data_full is None

        self.model.eval()
        self.model = self.model.to(self.device)
        self.data_full = self.data.to(self.device) if no_test_edges else self.data_full.to(self.device)

        z, feat = self.model(self.data_full.x, self.data_full.edge_index, return_feature=True)

        return F.log_softmax(z,dim=1), feat


    def prepare_data(self, input_data):
        data_full = input_data.clone()
        data = input_data.clone()
        
        data.edge_index = data.edge_index_train
        
        data.edge_index_train = None
        data_full.edge_index_train = None

        # to_sparse = T.ToSparseTensor()
        # self.data = to_sparse(data)
        self.data.edge_index = input_data.edge_index_train
        self.data.train_edge_index = input_data.edge_index_train
        self.data.edge_index_train = None
        self.data_full = data_full
        # self.data_full = to_sparse(data_full)
        
        if self.args['is_use_train_batch']:
            self.gen_train_loader()
        if self.args['is_use_test_batch']:
            self.gen_test_loader()