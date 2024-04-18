# Use official Node.js runtime as a parent image
FROM node:14-alpine

# Set work directory
ENV PROJ_DIR=/vue_proj
RUN mkdir -p ${PROJ_DIR}
WORKDIR ${PROJ_DIR}

# Copy package.json and package-lock.json files
COPY ./project_vue/package.json ${PROJ_DIR}
COPY ./project_vue/package-lock.json ${PROJ_DIR}

# Update npm to a compatible version
RUN npm install -g npm@7

# Install project dependencies
RUN npm install

# Copy project files
COPY ./project_vue ${PROJ_DIR}

# Specify the command to run on container startup
CMD ["npm", "run", "serve"]