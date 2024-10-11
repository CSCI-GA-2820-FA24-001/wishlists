# NYU DevOps Project Wishlist Service

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
    cd your-repo
    code .
    ```
2. If you are using VS Code with the Dev Containers extension installed, you should see a prompt that asks you to reopen the project in a dev container. Click "Reopen in Container."

    Alternatively, you can open the Command Palette (Ctrl + Shift + P or Cmd + Shift + P) and search for Remote-Containers: Reopen in Container.

After the container is up and running, you can start working on the code within the container. All required tools and dependencies should already be set up for you.
## Information About this Repo
These are the RESTful routes for wishlists and items

```
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
```

## Running the Tests
Run the unit tests using pytest

```
make test
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
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

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
