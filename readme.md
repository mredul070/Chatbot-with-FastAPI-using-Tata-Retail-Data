# Running the Project with Docker Compose

This guide will walk you through the steps to run the project using Docker Compose. Docker Compose is a tool for defining and running multi-container Docker applications.

## Prerequisites

Before you begin, make sure you have Docker and Docker Compose installed on your system. You can install them by following the instructions in the Docker documentation:

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

## Steps

1. **Clone the Repository**: Clone the project repository to your local machine.

2. **Navigate to the Project Directory**: Change to the directory where the project files are located.

3. **Create `.env` File**: Copy the `.env.example` file and create a new file named `.env`. This file will contain environment variables needed for the project. Update the values in the `.env` file as required.

4. **Update Docker Compose Configuration (Optional)**: If needed, update the `docker-compose.yml` file to configure any specific settings such as ports or environment variables.

5. **Build and Run Docker Containers**: Use Docker Compose to build and run the Docker containers defined in the `docker-compose.yml` file.

6. **Access the Application**: Once the containers are up and running, you can access the application by opening a web browser and navigating to the specified URL or port. In this project based on OS you can access this on locahost:5000 or 0.0.0.0:5000

7. **Shut Down the Containers**: To shut down the Docker containers and remove the resources, you can use the following command:

8. **Cleanup (Optional)**: If you want to remove all Docker images, containers, and volumes related to the project, you can use the following commands:

9. **API docs**: access the API doc on /docs endpoint
## Conclusion

By following these steps, you should be able to run the project using Docker Compose. If you encounter any issues, please refer to the project documentation or seek assistance from the project maintainers.
