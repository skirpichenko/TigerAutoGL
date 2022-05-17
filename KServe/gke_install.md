# Step 1 – Launch a GKE Cluster 
# --accelerator "type=nvidia-tesla-t4,count=1" \
gcloud beta container clusters create "tns-kserve" \
--project "tigergraph-r" \
--zone "us-west1-a" \
--no-enable-basic-auth \
--cluster-version "1.21.10-gke.2000" \
--addons HorizontalPodAutoscaling,HttpLoadBalancing \
--machine-type "n1-standard-2" \
--num-nodes "2" \
--image-type "UBUNTU_CONTAINERD" \
--disk-type "pd-standard" \
--disk-size "50" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

# Add a cluster-admin role for the GCP user.
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$(gcloud config get-value core/account)

# Install Istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.12.7 TARGET_ARCH=x86_64 sh -
./istio-1.12.7/bin/istioctl install --set profile=demo -y

# Install Knative CRDs and core services.
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-core.yaml  

# To integrate Knative with Istio Ingress, run the below commands.
kubectl apply -l knative.dev/crd-install=true -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.2.0/net-istio.yaml

# Finally, configure the DNS for Knative that points to the sslip.io domain.
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.2.0/serving-default-domain.yaml

# Step 4 – Installing Certificate Manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.1/cert-manager.yaml

# Step 5 – Install KServe Model Server
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.8.0/kserve.yaml

# create a model
kubectl create namespace kserve-test
kubectl apply -f sklearn.yaml -n kserve-test

kubectl get pods --all-namespaces

# Check InferenceService status
kubectl get inferenceservices sklearn-iris -n kserve-test