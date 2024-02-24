# csit-hack-backend

## Pre-requisites
* Python
* Docker
* [`just`](https://github.com/casey/just) (optional)

## Usage

1. Add `POSTGRES_PASSWORD` to `.env` file: `echo "POSTGRES_PASSWORD=pwd" > .env`
2. If `just` is installed, run `just init` and then `just start`, otherwise, copy commands from `init` and `start` recipes and run them in shell
