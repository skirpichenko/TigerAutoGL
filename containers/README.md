sudo usermod -aG docker $USER
docker build -t autogl .

# run container
sudo docker run -t -d -p 3000:3000 autogl 

# stop all containers
docker kill $(docker ps -q)
