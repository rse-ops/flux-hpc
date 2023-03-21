# Merlin Demo with Flux

This small demo will run merlin alongside redis and Flux. We will do this by way
of following [this tutorial](https://merlin.readthedocs.io/en/latest/modules/installation/installation.html#id5) 
and using a container with redis, and a container we build with Flux and the demo.

## 1. Certificates

Let's generate certificates locally to bind to the containers. First for
rabbitmq:

```bash
mkdir -p ./merlinu/cert_rabbitmq
git clone https://github.com/michaelklishin/tls-gen.git
cd tls-gen/basic
make CN=rabbitmq CLIENT_ALT_NAME=rabbitmq SERVER_ALT_NAME=rabbitmq
cp result/* ../../merlinu/cert_rabbitmq
```

And now redis:

```bash
make CN=redis CLIENT_ALT_NAME=redis SERVER_ALT_NAME=redis
make verify
mkdir -p ../../merlinu/cert_redis
cp result/* ../../merlinu/cert_redis
```

You can then delete the tls-gen repository, as we won't need it again.

```bash
cd ../../
rm -rf ./tls-gen
```

## 2. Docker Build

We will need to build two containers - one for merlin, and one for rabbitmq.
I pushed them to a temporary location:

```bash
$ docker compose build
```

And bring them up! This will pull redis and then start both containers.

```bash
$ docker compose up -d
```

You can see your containers running:

```bash
$ docker compose ps
```
```console
NAME                IMAGE                   COMMAND                  SERVICE             CREATED             STATUS                  PORTS
merlin              merlin-demos-merlin     "tail -f /dev/null"      merlin              13 seconds ago      Up Less than a second   
rabbitmq            rabbitmq:3-management   "docker-entrypoint.s…"   rabbitmq            14 seconds ago      Up Less than a second   0.0.0.0:5671-5672->5671-5672/tcp, :::5671-5672->5671-5672/tcp, 4369/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15671-15672->15671-15672/tcp, :::15671-15672->15671-15672/tcp
redis               redis:latest            "docker-entrypoint.s…"   redis               14 seconds ago      Up 1 second             0.0.0.0:6379->6379/tcp, :::6379->6
```

## 3. Merlin

Next, let's shell into the Merlin container.

```bash
$ docker exec -it merlin bash
```

Note the content of `/root/.merlin/app.yaml` that defines interactions with redis and rabbitmq,
and the password in plain text in /root/.merlin/rabbit.pass. Then run the demo workflow (without Flux first):

```bash
$ merlin run feature_demo/feature_demo.yaml
```

Note that this doesn't work for me because of ssl:
Here is what redis sees inside the container:

```
redis  | total 32
redis  | -rw-rw-r-- 1 1000 1000 1281 Mar 21 18:25 ca_certificate.pem
redis  | -rw------- 1 1000 1000 1704 Mar 21 18:25 ca_key.pem
redis  | -rw------- 1 1000 1000 3437 Mar 21 18:25 client_redis.p12
redis  | -rw-rw-r-- 1 1000 1000 1253 Mar 21 18:25 client_redis_certificate.pem
redis  | -rw------- 1 1000 1000 1708 Mar 21 18:25 client_redis_key.pem
redis  | -rw------- 1 1000 1000 3501 Mar 21 18:25 server_redis.p12
redis  | -rw-rw-r-- 1 1000 1000 1338 Mar 21 18:25 server_redis_certificate.pem
redis  | -rw------- 1 1000 1000 1704 Mar 21 18:25 server_redis_key.pem
```
When I use the entrypoint command:

```
    command:
      - --port 0
      - --tls-port 6379
      - --tls-ca-cert-file /cert_redis/ca_certificate.pem
      - --tls-key-file /cert_redis/server_redis_key.pem
      - --tls-cert-file /cert_redis/server_redis_certificate.pem
      - --tls-auth-clients no
```

I get permission denied

```
redis  | 1:M 21 Mar 2023 18:45:24.753 # Failed to configure TLS. Check logs for more info.
redis  | 1:C 21 Mar 2023 18:45:26.884 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis  | 1:C 21 Mar 2023 18:45:26.884 # Redis version=7.0.9, bits=64, commit=00000000, modified=0, pid=1, just started
redis  | 1:C 21 Mar 2023 18:45:26.884 # Configuration loaded
redis  | 1:M 21 Mar 2023 18:45:26.885 # Failed to load private key: /cert_redis/server_redis_key.pem: error:0200100D:system library:fopen:Permission denied
redis  | 1:M 21 Mar 2023 18:45:26.885 # Failed to configure TLS. Check logs for more info.
```
And that doesn't make sense because the user in the container is root. When I change ownership of that directory to uid 0 it doesn't change the error.
