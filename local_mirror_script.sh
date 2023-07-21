#!/usr/bin/env bash
# This script is workable for only Quok's machine

# git checkout main
git config credential.helper gcloud.sh
git status

if ! git remote | grep -q 'google'; then
    git remote add google https://source.developers.google.com/p/ecomercebackend-393408/r/cs428-backend
else
    echo "The google git remote is already existed"
fi

git push --set-upstream google quocnd/deploy_backend_gcp