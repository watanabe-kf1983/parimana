FROM public.ecr.aws/docker/library/node:24 AS node-base



FROM node-base AS build-stage

ARG BUILD_OPT="dev" 

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build.${BUILD_OPT}



FROM nginx:stable-alpine AS production-stage

COPY nginx/default.conf /etc/nginx/conf.d/
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
