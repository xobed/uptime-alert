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
TODO

### Docker swarm service
TODO

### Google Cloud Run
TODO

## Development
Build locally
```shell script
docker build . -t uptimealert
```
