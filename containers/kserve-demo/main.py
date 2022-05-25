import kserve
from typing import Dict
import logging

class AlexNetModel(kserve.Model):
    def __init__(self, name: str):
       super().__init__(name)
       self.name = name
       self.load()

    def load(self):
        pass

    def predict(self, request: Dict) -> Dict:
        logging.info ("predicting")
        return {"predictions": [1]}

if __name__ == "__main__":
    model = AlexNetModel("custom-model")
    kserve.ModelServer(http_port=8081).start([model])
