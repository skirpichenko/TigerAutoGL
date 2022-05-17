# install KServe
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.7.0/kserve.yaml

# switch between Kubernetes clusters 
gcloud container clusters get-credentials ai02 --region us-west1 --project tigergraph-r

# remove panding pod
kubectl delete pod -n –grace-period 0 –force.

# switch to a specific cluster
gcloud container clusters get-credentials ai00 --region us-west1 --project tigergraph-r


  # channel: REGULAR
  # validVersions:
  # - 1.23.5-gke.1501
  # - 1.22.8-gke.200
  # - 1.22.6-gke.300
  # - 1.21.11-gke.900
  # - 1.21.10-gke.2000
  # - 1.21.10-gke.400
  # - 1.21.9-gke.1002
  # - 1.21.6-gke.1503
  # - 1.20.15-gke.5000


Replace the project, zone, and other values appropriately to reflect your environment.

gcloud beta container clusters create "tns-kserve" \
--project "tigergraph-r" \
--zone "us-west1-a" \
--no-enable-basic-auth \
--cluster-version "1.21.10-gke.2000" \
--machine-type "n1-standard-4" \
--num-nodes "2" \
--image-type "UBUNTU_CONTAINERD" \
--disk-type "pd-standard" \
--disk-size "50" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"


# Step 1 – Launch a GKE Cluster with T4 GPU Node
# --accelerator "type=nvidia-tesla-t4,count=1" \
# --addons=Istio --istio-config=auth=MTLS_PERMISSIVE \
# 1.21.10-gke.2000
# --addons HorizontalPodAutoscaling,HttpLoadBalancing \
gcloud beta container clusters create "tns-kserve" \
--project "tigergraph-r" \
--zone "us-west1-a" \
--no-enable-basic-auth \
--cluster-version "1.21.10-gke.2000" \
--machine-type "n1-standard-2" \
--num-nodes "2" \
--image-type "UBUNTU_CONTAINERD" \
--disk-type "pd-standard" \
--disk-size "100" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"


# delete cluster
gcloud container clusters delete tns-kserve --zone "us-west1-a"

# Add a cluster-admin role for the GCP user.
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$(gcloud config get-value core/account)

# Install Istio
# curl -L https://istio.io/downloadIstio | sh -
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.12.7 TARGET_ARCH=x86_64 sh -
istioctl  
# check Istiao
kubectl get pods -n istio-system

curl -L https://istio.io/downloadIstio | sh -
istioctl install --set profile=demo -y


# Install Knative CRDs and core services.
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-core.yaml  

kubectl label namespace knative-serving istio-injection=enabled

# To integrate Knative with Istio Ingress, run the below commands.
kubectl apply -l knative.dev/crd-install=true -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/net-istio.yaml

# Finally, configure the DNS for Knative that points to the sslip.io domain.
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-default-domain.yaml
# Make sure that Knative Serving is successfully running.
kubectl get pods -n knative-serving

# Step 4 – Installing Certificate Manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.1/cert-manager.yaml
# verify
kubectl get pods -n cert-manager

# Step 5 – Install KServe Model Server
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.8.0/kserve.yaml
# verify
kubectl get pods -n kserve
kubectl get crd | grep "kserve"

# Create test InferenceService¶
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "sklearn-iris"
spec:
  predictor:
    sklearn:
      storageUri: "gs://kfserving-samples/models/sklearn/iris"

# apply
kubectl create namespace kserve-test
kubectl apply -f sklearn.yaml -n kserve-test

# Check InferenceService status
kubectl get inferenceservices sklearn-iris -n kserve-test

# Determine the ingress IP and ports
kubectl get svc istio-ingressgateway -n istio-system


  http://sklearn-iris.kserve-test.35.185.239.43.sslip.io/v1/models/sklearn-iris:predict






