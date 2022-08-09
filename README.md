# Introduction

Survey app. This software will be mapped to the frontend. This tool is a main connection channel

This application lives on the local computer and connects to the remote survey app server.

# Local installation

Easiest way to run this app is to run a docker container. Docker should be installed before.

1. Create a network for local interactions between different containers (or use existing if you already have it).
   Example network is `hybrid-ai-net`

```
docker network create hybrid-ai-net
```


2. Create .env file like that

```
PG_USERNAME='change'
PG_PASSWORD='change'
PG_DATABASE='change'
```

3. Add it to the network.

```
docker network connect hybrid-ai-net survey-app
```

4. Should open main.py file and uncomment lines of code(for creating tables in database):
```
from models import database#, metadata, engine
# metadata.create_all(engine)
```
5. Run build project by docker-compose

```
docker-compose build
docker-compose up
```
