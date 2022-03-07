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