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

# Add a cluster-admin role for the GCP user.
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$(gcloud config get-value core/account)
