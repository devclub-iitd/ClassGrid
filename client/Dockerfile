FROM node:latest

WORKDIR /frontend

COPY /client /frontend

RUN npm install

ENTRYPOINT [ "npm", "run", "build" ]