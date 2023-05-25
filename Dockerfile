FROM python:3.9.16

# Install necessary packages
RUN apt-get update && apt-get install -y mailutils

# Install Python packages
RUN pip install parameterized coverage