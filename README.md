# Uptime alert
Checks if specified URLs are responding, raises an alert if not.  
Will retry to ignore transient errors. Default retry limit is 60 seconds.  
Can be used as serverless function, in docker or in kubernetes.  
Uptime is running on schedule, no resources are used between checks.  
Schedule can be configured when deploying, more details on this are in [Deployment options](#deployment-options)

## Configuration
Configuration is done via ENV variables.  
Variables available:
```
# Comma delimited list of URLs to monitor
MONITORED_URLS
SENTRY_DSN
# How long to retry request on single URL before raising an alert
RETRY_LIMIT_SECONDS
```

## Deployment options
### Kubernetes
Edit `kubernetes-job.yaml` before applying - change monitored URLs and Sentry DSN
```
wget https://raw.githubusercontent.com/xobed/uptime-alert/master/kubernetes-job.yaml
kubectl -f kubernetes-job.yaml
```

### Kubernetes with Helm
```
helm upgrade --install uptime-alert \
    --set monitored_urls="https://example.com/" \
    --set sentry_dsn="https://token@mysentry.ingest.sentry.io/123" \
    ./helm/uptime-alert
```

### Docker swarm service
```
docker service create -e MONITORED_URLS="https://example.com/" -e SENTRY_DSN="https://token@mysentry.ingest.sentry.io/123" --name uptime-alert --restart-delay=60s --detach xobed/uptime-alert
```

## Development
### Build locally
```shell script
docker build . -t xobed/uptime-alert
docker run -it --rm -e MONITORED_URLS="https://example.com/" -e SENTRY_DSN="https://token@mysentry.ingest.sentry.io/123" --name uptime-alert xobed/uptime-alert
```

### Package helm chart
```
cd helm
helm package uptime-alert
helm repo index .
```
