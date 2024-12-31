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


FROM nginx:stable-alpine AS production-stage

COPY nginx/default.conf /etc/nginx/conf.d/
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
