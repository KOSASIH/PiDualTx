# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies only when needed
COPY package.json package-lock.json* ./
RUN npm install

# Copy source files
COPY . .

# Build the Vue.js app
RUN npm run build

# Production stage
FROM nginx:stable-alpine

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
