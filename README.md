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

2. Add it to the network.

```
docker network connect hybrid-ai-net survey-app
```

3. Run build project by docker-compose

```
docker-compose build
docker-compose up
```
