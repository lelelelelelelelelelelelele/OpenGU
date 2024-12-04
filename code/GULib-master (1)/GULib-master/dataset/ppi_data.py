class ppi_data:
    def __init__(self,all_data) :
        self.all_data = all_data
        self.train_out = None
        self.train_y = None
        self.test_out = None
        self.test_y = None
        self.num_features = 50
        self.num_classes = 121
