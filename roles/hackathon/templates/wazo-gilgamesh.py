#!/usr/bin/env bash

GIT_FOLDER=$1
NOW=$(date)

cd ${GIT_FOLDER}

GIT_ADD=$(git ls-files -om)

if [[ ! "${GIT_ADD}" = "" ]]; then
    git add .
    git commit -m "Updated files ${NOW}"
fi
