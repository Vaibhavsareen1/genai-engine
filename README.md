# genai-engine
Backend engine for building and serving generative AI applications.

## Repository Structure Explained

### `docs/`
Contains the knowledge base for the engine's evolution and technical specifications.

1. `docs/adr/`: Architecture Decision Records. These documents track the "why" behind our technical choices (e.g. choice of vector database, async framework or other complexities that help build a better system for generative AI applications).

### `chat_service/`
Contains code related to chat services

### `library/`
Contains common code that is shared across all types of services.


## How to setup the project
The project currently works with python 3.12. For the services to run you need to setup an `.env` file which is your version of `.env-example` file. The project is built using a core image which is built using `Dockerfile.AICoreImage` and all services are connected over a bridge network called `ai-network`.

Therefore we need the following steps to be performed before you can build the project and start working with it
1. Setup your env file using `.env-example`
2. Build core image using `Dockerfile.AICoreImage`. You can run the command ```docker build image -f Dockerfile.AICoreImage -t ai-core-image:latest .```
3. Build the network on which every service is connected to each other called `ai-network`. You can run the command ```docker network create --driver bridge ai-network```

Once these are configured you can do run the following command ```docker compose up``` if all of the containers have been build or ```docker compose up --build``` to rebuilt the containers.

## Current implementation
The project will contain services that are model provider agnostic but currently only few model providers are supported because for the sake of only development. More models will be added once their addition provides additional benefits.

### Current model providers supported
1. Open AI 
2. Google