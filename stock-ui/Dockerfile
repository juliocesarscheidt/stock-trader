FROM node:16-alpine as builder
LABEL maintainer="Julio Cesar <julio@blackdevs.com.br>"

WORKDIR /app

COPY package.json yarn.lock nginx.conf ./

RUN yarn install --production=true
COPY . .
RUN yarn run build --mode production

FROM nginx:1-alpine as runtime
EXPOSE 80

COPY --from=builder --chown=nginx:nginx /app/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html
