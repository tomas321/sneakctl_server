#!/bin/bash

FLASK_ENV="development"

# already satisfied in Dockerfile
#[ "x$PROJECT_DIR" == "x" ] && exit 1
#
#cd $PROJECT_DIR || exit 1

FLASK_ENV=$FLASK_ENV python3 -m flask run --host=0.0.0.0
