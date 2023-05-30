#!/bin/bash

# The email address to send the status to
email=$1

# Start the container
docker-compose up -d && build_status=true || build_status=false

# Run the tests
test_results=$(docker-compose exec -T startrek sh -c "python -m unittest 2>&1")
test_status=true

# Check if the tests failed
if echo "$test_results" | grep -q "FAILED"; then
  test_status=false
fi

# Send the email
echo -e "Build Status: $build_status\nTest Status: $test_status" | mail -s "Build and Test Results" $email
