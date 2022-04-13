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

from requests import request
import grpc
import time
from pkg.apis.manager.v1beta1.python import api_pb2_grpc
from pkg.apis.manager.health.python import health_pb2_grpc
from pkg.suggestion.v1beta1.autogl.service import HyperoptService
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
DEFAULT_PORT = "0.0.0.0:6789"


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = HyperoptService()
    api_pb2_grpc.add_SuggestionServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)
    server.add_insecure_port(DEFAULT_PORT)
    print("I am listening...")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    


if __name__ == "__main__":
    from pkg.apis.manager.v1beta1.python.api_pb2 import GetSuggestionsRequest, AlgorithmSetting
    print ('Loading AutpGL spec...')
    with open('autogl_spec.yaml') as f:
        spec = f.read()
        spec = spec.replace('\n', '#')
        
    request = GetSuggestionsRequest()
    autogl_setting = AlgorithmSetting(name='autogl_spec', value=spec)
    request.experiment.spec.algorithm.algorithm_settings.append(autogl_setting)
    
    service = HyperoptService()
    service.GetSuggestions(request, None)
    
    #serve()