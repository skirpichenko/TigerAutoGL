# Copyright 2021 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc
import yaml

from pkg.apis.manager.v1beta1.python import api_pb2
from pkg.apis.manager.v1beta1.python import api_pb2_grpc

from pkg.suggestion.v1beta1.internal.search_space import HyperParameterSearchSpace
from pkg.suggestion.v1beta1.internal.trial import Trial, Assignment
from pkg.suggestion.v1beta1.hyperopt.base_service import BaseHyperoptService
from pkg.suggestion.v1beta1.internal.base_health_service import HealthServicer

import torch.backends.cudnn
import numpy as np

from autogl.datasets import build_dataset_from_name
from autogl.solver.classifier.node_classifier import AutoNodeClassifier
from autogl.module import Acc
from autogl.backend import DependentBackend
from autogl.module.model.pyg._model_registry import MODEL_DICT
from autogl.module.hpo.base import HP_LIST

import logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

import types

# class Model(object):
#     def __init__(self):
#         pass
#     def train(self, param1, param2):
#         print ('model/tran', param1, param2)


def train_wrap(self, *arg, **kwargs):
    print ('wrapped train')
    return self._original_train(*arg, **kwargs)

# if __name__ == '__main__':
#     model_reg = {'model': Model()}

#     for name, model in model_reg.items():
#         model._original_train = model.train
#         model.train = types.MethodType(train_wrap, model)

#     model_reg['model'].train('param1', 'param2')

from google.cloud import storage
import tempfile
import joblib
 

def RunAutoGL(spec):
    HP_LIST['State'] = 'Collecting'
    dataset = build_dataset_from_name("cora")
    label = dataset[0].nodes.data["y" if DependentBackend.is_pyg() else "label"]
    LOGGER.info(label)
    num_classes = len(np.unique(label.numpy()))
    configs = yaml.load(spec, Loader=yaml.FullLoader)
    

    
    # for name, model in MODEL_DICT.items():
    #     print (name)
    #     model._original_train = model.initialize
    #     model.initialize = types.MethodType(train_wrap, model)
        
   # print (MODEL_DICT)
    
    autoClassifier = AutoNodeClassifier.from_config(configs)
    autoClassifier.fit(dataset, time_limit=3600, evaluation_method=[Acc])
    
    print (HP_LIST)
    
   # print (MODEL_DICT)
   
    # Instantiates a client
    storage_client = storage.Client()
    # The name for the new bucket
    bucket_name = "automl-cache"
    # Creates the new bucket
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = "dataset.pickle"
    blob = bucket.blob(destination_blob_name)
    tmp_file_name = tempfile.gettempdir()+'/'+destination_blob_name
    # read in
    blob.download_to_filename(tmp_file_name)
    dataset = joblib.load(tmp_file_name)
    print (dataset)

class HyperoptService(api_pb2_grpc.SuggestionServicer, HealthServicer):

    def __init__(self):
        super(HyperoptService, self).__init__()
        self.base_service = None
        self.is_first_run = True

    def GetSuggestions(self, request, context):
        if self.is_first_run:
            LOGGER.info("AutoGL suggestion service")
            
            for s in request.experiment.spec.algorithm.algorithm_settings:
                print (s.name)
                if s.name == 'autogl_spec':
                    #logger.info(type(s.value))
                    #logger.info(s.value.replace('#','\n'))
                    RunAutoGL(s.value.replace('#','\n'))
            self.is_first_run = False
                    
    def ValidateAlgorithmSettings(self, request, context):
        is_valid = True
        if not is_valid:
            message = "invalid syntax"
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(message)
            LOGGER.error(message)
        return api_pb2.ValidateAlgorithmSettingsReply()
            


# class HyperoptService(api_pb2_grpc.SuggestionServicer, HealthServicer):

#     def __init__(self):
#         super(HyperoptService, self).__init__()
#         self.base_service = None
#         self.is_first_run = True

