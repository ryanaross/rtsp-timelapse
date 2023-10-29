# rtsp-timelapse
## Overview
This project uses Docker to run a Python script that captures still images from an RTSP stream at regular intervals and compiles them into a timelapse video. The script is configured using environment variables which can be set in a .env file for development or directly in the docker-compose.yaml file for deployment.

## Development
To start development, create a .env file in the root directory and set the necessary environment variables as described in `config.py`. The Python script `main.py` uses these variables to control the behavior of the timelapse creation.

## Deployment
For deployment, the environment variables can be set directly in the docker-compose.yaml file. Once the variables are set, you can use Docker Compose to build and run the application.
