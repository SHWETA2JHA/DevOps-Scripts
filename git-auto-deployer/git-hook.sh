#!/bin/bash

REPO_DIR="/path/to/your/repo"
BRANCH="main"

cd "$REPO_DIR" || exit
git fetch origin "$BRANCH"

LOCAL=$(git rev-parse "$BRANCH")
REMOTE=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "New changes found. Pulling latest code..."
  git pull origin "$BRANCH"
  # Optional: restart service
  # systemctl restart myapp.service
else
  echo "No new changes."
fi
