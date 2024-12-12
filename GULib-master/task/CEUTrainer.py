from task.BaseTrainer import BaseTrainer
import torch
from tqdm import tqdm
import time
from torch.utils.data import DataLoader
import numpy as np
import os
from sklearn.metrics import classification_report
class CEUTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)
    
    def CEU_train(self,data,eval=True, verbose=True,return_epoch=False):
        # if self.args["downstream_task"]=="node":
        return self.CEU_train_node(data,eval,verbose,return_epoch)
        # elif self.args["downstream_task"]=="edge":
        #     return self.CEU_train_edge(data,eval,verbose,return_epoch)
        
    def CEU_train_node(self,data,eval=True, verbose=True,return_epoch=False):
        if verbose:
            t0 = time.time()
            print(f'Start to train a {self.args["model_name"]} model...')

        model = self.model.to(self.device)
        train_loader = DataLoader(data['train_set'], batch_size=self.args["train_batch"], shuffle=True)
        valid_loader = DataLoader(data['valid_set'], batch_size=self.args["test_batch"])
        edge_index = torch.tensor(data['edges'], device=self.device).t()
        num_epochs = self.args['num_epochs']
        lr = self.args["unlearn_lr"]
        l2 = self.args["l2"]
        patience = self.args["patience"]

        optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=l2)

        best_valid_loss = 999999.
        best_epoch = 0
        trail_count = 0

        for e in range(1, num_epochs + 1):

            train_losses = []

            model.train()
            iterator = tqdm(train_loader, f'  Epoch {e}') if verbose else train_loader
            for nodes, labels in iterator:
                model.zero_grad()

                nodes = nodes.to(self.device)
                labels = labels.to(self.device)

                y_hat = model(nodes, edge_index)
                loss = model.loss(y_hat, labels)
                loss.backward()
                optimizer.step()

                train_losses.append(loss.cpu().item())

            train_loss = np.mean(train_losses)

            valid_losses = []

            model.eval()
            with torch.no_grad():
                for nodes, labels in valid_loader:
                    nodes = nodes.to(self.device)
                    labels = labels.to(self.device)

                    y_hat = model(nodes, edge_index)
                    loss = model.loss(y_hat, labels)

                    valid_losses.append(loss.cpu().item())

            valid_loss = np.mean(valid_losses)

            if verbose:
                print(f'  Epoch {e}, training loss: {train_loss:.4f}, validation loss: {valid_loss:.4f}.')

            if self.args["early_stop"]:
                if valid_loss < best_valid_loss:
                    best_valid_loss = valid_loss
                    trail_count = 0
                    best_epoch = e
                    path = os.path.join('./data/CEU/checkpoint', 'tmp')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    torch.save(model.state_dict(), path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
                else:
                    trail_count += 1
                    if trail_count > patience:
                        if verbose:
                            print(
                                f'  Early Stop, the best Epoch is {best_epoch}, validation loss: {best_valid_loss:.4f}.')
                        break
            else:
                path = os.path.join('./data/CEU/checkpoint','tmp')
                if not os.path.exists(path):
                    os.makedirs(path)
                torch.save(model.state_dict(),path+f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
        path = os.path.join('./data/CEU/checkpoint', 'tmp')
        model.load_state_dict(torch.load(path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt'))

        if eval:
            self.CEU_evaluate()

        # os.remove(os.path.join('./checkpoint', 'tmp', f'{args.model}_{args.data}_{args.gpu}_best.pt'))

        if verbose:
            print(f'{self.args["base_model"]} model training finished. Duration:', int(time.time() - t0))

        if return_epoch:
            return model, num_epochs
        else:
            return model

    def CEU_train_edge(self,data,eval=True, verbose=True,return_epoch=False):
        if verbose:
            t0 = time.time()
            print(f'Start to train a {self.args["model_name"]} model...')

        model = self.model.to(self.device)
        train_loader = DataLoader(data['train_set'], batch_size=self.args["train_batch"], shuffle=True)
        valid_loader = DataLoader(data['valid_set'], batch_size=self.args["test_batch"])
        edge_index = torch.tensor(data['edges'], device=self.device).t()
        
        num_epochs = self.args['num_epochs']
        lr = self.args["unlearn_lr"]
        l2 = self.args["l2"]
        patience = self.args["patience"]

        optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=l2)

        best_valid_loss = 999999.
        best_epoch = 0
        trail_count = 0

        for e in range(1, num_epochs + 1):

            train_losses = []

            model.train()
            iterator = tqdm(train_loader, f'  Epoch {e}') if verbose else train_loader
            for nodes, labels in iterator:
                model.zero_grad()

                nodes = nodes.to(self.device)
                labels = labels.to(self.device)

                y_hat = model(nodes, edge_index)
                
                loss = model.loss(y_hat, labels)
                
                loss.backward()
                optimizer.step()

                train_losses.append(loss.cpu().item())

            train_loss = np.mean(train_losses)

            valid_losses = []

            model.eval()
            with torch.no_grad():
                for nodes, labels in valid_loader:
                    nodes = nodes.to(self.device)
                    labels = labels.to(self.device)

                    y_hat = model(nodes, edge_index)
                    loss = model.loss(y_hat, labels)

                    valid_losses.append(loss.cpu().item())

            valid_loss = np.mean(valid_losses)

            if verbose:
                print(f'  Epoch {e}, training loss: {train_loss:.4f}, validation loss: {valid_loss:.4f}.')

            if self.args["early_stop"]:
                if valid_loss < best_valid_loss:
                    best_valid_loss = valid_loss
                    trail_count = 0
                    best_epoch = e
                    path = os.path.join('./data/CEU/checkpoint', 'tmp')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    torch.save(model.state_dict(), path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
                else:
                    trail_count += 1
                    if trail_count > patience:
                        if verbose:
                            print(
                                f'  Early Stop, the best Epoch is {best_epoch}, validation loss: {best_valid_loss:.4f}.')
                        break
            else:
                path = os.path.join('./data/CEU/checkpoint','tmp')
                if not os.path.exists(path):
                    os.makedirs(path)
                torch.save(model.state_dict(),path+f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
        path = os.path.join('./data/CEU/checkpoint', 'tmp')
        model.load_state_dict(torch.load(path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt'))

        if eval:
            self.CEU_evaluate()

        # os.remove(os.path.join('./checkpoint', 'tmp', f'{args.model}_{args.data}_{args.gpu}_best.pt'))

        if verbose:
            print(f'{self.args["base_model"]} model training finished. Duration:', int(time.time() - t0))

        if return_epoch:
            return model, num_epochs
        else:
            return model



    @torch.no_grad()
    def CEU_test(self,model, test_loader, edge_index):
        y_preds = []
        y_trues = []
        test_loss = []
        model.eval()
        with torch.no_grad():
            for nodes, labels in test_loader:
                nodes, labels = nodes.to(self.device), labels.to(self.device)
                y_hat = model(nodes, edge_index)
                test_loss.append(model.loss(y_hat, labels).cpu().item())
                y_pred = torch.argmax(y_hat, dim=1)
                y_preds.extend(y_pred.cpu().tolist())
                y_trues.extend(labels.cpu().tolist())
        # del model
        # torch.cuda.empty_cache()
        res = classification_report(y_trues, y_preds, digits=4, output_dict=True)
        return res, np.mean(test_loss)

    @torch.no_grad()
    def CEU_evaluate(self):
        test_loader = DataLoader(self.data['test_set'], batch_size=self.args['test_batch'], shuffle=False)
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        y_preds = []
        y_true = []

        self.model.eval()
        with torch.no_grad():
            for nodes, labels in test_loader:
                nodes = nodes.to(self.device)
                labels = labels.to(self.device)

                y_hat = self.model(nodes, edge_index)
                y_pred = torch.argmax(y_hat, dim=1)

                y_preds.extend(y_pred.cpu().tolist())
                y_true.extend(labels.cpu().tolist())

        results = classification_report(y_true, y_preds, digits=4)
        print('  Result:')
        print(results)