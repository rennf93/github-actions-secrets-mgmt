#!/bin/sh -l

# Debugging: Print all INPUT_ prefixed environment variables
echo "Debugging INPUT variables:"
env | grep INPUT_

# Extract inputs from 'with' GitHub context using the INPUT_ prefix
OWNER="${INPUT_OWNER}"
REPOSITORY="${INPUT_REPOSITORY}"
ACCESS_TOKEN="${INPUT_ACCESS_TOKEN}"
SECRET_NAME="${INPUT_SECRET_NAME}"
SECRET_VALUE="${INPUT_SECRET_VALUE}"

# Debugging: Print extracted variables
echo "OWNER: $OWNER"
echo "REPOSITORY: $REPOSITORY"
echo "ACCESS_TOKEN: $ACCESS_TOKEN"
echo "SECRET_NAME: $SECRET_NAME"
echo "SECRET_VALUE: $SECRET_VALUE"

# Check if required inputs are provided
if [ -z "$OWNER" ]; then
  echo "OWNER is a required input and must be set."
  exit 1
fi

if [ -z "$REPOSITORY" ]; then
  echo "REPOSITORY is a required input and must be set."
  exit 1
fi

if [ -z "$ACCESS_TOKEN" ]; then
  echo "ACCESS_TOKEN is a required input and must be set."
  exit 1
fi

if [ -z "$SECRET_NAME" ]; then
  echo "SECRET_NAME is a required input and must be set."
  exit 1
fi

if [ -z "$SECRET_VALUE" ]; then
  echo "SECRET_VALUE is a required input and must be set."
  exit 1
fi

# Run the Python script with the provided inputs
python /usr/src/app/run.py "$OWNER" "$REPOSITORY" "$ACCESS_TOKEN" "$SECRET_NAME" "$SECRET_VALUE"