#     def GetSuggestions(self, request, context):
#         """
#         Main function to provide suggestion.
#         """
#         name, config = OptimizerConfiguration.convert_algorithm_spec(
#             request.experiment.spec.algorithm)

#         if self.is_first_run:
#             logger.info("AutoGL suggestion service")
            
#             for s in request.experiment.spec.algorithm.algorithm_settings:
#                 if s.name == 'autogl_spec':
#                     logger.info(type(s.value))
#                     logger.info(s.value.replace('#','\n'))
            
#             search_space = HyperParameterSearchSpace.convert(request.experiment)
#             self.base_service = BaseHyperoptService(
#                 algorithm_name=name,
#                 algorithm_conf=config,
#                 search_space=search_space)
#             self.is_first_run = False

#         trials = Trial.convert(request.trials)
#         new_assignments = self.base_service.getSuggestions(trials, request.current_request_number)
#         return api_pb2.GetSuggestionsReply(
#             parameter_assignments=Assignment.generate(new_assignments)
#         )

#     def ValidateAlgorithmSettings(self, request, context):
#         is_valid, message = OptimizerConfiguration.validate_algorithm_spec(
#             request.experiment.spec.algorithm)
#         if not is_valid:
#             context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
#             context.set_details(message)
#             logger.error(message)
#         return api_pb2.ValidateAlgorithmSettingsReply()


# class OptimizerConfiguration:
#     __conversion_dict = {
#         'tpe': {
#             'gamma': lambda x: float(x),
#             'prior_weight': lambda x: float(x),
#             'n_EI_candidates': lambda x: int(x),
#             "random_state": lambda x: int(x),
#         },
#         "random": {
#             "random_state": lambda x: int(x),
#         }
#     }

#     @classmethod
#     def convert_algorithm_spec(cls, algorithm_spec):
#         ret = {}
#         setting_schema = cls.__conversion_dict[algorithm_spec.algorithm_name]
#         for s in algorithm_spec.algorithm_settings:
#             if s.name in setting_schema:
#                 ret[s.name] = setting_schema[s.name](s.value)

#         return algorithm_spec.algorithm_name, ret

#     @classmethod
#     def validate_algorithm_spec(cls, algorithm_spec):
#         algo_name = algorithm_spec.algorithm_name
#         if algo_name == 'tpe':
#             return cls._validate_tpe_setting(algorithm_spec.algorithm_settings)
#         elif algo_name == 'random':
#             return cls._validate_random_setting(algorithm_spec.algorithm_settings)
#         else:
#             return False, "unknown algorithm name {}".format(algo_name)

#     @classmethod
#     def _validate_tpe_setting(cls, algorithm_settings):
#         for s in algorithm_settings:
#             try:
#                 if s.name == 'gamma':
#                     if not 1 > float(s.value) > 0:
#                         return False, "gamma should be in the range of (0, 1)"
#                 elif s.name == 'prior_weight':
#                     if not float(s.value) > 0:
#                         return False, "prior_weight should be great than zero"
#                 elif s.name == 'n_EI_candidates':
#                     if not int(s.value) > 0:
#                         return False, "n_EI_candidates should be great than zero"
#                 elif s.name == 'random_state':
#                     if not int(s.value) >= 0:
#                         return False, "random_state should be great or equal than zero"
#                 else:
#                     return False, "unknown setting {} for algorithm tpe".format(s.name)
#             except Exception as e:
#                 return False, "failed to validate {name}({value}): {exception}".format(
#                     name=s.name, value=s.value, exception=e)

#         return True, ""

#     @classmethod
#     def _validate_random_setting(cls, algorithm_settings):
#         for s in algorithm_settings:
#             if s.name == 'autogl_spec':
#                 continue
#             try:
#                 if s.name == 'random_state':
#                     if not (int(s.value) >= 0):
#                         return False, "random_state should be great or equal than zero"
#                 else:
#                     return False, "unknown setting {} for algorithm random".format(s.name)
#             except Exception as e:
#                 return False, "failed to validate {name}({value}): {exception}".format(
#                     name=s.name, value=s.value, exception=e)

#         return True, ""
