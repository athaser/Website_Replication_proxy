
# Flask Proxy Application

A Dockerized Flask app that serves as a proxy server, dynamically fetching and modifying HTML content from target sites. Internal navigation links are rewritten to stay within the proxy.

## Features

- **Dynamic Link Rewriting**: Ensures links navigate within the proxy.
- **JavaScript Injection**: Enhances navigation handling.
- **Dockerized Deployment**: Simplifies setup with Docker Compose.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup and Run

1. **Clone the Repository**:
   Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/athaser/Website_Replication_proxy
   cd Website_Replication_proxy
   ```

2. **Build the Docker Containers**:
   Build the Docker image for the application using Docker Compose:
   ```bash
   docker-compose build
   ```

3. **Start the Application**:
   Run the application using Docker Compose:
   ```bash
   docker-compose up
   ```

4. **Access the Application**:
   Open a web browser and go to the following address:
   ```
   http://localhost:8080
   ```

5. **Stop the Application**:
   To stop the running containers, use the following command:
   ```bash
   docker-compose down
   ```

## Configuration

- **Change Target URL**: Update `TARGET_URL` in `app.py` to set a new target website for proxying.

## File Structure

- **Dockerfile**: Defines the Python environment and installs dependencies.
- **docker-compose.yml**: Manages the services, port mappings, and restart policies.

## Dependencies

Dependencies are listed in `requirements.txt`:
```plaintext
Flask==2.2.5
Flask-Cors==4.0.0
flask-oidc==1.4.0
Flask-Session==0.5.0
requests==2.31.0
beautifulsoup4==4.12.2
```
