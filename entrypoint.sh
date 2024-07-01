#!/bin/sh -l

# Extract inputs from with github context
OWNER=$INPUT_OWNER
REPOSITORY=$INPUT_REPOSITORY
ACCESS_TOKEN=$INPUT_ACCESS_TOKEN
SECRET_NAME=$INPUT_SECRET_NAME
SECRET_VALUE=$INPUT_SECRET_VALUE

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