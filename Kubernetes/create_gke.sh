#!/usr/bin/env bash

# Step 1 – Launch a GKE Cluster 
# --accelerator "type=nvidia-tesla-t4,count=1" \
# --addons HorizontalPodAutoscaling,HttpLoadBalancing \
gcloud beta container clusters create "tns-kserve" \
--project "tigergraph-r" \
--zone "us-west1-a" \
--no-enable-basic-auth \
--cluster-version "1.21.10-gke.2000" \
--machine-type "n1-standard-4" \
--num-nodes "3" \
--image-type "UBUNTU_CONTAINERD" \
--disk-type "pd-standard" \
--disk-size "50" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"

# Add a cluster-admin role for the GCP user.
kubectl create clusterrolebinding cluster-admin-binding \
    --clusterrole=cluster-admin \
    --user=$(gcloud config get-value core/account)

deploymentMode=serverless
export ISTIO_VERSION=1.9.0
export KNATIVE_VERSION=v0.22.0
export KSERVE_VERSION=v0.7.0
export CERT_MANAGER_VERSION=v1.3.0

KUBE_VERSION=$(kubectl version --short=true)

echo ${KUBE_VERSION:43:2}

if [ ${KUBE_VERSION:43:2} -gt 20 ]; then export ISTIO_VERSION=1.10.3; export KNATIVE_VERSION=v0.23.2; fi

curl -L https://git.io/getLatestIstio | sh -
cd istio-${ISTIO_VERSION}

# Create istio-system namespace
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: istio-system
  labels:
    istio-injection: disabled
EOF

cat << EOF > ./istio-minimal-operator.yaml
apiVersion: install.istio.io/v1beta1
kind: IstioOperator
spec:
  values:
    global:
      proxy:
        autoInject: disabled
      useMCP: false
      # The third-party-jwt is not enabled on all k8s.
      # See: https://istio.io/docs/ops/best-practices/security/#configure-third-party-service-account-tokens
      jwtPolicy: first-party-jwt

  meshConfig:
    accessLogFile: /dev/stdout

  addonComponents:
    pilot:
      enabled: true

  components:
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
EOF

if [ $(cut -d '.' -f 2,2 <<< $ISTIO_VERSION) -gt 9 ]
then
    bin/istioctl install --set profile=demo -y;
else
    bin/istioctl manifest apply -f istio-minimal-operator.yaml -y;
fi

# Install Knative
if [ $deploymentMode = serverless ]; then
   kubectl apply --filename https://github.com/knative/serving/releases/download/${KNATIVE_VERSION}/serving-crds.yaml
   kubectl apply --filename https://github.com/knative/serving/releases/download/${KNATIVE_VERSION}/serving-core.yaml
   kubectl apply --filename https://github.com/knative/net-istio/releases/download/${KNATIVE_VERSION}/release.yaml
fi

# Install Cert Manager
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager-webhook -n cert-manager
cd ..
# Install KFServing
KSERVE_CONFIG=kfserving.yaml
if [ ${KSERVE_VERSION:3:1} -gt 6 ]; then KSERVE_CONFIG=kserve.yaml; fi

# Retry inorder to handle that it may take a minute or so for the TLS assets required for the webhook to function to be provisioned
for i in 1 2 3 4 5 ; do kubectl apply -f https://github.com/kserve/kserve/releases/download/${KSERVE_VERSION}/${KSERVE_CONFIG} && break || sleep 15; done
# Clean up
rm -rf istio-${ISTIO_VERSION}

# configure the DNS for Knative that points to the sslip.io domain.
# kubectl apply -f https://github.com/knative/serving/releases/download/${KNATIVE_VERSION}/serving-default-domain.yaml

kubectl get pods -A

echo "ISTIO_VERSION=${ISTIO_VERSION}"
echo "KNATIVE_VERSION=${KNATIVE_VERSION}"
echo "KSERVE_VERSION=${KSERVE_VERSION}"
echo "CERT_MANAGER_VERSION=${CERT_MANAGER_VERSION}"