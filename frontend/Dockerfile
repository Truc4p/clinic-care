FROM node:20-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install --production
COPY frontend ./
ENV NUXT_PUBLIC_API_BASE=http://backend:8000
EXPOSE 3000
CMD ["npm", "run", "dev"]
