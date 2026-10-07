FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json next-env.d.ts postcss.config.js tailwind.config.ts ./
RUN npm install
COPY app ./app
COPY lib ./lib
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
