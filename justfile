init:
    if [ ! -f requirements.lock ]; then rye sync; fi
    rye run pre-commit install
    docker build -t gprk-base:latest . && docker-compose build

start:
    docker-compose up

stop:
    docker-compose down

format:
    rye run ruff format
    rye run ruff . --fix # sort headers + linting

