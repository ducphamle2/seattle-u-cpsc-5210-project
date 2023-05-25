#!/bin/bash

# The email address to send the status to
email=$1

# Build the docker container
docker build -t cpsc5210-startrek . && build_status=true || build_status=false

# Start the container
docker-compose up -d

# Run the tests
test_results=$(docker-compose exec -T startrek sh -c "python -m unittest")
test_status=true

# Check if the tests failed
if echo "$test_results" | grep -q "FAILED"; then
  test_status=false
fi

# Send the email
echo -e "Build Status: $build_status\nTest Status: $test_status" | mail -s "Build and Test Results" $email
