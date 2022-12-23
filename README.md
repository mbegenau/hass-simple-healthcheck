# HomeAssistant Simple Healthcheck component

Currently HomeAssistant is not exposing healthcheck endpoint which can be used by K8s or docker.

This component tries to change that. It should be used only be people who really needs it, and understand how it works.

**This component will not ensure that yours HomeAssistant installation is really healthy.**

Initial discussion about HealthCheck endpoint was started [here](https://github.com/home-assistant/architecture/discussions/650).

Component was created for my K8s HomeAssistant deployment, but any comments or contribution is welcome!

## How it works

* Users need to create `simple_healthcheck_keepalive` automation
* Component creates new HTTP endpoint `/healthz`

## HTTP endpoint `/healthz`

This component will create new HomeAssistant endpoint `/healthz`.

By default this endpoint requires HomeAssistant authentication with [long term token](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token).

### Healthy response
```
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 17
< Date: Tue, 02 Nov 2021 19:30:32 GMT
< Server: Python/3.9 aiohttp/3.7.4.post0
<
{"healthy": true}
```

### Unhealthy response
```
< HTTP/1.1 500 Internal Server Error
< Content-Type: application/json
< Content-Length: 18
< Date: Tue, 02 Nov 2021 19:30:31 GMT
< Server: Python/3.9 aiohttp/3.7.4.post0
<
{"healthy": false}
```
