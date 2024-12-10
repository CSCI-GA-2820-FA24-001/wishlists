# NYU DevOps Project Wishlist Service

[![Build Status](https://github.com/CSCI-GA-2820-FA24-001/wishlists/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA24-001/wishlists/actions)
[![Coverage Status](https://codecov.io/gh/CSCI-GA-2820-FA24-001/wishlists/branch/master/graph/badge.svg?token={token})](https://codecov.io/gh/CSCI-GA-2820-FA24-001/wishlists)


[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)


## Overview

This repository contains code for Wishlist Service for an e-commerce website. 

The `/service` folder contains `models.py` and `routes.py` file for our Wishlist model and service. 
The `/tests` folder contains test case for testing the model and the service separately. 

## Setup Development Environment

This repository uses Docker to create a fully isolated and reproducible development environment. We rely on the `.devcontainer` folder's configuration for integration with Docker containers in Visual Studio Code or other development tools that support devcontainer setups.

Ensure you have the following softwares isntalled before starting:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the Visual Studio Marketplace

### Steps
1. Clone the repository using http (or ssh) and open repository in VSCode:
    ```
    git clone https://github.com/CSCI-GA-2820-FA24-001/wishlists.git
    cd wishlists
    code .
    ```
2. If you are using VS Code with the Dev Containers extension installed, you should see a prompt that asks you to reopen the project in a dev container. Click "Reopen in Container."

    Alternatively, you can open the Command Palette (Ctrl + Shift + P or Cmd + Shift + P) and search for Remote-Containers: Reopen in Container.

After the container is up and running, you can start working on the code within the container. All required tools and dependencies should already be set up for you.

## API Routes

These are the RESTful routes for wishlists and items

### Base Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /        | Returns service information in JSON format |

### Wishlists

| Method | Endpoint          | Description |
|--------|-------------------|-------------|
| GET    | /wishlists        | Retrieve all wishlists |
| POST   | /wishlists        | Create a new wishlist |
| GET    | /wishlists/{id}   | Retrieve a specific wishlist by ID |
| PUT    | /wishlists/{id}   | Update a specific wishlist by ID |
| DELETE | /wishlists/{id}   | Delete a specific wishlist by ID |

### Wishlist Items

| Method | Endpoint                      | Description |
|--------|-------------------------------|-------------|
| GET    | /wishlists/{id}/items        | Retrieve all items in a specific wishlist |
| POST   | /wishlists/{id}/items        | Add a new item to a specific wishlist |
| GET    | /wishlists/{id}/items/{id}   | Retrieve a specific item from a wishlist |
| PUT    | /wishlists/{id}/items/{id}   | Update a specific item in a wishlist |
| DELETE | /wishlists/{id}/items/{id}   | Remove a specific item from a wishlist |

<!-- ```
Methods Rule                        Endpoints
------  --------------------------  -----------------------------------------------------
GET      /                           <- Return some json about service

GET      /wishlists                  <- List all wishlists
POST     /wishlists                  <- Create a new wishlist
GET      /wishlists/{id}             <- Read a wishlist
PUT      /wishlists/{id}             <- Update a wishlist
DELETE   /wishlists/{id}             <- Delete a wishlist

GET      /wishlists/{id}/items       <- List all items in a wishlist
POST     /wishlists/{id}/items       <- Create a new item in a wishlist
GET      /wishlists/{id}/items/{id}  <- Read an item from a wishlist
PUT      /wishlists/{id}/items/{id}  <- Update an item in a wishlist
DELETE   /wishlists/{id}/items/{id}  <- Delete an item from a wishlist
``` -->
### Purchase Action for Wishlist item:

| Method | Endpoint                      | Description |
|--------|-------------------------------|-------------|
| PUT | /wishlists/{id}/items/{id}/purchase | Mark a wishlist item as purchased |

### Query Wishlist:
The `/wishlists` endpoint supports the following query parameters:

| Parameter | Description | Format | Example |
|-----------|-------------|---------|---------|
| name | Filter wishlists by name | String | `/wishlists?name=SampleWishlist` |
| userid | Filter wishlists by user ID | String | `/wishlists?userid=12345` |
| date_created | Filter wishlists by creation date | YYYY-MM-DD | `/wishlists?date_created=2024-12-10` |

## Test Driven Development - TDD
Run the unit tests using pytest and check linting with following code:
```
make test
make lint
```

## Behavior Driven Development - BDD 
Use code shown below to run the service. Navigate to http://localhost:8080/ to see service ui page. Alternatively, you can also use VSCode ```Thunder Client``` extension to test services.
```
flask run
# or
honcho start
```

And run behave test with:
```
behave
```

## Deploy to Kubernetes 
Create a K3S cluster in your development environment with:
```
make cluster
```

Deploy postgresql first with
```
kubectl apply -f k8s/postgres
```

Build, tag, and push docker image to local registry:
```
docker build -t nyu-project:latest .
docker tag nyu-project:latest cluster-registry:5000/nyu-project:latest
docker push cluster-registry:5000/nyu-project:latest
```
Deploy application with
```
kubectl apply -f k8s
```

Check running pod
```
kubectl get pods
```

When all pods are running, the wishlist service can then be accessed from http://localhost:8080

## Deploy to Red Hat OpenShift Kubernetes cluster
Connect with OpenShift and its project namespace
```
oc login <login token>
oc project <username>-dev
```
deploy database and add event listener
```
oc apply -f k8s/postgres/
oc apply -f .tekton/events/
```
A sample CD Pipeline with 6 tasks was created in OpenShift:
- clone, lint, test, build an image, deploy it to
Kubernetes, and run BDD tests on the deployment.

A route to microservice was created for access from outside the cluster.
The pipeline and the web hook were set up to trigger the pipeline every time a PR is merged. 


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - environment variables to configure Flask
.gitattributes      - file to gix Windows CRLF issues
.devcontainers/     - folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

service/static/             
│   └── static/
│       ├── css/           - bootstrap theme variations
        ├── ...
│       ├── index.html     - main application HTML template
│       └── js/            - javaScript resources
          └── rest_api.js  - custom REST API interaction code

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
├── test_base.py           - base test classes and common fixtures
├── test_item.py           - item-specific test cases
└── test_wishlist.py       - wishlist feature tests

features/                  - BDD test directory
├── environment.py         - behave test environment setup
├── steps/                 - step definition files
│   ├── web_steps.py       - web interface test steps
│   └── wishlist_steps.py  - wishlist feature test steps
└── wishlist.feature       - wishlist feature specifications in Gherkin

k8s/                       - kubernetes configuration directory
├── deployment.yaml        - main application deployment configuration
├── ingress.yaml           - ingress controller configuration
├── postgres/              - postgreSQL database configurations
│   ├── configmap.yaml     - database configuration settings
│   ├── pvc.yaml           - persistent Volume Claim for database
│   ├── secret.yaml        - database credentials and secrets
│   ├── service.yaml       - database service configuration
│   └── statefulset.yaml   - postgreSQL StatefulSet configuration
├── pv.yaml                - persistent Volume configuration
├── redis.yaml             - Redis cache configuration
├── secret.yaml            - application secrets configuration
└── service.yaml           - application service configuration

```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

