# Networks

[![networks](https://github.com/pieteradejong/networks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/pieteradejong/networks/actions/workflows/ci.yml)


## Goal

## Development
Recommend using `black` formatter and `ruff` linter.


## Dependencies
See `requirements.txt`

## Setup / Usage

To set up your development environment, follow these steps:

1. Clone the repository: `git clone <this-repository-url>`
2. Navigate to the project directory: `cd python-base-app`
3. (Optional) Run the initialization script: `./init.sh`
   - use `chmod +x init.sh` to add execute permissions.
   - sets up a virtual environment and installs  dependencies.
4. If not using the init script, create a virtual environment: `python3 -m venv venv`
5. **Activate the virtual environment**:
   - On Windows: `.\venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`
