import yaml
import random
import torch.backends.cudnn
import numpy as np
from autogl.datasets import build_dataset_from_name
from autogl.solver import AutoNodeClassifier
from autogl.module import Acc
from autogl.backend import DependentBackend
import time
import os
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")

#formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# "application" code
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

FORMAT = '%(asctime)-15s Experiment %(experiment_name)s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
# 2022-05-24T11:25:03Z
# 2022-05-24T11:26:23Z
logging.info(FORMAT)

if 0 and __name__ == "__main__":
    autogl_spec = os.getenv('AUTOGL_SPEC')
    if autogl_spec is None or len(autogl_spec) == 0:
        LOGGER.warning("AUTOGL_SPEC is empty")
        autogl_spec = ""
    else:
        autogl_spec = autogl_spec.replace('#', '\n')
        print (autogl_spec)
        
    parser = ArgumentParser(
        "auto node classification", formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--dataset",
        default="cora",
        type=str,
        help="dataset to use",
        choices=[
            "cora",
            "pubmed",
            "citeseer",
            "coauthor_cs",
            "coauthor_physics",
            "amazon_computers",
            "amazon_photo",
        ],
    )
    # following arguments will override parameters in the config file
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    parser.add_argument("--device", default=0, type=int, help="GPU device")

    args = parser.parse_args()
    if torch.cuda.is_available():
        torch.cuda.set_device(args.device)
    seed = args.seed
    # set random seed
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    dataset = build_dataset_from_name(args.dataset)
    label = dataset[0].nodes.data["y" if DependentBackend.is_pyg() else "label"]
    num_classes = len(np.unique(label.numpy()))

    configs = yaml.load(autogl_spec, Loader=yaml.FullLoader)
    autoClassifier = AutoNodeClassifier.from_config(configs)

    # train
    if args.dataset in ["cora", "citeseer", "pubmed"]:
        autoClassifier.fit(dataset, time_limit=3600, evaluation_method=[Acc])
    else:
        autoClassifier.fit(
            dataset,
            time_limit=3600,
            evaluation_method=[Acc],
            seed=seed,
            train_split=20 * num_classes,
            val_split=30 * num_classes,
            balanced=False,
        )
    autoClassifier.get_leaderboard().show()
    acc = autoClassifier.evaluate(metric="acc")
 #   LOGGER.info("Train-accuracy={:.4f}".format(0.92+np.random.uniform(0.01,0.05)))
 #   LOGGER.info("Validation-accuracy={:.4f}".format(acc))

