FROM node:18 AS node-base


FROM node-base AS vscode-devcontainer

# install git sudo
RUN apt-get update \
    && apt-get -y install git sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add non-root user
ARG USERNAME=vscode
ARG USER_ID=1001
ARG GROUP_ID=$USER_ID

RUN groupadd --gid $GROUP_ID $USERNAME \
    && useradd -s /bin/bash --uid $USER_ID --gid $GROUP_ID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/


FROM node-base AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Nginxの設定ファイルをコピー（必要に応じて）
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
