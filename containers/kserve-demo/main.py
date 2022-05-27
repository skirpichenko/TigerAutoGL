import torch
import kserve
from typing import Dict
import logging
import pyTigerGraph as tg
from torch_geometric.nn import GCN

logger = logging.getLogger(__name__)
conn = tg.TigerGraphConnection("http://35.230.92.92", graphname="Cora")

# Hyperparameters
hp = {"batch_size": 64, "num_neighbors": 10, "num_hops": 2, "hidden_dim": 64,
      "num_layers": 2, "dropout": 0.6, "lr": 0.01, "l2_penalty": 5e-4}

class GCNNodeClassifier(kserve.Model):
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
        self.model = self.load_model('/opt/kserve-demo/binaries/model.pth')

    def load(self):
        pass
    
    def load_model(self, filename):
        model = GCN(
            in_channels=1433,
            hidden_channels=hp["hidden_dim"],
            num_layers=hp["num_layers"],
            out_channels=7,
            dropout=hp["dropout"],
        )
        logger.info("Instantiated Model")
        model.load_state_dict(torch.load(filename))
        model.to(self.device).eval()
        logger.info("Loaded Model")
        return model

    def predict(self, request: Dict) -> Dict:
        input_nodes = request["nodes"]
        input_ids = set([str(node['primary_id']) for node in input_nodes])
        logger.info(input_ids)
        data = self.infer_loader.fetch(input_nodes)
        logger.info (f"predicting {data}")
        pred = self.model(data.x.float(), data.edge_index).argmax(dim=1)
        ret = {"predictions": []}
        for primary_id, label in zip(data.primary_id, pred):
            if primary_id in input_ids:
                ret['predictions'].append({'primary_id': primary_id, 'label': label.item()})
        return ret

if __name__ == "__main__":
    model = GCNNodeClassifier("tg-gcn-kserve-demo")
    kserve.ModelServer(http_port=8080).start([model])
