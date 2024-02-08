FROM node:20 AS node-base


FROM node-base AS vscode-devcontainer

# install git sudo
RUN apt-get update \
    && apt-get -y install git sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER node

FROM node-base AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build


FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Nginxの設定ファイルをコピー（必要に応じて）
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
