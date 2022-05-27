# Create Kubernetes cluster
gcloud beta container clusters create "kdd-demo" \
    --project "tigergraph-r" \
    --zone "us-west1-a" \
    --no-enable-basic-auth \
    --cluster-version "1.19.16-gke.11000" \
    --machine-type "n1-highmem-4" \
    --num-nodes "3" \
    --image-type "UBUNTU_CONTAINERD" \
    --disk-type "pd-standard" \
    --disk-size "100" \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

# Fetch cluste endpoint
gcloud container clusters get-credentials kdd-demo --region us-west1-a --project tigergraph-r

# Add a cluster-admin role for the GCP user.
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$(gcloud config get-value core/account)

# install kustomize 3.2.0
wget https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_linux_amd64
chmod +x kustomize_3.2.0_linux_amd64
sudo mv kustomize /usr/local/bin/kustomize

# clone Kubectl manifest 1.4
git clone -b v1.4-branch https://github.com/kubeflow/manifests.git

# autoinstall
cd ./manifest
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

# delete cluster
gcloud container clusters delete tns-kserve --zone "us-west1-a"

# 1.21.0-gke.1500 and later	    Kubernetes Engine API or Google Cloud CLI	VPC-native
# Earlier than 1.21.0-gke.1500	Kubernetes Engine API or Google Cloud CLI	Routes-based
# You can also create a routes-based cluster by specifying the --no-enable-ip-alias flag when you create the cluster.

gcloud beta container clusters create "kdd-demo4" \
    --project "tigergraph-r" \
    --no-enable-ip-alias \
    --zone "us-west1-a" \
    --cluster-version "1.21.10-gke.2000" \
    --machine-type "n1-highmem-4" \
    --num-nodes "3" \
    --image-type "UBUNTU_CONTAINERD" \
    --disk-type "pd-standard" \
    --disk-size "100" \
    --addons HttpLoadBalancing \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

kubectl apply -f https://github.com/knative/serving/releases/download/v0.22.2/serving-default-domain.yaml

#     --no-enable-basic-auth \
gcloud beta container clusters create "kdd-demo" \
    --project "tigergraph-r" \
    --no-enable-ip-alias \
    --zone "us-west1-a" \
    --cluster-version "1.21.10-gke.2000" \
    --machine-type "n1-highmem-4" \
    --num-nodes "3" \
    --image-type "UBUNTU_CONTAINERD" \
    --disk-type "pd-standard" \
    --disk-size "100" \
    --addons HorizontalPodAutoscaling,HttpLoadBalancing \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

#     --no-enable-basic-auth \
gcloud beta container clusters create "kdd-demo5" \
    --project "tigergraph-r" \
    --no-enable-ip-alias \
    --zone "us-west1-a" \
    --cluster-version "1.21.10-gke.2000" \
    --machine-type "n1-highmem-4" \
    --num-nodes "3" \
    --image-type "UBUNTU_CONTAINERD" \
    --disk-type "pd-standard" \
    --disk-size "100" \
    --addons HorizontalPodAutoscaling,HttpLoadBalancing \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

#     --no-enable-basic-auth \
gcloud beta container clusters create "kdd-demo3" \
    --project "tigergraph-r" \
    --no-enable-ip-alias \
    --zone "us-west1-a" \
    --cluster-version "1.21.10-gke.2000" \
    --machine-type "n1-highmem-4" \
    --num-nodes "3" \
    --image-type "UBUNTU_CONTAINERD" \
    --disk-type "pd-standard" \
    --disk-size "100" \
    --addons HttpLoadBalancing \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"





export KUBEFLOW_USERNAME=user@example.com
export KUBEFLOW_PASSWORD=12341234


wget https://github.com/kubeflow/kfctl/releases/download/v1.2.0/kfctl_v1.2.0-0-gbc038f9_linux.tar.gz
tar -xvf kfctl_v1.2.0-0-gbc038f9_linux.tar.gz 
sudo mv kfctl /usr/local/bin/ 

export PROJECT=tigergraph-r
export ZONE=us-west1-a

export KFAPP=/home/sergey.kirpichenko/TigerAutoGL/Kubernetes/
export CONFIG="https://raw.githubusercontent.com/kubeflow/kubeflow/c54401e/bootstrap/config/kfctl_gcp_basic_auth.0.6.2.yaml"
