# Tutorial

## 1. Install docker & docker-compose

## 2. Build the docker image

```bash
docker build -t cpsc5210-startrek .
```

## 3. Start the container

```bash
docker-compose up -d
```

## 4. Start The container shell

```bash
docker-compose exec startrek sh
```

## 4. Run tests

```python

# run all tests
python -m unittest

# code coverage
python -m coverage report
```

### NOTES:

You should make sure the python version is python:3.9.16, which is specified in the Dockerfile. Using other python versions will lead to unexpected errors

## TIPS: you can use Remote Container VSCode extension to open the container with VSCode for local development
