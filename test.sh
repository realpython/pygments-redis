#!/bin/sh
NC='\033[0m'
if python3 -m unittest -v tests/test_redis.py && flake8 --exclude=venv* .; then
    GRN='\033[0;32m'
    echo "${GRN}Success${NC}"
    exit 0
else
    RED='\033[0;31m'
    echo "${RED}Failed${NC}"
    exit 1
fi
