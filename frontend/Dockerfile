FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build --configuration=production

# Stage 2: serve with nginx
FROM nginx:alpine
COPY --from=builder /app/dist/* /usr/share/nginx/html
