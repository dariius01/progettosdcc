# STAGE 1: Build Angular
FROM node:18 AS build
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install -g @angular/cli && npm install

COPY . .
RUN ng build --configuration production

# STAGE 2: Nginx
FROM nginx:1.25-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /usr/src/app/dist/appweb/browser /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
