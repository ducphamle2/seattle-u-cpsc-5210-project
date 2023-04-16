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

## 4. Run tests

```python

# run all tests
pytest

# code coverage
pytest --cov=/workspace ./
```

## TIPS: you can use Remote Container VSCode extension to open the container with VSCode for local development
