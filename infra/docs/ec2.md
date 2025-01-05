
## in AL2023

### Clone me
```
sudo dnf install git
export WATANABE_TOKEN=`aws secretsmanager get-secret-value --secret-id watanabe-github-token --query 'SecretString' --output text`
git clone https://$WATANABE_TOKEN@github.com/watanabe-kf1983/parimana.git
cd parimana
```

### Install docker
```
sudo dnf install -y git docker containerd cni-plugins container-selinux udica
sudo usermod -aG docker ec2-user
sudo systemctl enable --now docker
sudo restart
```

### Install docker-compose
```
sudo curl -sL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

#DOCKER_CONFIG=/usr/local/lib/docker
#DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
#mkdir -p $DOCKER_CONFIG/cli-plugins
#chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# verify 
docker-compose --version
```
