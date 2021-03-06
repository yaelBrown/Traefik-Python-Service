# Traefik-Python-Service
Use Python to update configuration of Traefik Proxy

```
version: '3'
services:
  reverse-proxy:
    # The official v2 Traefik docker image
    image: traefik:v1.7
    # Enables the web UI and tells Traefik to listen to docker
    command: --api --rest --docker --debug --loglevel=DEBUG
    ports:
      # The HTTP port
      - "80:80"
      # The Web UI (enabled by --api.insecure=true)
      - "8080:8080"
    volumes:
      # So that Traefik can listen to the Docker events
      - /var/run/docker.sock:/var/run/docker.sock
```

```
docker-compose up
```

```
python3 app.py
```