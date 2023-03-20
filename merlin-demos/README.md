# Merlin Demo with Flux

This small demo will run merlin alongside redis and Flux. We will do this by way
of following [this tutorial](https://merlin.readthedocs.io/en/latest/modules/installation/installation.html#id5) 
and using a container with redis, and a container we build with Flux and the demo.

## 1. Certificates

Let's generate certificates locally to bind to the containers:

```bash
mkdir -p ./merlinu/cert_rabbitmq
git clone https://github.com/michaelklishin/tls-gen.git
cd tls-gen/basic
make CN=rabbitmq CLIENT_ALT_NAME=rabbitmq SERVER_ALT_NAME=rabbitmq
cp result/* ../../merlinu/cert_rabbitmq
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

Note that this doesn't work for me because my merlin container cannot see redit or rabbitmq - likely
some bug that I can't figure out with my setup. What we *could try* is getting the hostnames manually:

```bash
$ docker exec -it redis /bin/bash -c "cat /etc/hosts | grep $(hostname)"
```
