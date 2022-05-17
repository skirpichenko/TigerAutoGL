#!/usr/bin/env bash

kubectl create namespace kserve-test

kubectl apply -n kserve-test -f - <<EOF
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "sklearn-iris"
spec:
  predictor:
    sklearn:
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
EOF

kubectl get inferenceservice -n kserve-test
echo -e ""

cat <<EOF > "./iris-input.json"
{
  "instances": [
    [6.8,  2.8,  4.8,  1.4],
    [6.0,  3.4,  4.5,  1.6]
  ]
}
EOF

MODEL_NAME=sklearn-iris
INPUT_PATH=@./iris-input.json

SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -n kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)
CLUSTER_IP=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo -e "Host: ${SERVICE_HOSTNAME} http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH"
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH
echo -e "\n"

curl -v ${SERVICE_HOSTNAME}
echo -e "\n"
