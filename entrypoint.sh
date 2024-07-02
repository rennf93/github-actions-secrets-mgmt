#!/bin/sh -l

# Extract inputs from 'with' GitHub context using the INPUT_ prefix
export OWNER="${INPUT_OWNER}"
export REPOSITORY="${INPUT_REPOSITORY}"
export ACCESS_TOKEN="${INPUT_ACCESS_TOKEN}"
export SECRET_NAME="${INPUT_SECRET_NAME}"
export SECRET_VALUE="${INPUT_SECRET_VALUE}"

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
python /usr/src/app/run.py