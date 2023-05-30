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
python -m unittest -b -v

# code coverage. (need to run all tests before generating the code coverage report. Eg: python -m coverage run -m unittest -b -v && coverage report --omit=test_*.py)
python -m coverage report --omit=test_*.py

# code coverage html
coverage html
```

## 5.Run Regression Script
```bash
bash buildTestSuite.sh example@email.com
```
### NOTES:

You should make sure the python version is python:3.9.16, which is specified in the Dockerfile. Using other python versions will lead to unexpected errors

## TIPS: you can use Remote Container VSCode extension to open the container with VSCode for local development
