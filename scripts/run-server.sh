#!/usr/bin/env bash

echo "$(dirname "$0")/src/manage.py"
python "$(dirname "$0")/src/manage.py" runserver