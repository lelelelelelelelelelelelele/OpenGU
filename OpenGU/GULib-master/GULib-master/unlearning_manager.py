import numpy as np
import copy
from unlearning.unlearning_methods.CEU.ceu import ceu
from unlearning.unlearning_methods.GraphEraser.grapheraser import grapheraser
from unlearning.unlearning_methods.GUIDE.guide import guide
from unlearning.unlearning_methods.GIF.gif import gif
from unlearning.unlearning_methods.CGU.cgu import cgu
from unlearning.unlearning_methods.SGU.sgu import sgu
from unlearning.unlearning_methods.GST.gst_based import gst
from unlearning.unlearning_methods.Projector.projector import projector
from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete
from unlearning.unlearning_methods.MEGU.megu import megu
from unlearning.unlearning_methods.UTU.utu import utu
from unlearning.unlearning_methods.GraphRevoker.graphrevoker import graphrevoker
from unlearning.unlearning_methods.GUKD.gukd import gukd
from unlearning.unlearning_methods.D2DGN.d2dgn import d2dgn
from unlearning.unlearning_methods.IDEA.idea import idea
from utils.dataset_utils import process_data,save_data
from attack.Attack_methods.GraphEraser_MIA import GraphEraser_Attack
from attack.Attack_methods.GUIDE_MIA import GUIDE_MIA
from attack.MIA_attack import GCNShadowModel
from attack.MIA_attack import train_shadow_model
from attack.MIA_attack import generate_shadow_model_output
from attack.MIA_attack import train_attack_model
# import optuna


class UnlearningManager:
    def __init__(self, args, original_data, data, logger, model_zoo, dataset=None):
        self.args = args
        self.original_data = original_data
        self.data = data
        self.logger = logger
        self.model_zoo = model_zoo
        self.dataset = dataset

    def run(self):
        method = self.args["unlearning_methods"]

        if method == "GraphEraser":
            self.run_graph_eraser()

        elif method == "GNNDelete":
            self.run_gnn_delete()

        elif method == "CGU":
            self.run_cgu()

        elif method == "SGU":
            self.run_sgu()

        elif method == "GIF":
            self.run_gif()

        elif method == "GUIDE":
            self.run_guide()

        elif method == "GST":
            self.run_gst()

        elif method == "Projector":
            self.run_projector()

        elif method == "MEGU" :
            self.run_megu()
            
        elif method == "GraphRevoker":
            self.run_graphrevoker()

        elif method == "UTU":
            self.run_UTU()
        elif method == "GUKD":
            self.run_GUKD()
        elif method == "D2DGN":
            self.run_D2DGN()
        elif method == "IDEA":
            self.run_IDEA()
        elif method == "CEU":
            self.run_CEU()
        else:
            self.logger.error(f"Unknown unlearning method: {method}")
            raise ValueError(f"Unknown unlearning method: {method}")

    def run_graph_eraser(self):
        GraphEraser = grapheraser(self.args, self.original_data, self.logger, self.model_zoo)
        GraphEraser.run_exp()

    def run_gnn_delete(self):
        GNNDelete = gnndelete(self.args,self.logger, self.model_zoo, self.dataset)
        GNNDelete.run_exp()
    def run_cgu(self):
        CGU = cgu(self.logger, self.args,self.model_zoo)
        CGU.run_exp()

    def run_sgu(self):
        SGU = sgu(self.args, self.logger, self.model_zoo)
        SGU.run_exp()

    def run_gif(self):
        GIF = gif(self.args, self.dataset, self.logger, self.model_zoo)
        GIF.run_exp()

    def run_guide(self):
        GUIDE = guide( self.args, self.logger, self.model_zoo)
        GUIDE.run_exp()
    def run_gst(self):
        GST = gst(self.args, self.logger, self.model_zoo)
        GST.run_exp()

    def run_projector(self):
        Projector = projector(self.args, self.logger, self.model_zoo)
        Projector.run_exp()

    def run_megu(self):
        MEGU = megu(self.args,self.logger,self.model_zoo)
        MEGU.run_exp()

    def run_graphrevoker(self):
        GraphRevoker = graphrevoker(self.args,self.logger,self.model_zoo)
        GraphRevoker.run_exp()
    
    def run_UTU(self):
        UTU = utu(self.args,self.logger,self.model_zoo)
        UTU.run_exp()

    def run_GUKD(self):
        GUKD = gukd(self.args,self.logger,self.model_zoo)
        GUKD.run_exp()

    def run_D2DGN(self):
        D2DGN = d2dgn(self.args,self.logger,self.model_zoo)
        D2DGN.run_exp()

    def run_IDEA(self):
        IDEA = idea(self.args,self.logger,self.model_zoo)
        IDEA.run_exp()

    def run_CEU(self):
        CEU = ceu(self.args,self.logger,self.model_zoo)
        CEU.run_exp()

    def train_attack(self):
        shadow_model = GCNShadowModel(self.data.num_features, 64, self.data.num_classes)
        trained_shadow_model = train_shadow_model(shadow_model, self.data)
        train_x = generate_shadow_model_output(shadow_model, self.data)
        input_dim = train_x.shape[1]
        attack_model = train_attack_model(train_x,input_dim)


    


