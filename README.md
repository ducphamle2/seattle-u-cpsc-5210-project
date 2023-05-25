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

# code coverage. (need to run all tests before generating the code coverage report. Eg: python -m coverage run -m unittest && coverage report)
python -m coverage report
```

## 5.Run Regression Script
```bash
bash buildTestSuite.sh example@email.com
```
### NOTES:

You should make sure the python version is python:3.9.16, which is specified in the Dockerfile. Using other python versions will lead to unexpected errors

## TIPS: you can use Remote Container VSCode extension to open the container with VSCode for local development
