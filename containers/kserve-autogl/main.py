import torch
import kserve
from typing import Dict
import logging
import pyTigerGraph as tg
from torch_geometric.nn import GCN
import os
import autogl
from autogl.data import InMemoryStaticGraphSet
from autogl.data.graph import GeneralStaticGraphGenerator
import dill

logger = logging.getLogger(__name__)
conn = tg.TigerGraphConnection("http://35.230.92.92", graphname="Cora")

# Hyperparameters
hp = {"batch_size": 64, "num_neighbors": 10, "num_hops": 2}

class AutoglNodeClassifier(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.infer_loader = conn.gds.neighborLoader(
            v_in_feats=["x"],
            v_out_labels=["y"],
            output_format="PyG",
            batch_size=hp["batch_size"],
            num_neighbors=hp["num_neighbors"],
            num_hops=hp["num_hops"],
            shuffle=False
        )
        # should be loaded from gstorage, s3 etc
        self.solver = self.load_model('/opt/kserve-demo/binaries/autoClassifier.dill')

    def load(self):
        pass
    
    def load_model(self, filename):
        logger.info(f"Loading AutoGL Model: {filename}")
        with open(filename, 'rb') as f:
            solver = dill.load(f)
        for m in solver.trained_models.values():
            if m.encoder:
                m.encoder.model.to(self.device)
            if m.decoder:
                m.decoder.model.to(self.device)
        logger.info("Loaded Model")
        return solver

    def predict(self, request: Dict) -> Dict:
        input_nodes = request["nodes"]
        input_ids = set([str(node['primary_id']) for node in input_nodes])
        logger.info(input_ids)
        data = self.infer_loader.fetch(input_nodes)
        logger.info (f"predicting {data}")
        
        mask = torch.ones(data.x.size()[0], dtype=torch.bool)
        static_graph = GeneralStaticGraphGenerator.create_homogeneous_static_graph(
            {
                'x': data.x.float(),
                'y': data.y,
                'train_mask': mask,
                'val_mask': mask,
                'test_mask': mask
            },
            data.edge_index
        )
        dataset = InMemoryStaticGraphSet([static_graph])
        
        pred = self.solver.predict(dataset, inplaced = False, inplace = True)
        ret = {"predictions": []}
        for primary_id, label in zip(data.primary_id, pred):
            if primary_id in input_ids:
                ret['predictions'].append({'primary_id': primary_id, 'label': label.item()})
        return ret

if __name__ == "__main__":
    model_name = os.environ.get('K_SERVICE', "tg-gcn-kserve-autogl-predictor-default")
    model_name = '-'.join(model_name.split('-')[:-2]) # removing suffix "-predictor-default"
    logging.info(f"Starting model '{model_name}'")
    model = AutoglNodeClassifier(model_name)
    kserve.ModelServer(http_port=8080).start([model])
