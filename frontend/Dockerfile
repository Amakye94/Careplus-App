FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Clear default nginx HTML
RUN rm -rf ./*

# Copy your static frontend files
COPY . .

EXPOSE 80
