#!/bin/sh

gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.src:app