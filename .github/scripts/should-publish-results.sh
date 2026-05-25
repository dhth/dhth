#!/usr/bin/env bash

if git diff --quiet -- README.md; then
    echo 0
else
    echo 1
fi
