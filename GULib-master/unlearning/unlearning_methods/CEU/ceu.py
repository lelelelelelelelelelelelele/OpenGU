import copy
import os
import random
import torch
import pandas as pd
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader
from collections import defaultdict

from attack.Attack_methods.CEU_MIA import _mia_attack
from task.node_classification import NodeClassifier
from task import get_trainer
from tqdm import tqdm
from scipy.sparse import csr_matrix
from deeprobust.graph.utils import preprocess
from deeprobust.graph.defense import GCN
from deeprobust.graph.global_attack import PGDAttack, MinMax, Metattack
from unlearning.unlearning_methods.CEU.unlearn import unlearn
from utils.utils import JSD, remove_undirected_edges
from pipeline.IF_based_pipeline import IF_based_pipeline

class ceu(IF_based_pipeline):
    def __init__(self,args,logger,model_zoo):
        self.args = args
        self.logger = logger
        self.data = model_zoo.data
        self.model_zoo = model_zoo
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # self.NodeClassifier = NodeClassifier(args,self.data,self.model_zoo,self.logger)
        self.args["unlearn_trainer"] = 'CEUTrainer'
        self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)
        self.fidelity()
        self.efficacy()
        

    def fidelity(self):
        self.delete_edges = [100,200,400,800,1000]
        test_loader = DataLoader(self.data['test_set'], shuffle=False, batch_size=self.args["test_batch"])
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        result = defaultdict(list)

        for _ in tqdm(range(1), desc=f'{self.args["dataset_name"]}-{self.args["base_model"]}'):
            original_model = self.target_model.CEU_train(self.data,eval=False, verbose=False,return_epoch=False)
            original_res, _ = self.target_model.CEU_test(original_model, test_loader, edge_index)

            for num_edges in self.delete_edges:
                _, _, adv_res, _ = self.adv_retrain_unlearn(self.data, num_edges)

                # Benign
                random_edges = []
                while len(random_edges) < num_edges * 2:
                    v1 = random.randint(0, self.data['num_nodes'] - 1)
                    v2 = random.randint(0, self.data['num_nodes'] - 1)
                    if (v1, v2) in self.data['edges'] or (v2, v1) in self.data['edges']:
                        continue
                    random_edges.append((v1, v2))
                    random_edges.append((v2, v1))

                _data = copy.deepcopy(self.data)
                _data['edges'] += random_edges
                benign_orig = self.target_model.CEU_train(_data,eval=False, verbose=False)
                benign_unlearn, _ = unlearn(self.args,_data, benign_orig, random_edges, device=self.device)

                benign_res, _ = self.target_model.CEU_test(benign_unlearn, test_loader, edge_index)
                result['# edges'].append(num_edges)
                result['setting'].append('Retrain')
                result['accuracy'].append(original_res['accuracy'])

                result['# edges'].append(num_edges)
                result['setting'].append('Benign')
                result['accuracy'].append(benign_res['accuracy'])

                result['# edges'].append(num_edges)
                result['setting'].append('Advesarial')
                result['accuracy'].append(adv_res['accuracy'])
        
        df = pd.DataFrame(data=result)
        print(df.groupby(['# edges', 'setting']).mean())
        if not os.path.exists('./result/CEU'):
            os.mkdir('./result/CEU')
        df.to_csv(f'./result/CEU/fidelity_{self.args["dataset_name"]}_{self.args["base_model"]}.csv')

    def efficacy(self):
        self.delete_edges = [100, 200, 400, 800, 1000]
        test_loader = DataLoader(self.data['test_set'], shuffle=False, batch_size=self.args["test_batch"])
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        nodes = torch.tensor(self.data['nodes'], device=self.device)

        jsd_result = defaultdict(list)
        mia_result = defaultdict(list)


        for _ in tqdm(range(1), desc=f'{self.args["dataset_name"]}-{self.args["base_model"]}'):
            original_model = self.target_model.CEU_train(self.data,eval=False, verbose=False,return_epoch=False)
            original_res, _ = self.target_model.CEU_test(original_model, test_loader, edge_index)

            for num_edges in self.delete_edges:
                def _efficacy(retrain_model, unlearn_model, edge_index_prime):
                    retrain_model.eval()
                    with torch.no_grad():
                        retrain_post = retrain_model(nodes, edge_index_prime)
                    unlearn_model.eval()
                    with torch.no_grad():
                        unlearn_post = unlearn_model(nodes, edge_index_prime)

                    retrain_post = F.softmax(retrain_post, dim=1).cpu().numpy().astype(np.float64)
                    unlearn_post = F.softmax(unlearn_post, dim=1).cpu().numpy().astype(np.float64)

                    _jsd = JSD(retrain_post, unlearn_post)
                    if np.sum(_jsd < 0) > 0:
                        _jsd[_jsd < 0] = 0
                    return np.mean(_jsd)

                adv_model, adv_unlearn_model, A = self.adv_unlearn(self.data, num_edges)

                adv_o_pl, adv_r_pl, adv_u_pl = _mia_attack(self.data, adv_model, original_model,
                                                           adv_unlearn_model, A, self.device)
                edge_index_prime = torch.tensor(remove_undirected_edges(self.data['edges'], A), device=self.device).t()

                adv_jsd = _efficacy(original_model, adv_unlearn_model, edge_index_prime)

                random_edges = []
                while len(random_edges) < num_edges * 2:
                    v1 = random.randint(0, self.data['num_nodes'] - 1)
                    v2 = random.randint(0, self.data['num_nodes'] - 1)
                    if (v1, v2) in self.data['edges'] or (v2, v1) in self.data['edges']:
                        continue
                    random_edges.append((v1, v2))
                    random_edges.append((v2, v1))

                _data = copy.deepcopy(self.data)
                _data['edges'] += random_edges
                benign_orig = self.target_model.CEU_train(_data, eval=False, verbose=False)
                benign_unlearn, _ = unlearn(self.args, _data, benign_orig, random_edges, device=self.device)

                _edges = remove_undirected_edges(self.data['edges'], random_edges)
                edge_index_prime = torch.tensor(_edges, device=self.device).t()
                beni_o_pl, beni_r_pl, beni_u_pl = _mia_attack(self.data, benign_orig, original_model,
                                                              benign_unlearn, random_edges, self.device)
                benign_jsd = _efficacy(original_model, benign_unlearn, edge_index_prime)

                jsd_result['# edges'].append(num_edges)
                jsd_result['setting'].append('adv')
                jsd_result['jsd'].append(np.mean(adv_jsd))

                jsd_result['# edges'].append(num_edges)
                jsd_result['setting'].append('benign')
                jsd_result['jsd'].append(np.mean(benign_jsd))

                mia_result['# edges'].append(num_edges)
                mia_result['setting'].append('adv')
                mia_result['privacy leakage'].append(adv_u_pl)

                mia_result['# edges'].append(num_edges)
                mia_result['setting'].append('benign')
                mia_result['privacy leakage'].append(beni_u_pl)

            jsd_df = pd.DataFrame(jsd_result)
            jsd_df.to_csv(os.path.join('./result/CEU', f'rq3_jsd_{self.args["dataset_name"]}_{self.args["base_model"]}.csv'))

            mia_df = pd.DataFrame(mia_result)
            mia_df.to_csv(os.path.join('./result/CEU', f'rq3_mia_{self.args["dataset_name"]}_{self.args["base_model"]}.csv'))

    def adv_retrain_unlearn(self,data, num_edges):
        test_loader = DataLoader(data['test_set'])

        A = self.adversarial_adjacency_mat(data, n_perturbations=int(num_edges))
        print()
        print('The number we asked:', num_edges)
        print('The number of adv edges:', len(A) / 2)

        A = [(v1, v2) for v1, v2 in A]

        D_prime = data['edges'] + A

        data_ = copy.deepcopy(data)
        data_['edges'] = D_prime
        orig_model_prime = self.target_model.CEU_train(data_,eval=False, verbose=False)
        edge_index_d_prime = torch.tensor(D_prime, device=self.device).t()
        orig_res_prime, orig_loss_prime = self.target_model.CEU_test(orig_model_prime, test_loader, edge_index_d_prime)

        unlearn_model_prime, _ = unlearn(self.args, data_, orig_model_prime, A, device=self.device)
        edge_index = torch.tensor(data['edges'], device=self.device).t()
        unlearn_res_prime, unlearn_loss_prime = self.target_model.CEU_test(unlearn_model_prime, test_loader, edge_index)

        return orig_res_prime, orig_loss_prime, unlearn_res_prime, unlearn_loss_prime

    def adv_unlearn(self, data, num_edges):
        A = self.adversarial_adjacency_mat(data, n_perturbations=int(num_edges))
        print()
        print('The number we asked:', num_edges)
        print('The number of adv edges:', len(A))
        A = [(v1, v2) for v1, v2 in A]

        D_prime = data['edges'] + A

        data_ = copy.deepcopy(data)
        data_['edges'] = D_prime
        orig_model_prime = self.target_model.CEU_train(data_,eval=False, verbose=False)
        unlearn_model_prime, _ = unlearn(self.args, data_, orig_model_prime, A, device=self.device)
        return orig_model_prime, unlearn_model_prime, A
    def adversarial_adjacency_mat(self,data, n_perturbations=500):
        # data = load_data(args)
        n_feat = data['features'].shape[1]

        adj_data, row, col = [], [], []
        for v1, v2 in data['edges']:
            row.append(v1)
            col.append(v2)
            adj_data.append(1)
        adj = csr_matrix((adj_data, (row, col)), shape=(data['num_nodes'], data['num_nodes']))

        features = csr_matrix(data['features'])
        # features = data['features']
        labels = data['labels']
        idx_train = [node for node in data['train_set'].nodes]
        idx_val = [node for node in data['valid_set'].nodes]
        idx_test = [node for node in data['test_set'].nodes]
        idx_unlabeled = np.union1d(idx_val, idx_test)
        adj, features, labels = preprocess(adj, features, labels, preprocess_adj=False)  # 将adj和feature转化为tensor
        # adj = adj.to(device)
        # features = features.to(device)
        # labels = labels.to(device)
        victim_model = GCN(nfeat=n_feat, nclass=data['num_classes'],
                           nhid=16, dropout=0.5, weight_decay=5e-4, device=self.device).to(self.device)
        victim_model.fit(features, adj, labels, idx_train, idx_val=idx_val, patience=10, train_iter=20)

        # Setup Attack Model
        model = PGDAttack(model=victim_model, nnodes=adj.shape[0], loss_type='CE', device=self.device).to(self.device)
        # model = MinMax(model=victim_model, nnodes=adj.shape[0], loss_type='CE', device=device).to(device)
        # model = Metattack(victim_model, nnodes=adj.shape[0], feature_shape=features.shape, device=device).to(device)
        # Attack
        try:
            model.attack(features, adj, labels, idx_train, n_perturbations=n_perturbations, attack=20, epochs=20)
            # model.attack(features, adj, labels, idx_train, idx_unlabeled, n_perturbations=n_perturbations)
        except AssertionError as err:
            print('Error:', err)
        modified_adj = model.modified_adj.cpu()  # modified_adj is a torch.tensor
        A = torch.cat(torch.where(modified_adj - adj == 1)).view(2, -1).t().tolist()
        return A

    def determine_target_model(self):
        self.logger.info('target model: %s' % (self.args['base_model'],))
        self.args["unlearn_trainer"] = "CEUTrainer"
        self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)
        
    def train_original_model(self, run):
        self.logger.info('training target models, run %s' % run)
        test_loader = DataLoader(self.data['test_set'], shuffle=False, batch_size=self.args["test_batch"])
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        result = defaultdict(list)
        self.target_model.model = self.target_model.CEU_train(self.data,eval=False, verbose=False,return_epoch=False)
        original_res, _ = self.target_model.CEU_test(self.target_model.model, test_loader, edge_index)
        if self.args["poison"]:
            self.poison_f1 = original_res["accuracy"]
    def unlearning_request(self):
        num_edges = int(self.args["unlearn_ratio"]*self.data["num_edges"])
        _, _, adv_res, _ = self.adv_retrain_unlearn(self.data, num_edges)

        # Benign
        self.random_edges = []
        while len(self.random_edges) < num_edges * 2:
            v1 = random.randint(0, self.data['num_nodes'] - 1)
            v2 = random.randint(0, self.data['num_nodes'] - 1)
            if (v1, v2) in self.data['edges'] or (v2, v1) in self.data['edges']:
                continue
            self.random_edges.append((v1, v2))
            self.random_edges.append((v2, v1))

        self._data = copy.deepcopy(self.data)
        self._data['edges'] += self.random_edges
    
    
    def unlearn(self):
        test_loader = DataLoader(self.data['test_set'], shuffle=False, batch_size=self.args["test_batch"])
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        benign_orig = self.target_model.CEU_train(self._data,eval=False, verbose=False)
        benign_unlearn, _ = unlearn(self.args,self._data, benign_orig, self.random_edges, device=self.device)
        benign_res, _ = self.target_model.CEU_test(benign_unlearn, test_loader, edge_index)
        self.average_f1 = benign_res["accuracy"]