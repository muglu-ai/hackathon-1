# Base image for building the app
FROM node:22.12.0 as build

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire project including the tsconfig.json file
COPY . .

# Build the project
RUN npm run build

# Base image for serving the app
FROM nginx:latest

# Copy built files to NGINX
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the NGINX default port
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
