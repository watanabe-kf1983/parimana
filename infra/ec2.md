
in AL2023

```
sudo dnf install git
export WATANABE_TOKEN=`aws secretsmanager get-secret-value --secret-id watanabe-github-token --query 'SecretString' --output text`
git clone https://$WATANABE_TOKEN@github.com/watanabe-kf1983/parimana.git
cd parimana

```
curl -sSL https://install.python-poetry.org | python3 -

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
npm install node
```
