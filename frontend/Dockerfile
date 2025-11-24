# Step 1: Build the React app
FROM node:18-alpine as builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
ARG REACT_APP_API_BASE
ENV REACT_APP_API_BASE=$REACT_APP_API_BASE
RUN npm run build

# Step 2: Serve it with Nginx
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80



# frontend/Dockerfile
#FROM nginx:alpine

#COPY . /usr/share/nginx/html
#EXPOSE 70
