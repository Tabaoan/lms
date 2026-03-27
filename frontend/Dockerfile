FROM node:18-alpine
WORKDIR /app

# Cài đặt dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

EXPOSE 5173

# Chạy Vite ở chế độ host để map port ra ngoài Docker
CMD ["npm", "run", "dev", "--", "--host"]