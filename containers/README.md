git config --global user.email "skirpichenko@gmail.com" && git config --global user.name "Sergey Kirpichenko"

docker build -t autogl .

# run container
sudo docker run -t -d -p 3000:3000 autogl 

# stop all containers
docker kill $(docker ps -q)

# install docker 
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ${USER}
su -s ${USER}

# list pods
kubectl get pods -n kubeflow

# list pods of specific namespace
 kubectl get pods -n kubeflow-user-example-com

# show log (add --follow to stream it)
kubectl logs -n kubeflow-user-example-com random-experiment-my-79rv5gcw metrics-logger-and-collector

# describe example
kubectl -n kubeflow-user-example-com describe experiment autogl-08
kubectl -n kubeflow-user-example-com get experiment autogl-08 -o yaml

# edit katib config
kubectl edit configMap katib-config -n kubeflow