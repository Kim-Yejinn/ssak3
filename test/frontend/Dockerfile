# Use an official Node.js runtime as the base image
FROM node
# Set the working directory in the container
WORKDIR /workspace
# Copy the package.json and package-lock.json files
COPY package*.json ./
# Install the dependencies
RUN npm install
# Copy the React project files
COPY . ./
# Build the Vue project
RUN npm run build

# Use Nginx as the web server
FROM nginx
# nginx 의 default.conf 를 삭제
RUN rm /etc/nginx/conf.d/default.conf
# host pc 의 nginx.conf 를 아래 경로에 복사
COPY ./nginx.conf /etc/nginx/conf.d
# Copy the build files to the Nginx web root directory
COPY --from=build /app/build /usr/share/nginx/html
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
