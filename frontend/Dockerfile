# Base image
FROM node:23-alpine

# Set working directory
WORKDIR /app

# Copy only package.json and package-lock.json (if available) - for caching dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy remaining files
COPY . .

# Expose the port used by Vite
EXPOSE 5173

# Start the dev server with external access
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
