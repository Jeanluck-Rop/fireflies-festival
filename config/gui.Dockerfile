FROM node:20

WORKDIR /app

COPY ../gui/package*.json ./

RUN npm install

COPY ../gui .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
