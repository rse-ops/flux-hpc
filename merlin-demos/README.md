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

You can check the status of your redis and rabbitmq (both should be OK before proceeding):

```bash
$ merlin info
```

<details>

<summary>Output of merlin info</summary>

```console
[2023-03-22 03:39:27: INFO] Reading app config from file /root/.merlin/app.yaml
  
                                                
       *      
   *~~~~~                                       
  *~~*~~~*      __  __           _ _       
 /   ~~~~~     |  \/  |         | (_)      
     ~~~~~     | \  / | ___ _ __| |_ _ __  
    ~~~~~*     | |\/| |/ _ \ '__| | | '_ \ 
   *~~~~~~~    | |  | |  __/ |  | | | | | |
  ~~~~~~~~~~   |_|  |_|\___|_|  |_|_|_| |_|
 *~~~~~~~~~~~                                    
   ~~~*~~~*    Machine Learning for HPC Workflows                                 
              


Merlin Configuration
-------------------------

 config_file        | /root/.merlin/app.yaml
 is_debug           | False
 merlin_home        | /root/.merlin
 merlin_home_exists | True
 broker server      | amqps://root:******@rabbitmq:5671//merlinu
 broker ssl         | {'keyfile': '/cert_rabbitmq/client_rabbitmq_key.pem', 'certfile': '/cert_rabbitmq/client_rabbitmq_certificate.pem', 'ca_certs': '/cert_rabbitmq/ca_certificate.pem', 'cert_reqs': <VerifyMode.CERT_REQUIRED: 2>}
 results server     | rediss://redis:6379/0
 results ssl        | {'ssl_keyfile': '/cert_redis/client_redis_key.pem', 'ssl_certfile': '/cert_redis/client_redis_certificate.pem', 'ssl_ca_certs': '/cert_redis/ca_certificate.pem', 'ssl_cert_reqs': <VerifyMode.CERT_REQUIRED: 2>}

Checking server connections:
----------------------------
broker server connection: OK
results server connection: OK

Python Configuration
-------------------------

 $ which python3
/opt/conda/bin/python3

 $ python3 --version
Python 3.10.9

 $ which pip3
/opt/conda/bin/pip3

 $ pip3 --version
pip 23.0 from /opt/conda/lib/python3.10/site-packages/pip (python 3.10)

"echo $PYTHONPATH"
```

</details>

Note the content of `/root/.merlin/app.yaml` that defines interactions with redis and rabbitmq,
and the password in plain text in /root/.merlin/rabbit.pass. The ownership of the certificates
(and also being bound to the merlin container) is really important - and that is handled
in the respective entrypoint scripts in [scripts](scripts). First, generate
the demo:

```bash
$ merlin example feature_demo
```

Then run the demo workflow (without Flux first):

```bash
$ merlin run feature_demo/feature_demo.yaml
```

From what I can tell, we see output and error in the studies directory:

```bash
# cat studies/feature_demo_20230322-035214/merlin_info/cmd.out 
[[0.78055381 0.02167573]
 [0.34246986 0.81569574]
 [0.12497185 0.54133217]
 [0.23107361 0.2192876 ]
 [0.14349186 0.96902287]
 [0.78745147 0.3541445 ]
 [0.48053942 0.23776201]
 [0.75213343 0.75142001]
 [0.82011063 0.78713369]
 [0.35126391 0.2416619 ]]
```

(and .err is empty).

Now let's try with flux. We need to change the batch type in "feature_demo/feature_demo.yml" to "flux"

```diff
batch:
-    type: local
+    type: flux
```

And then start the flux instance:

```bash
$ # sudo -u fluxuser -E PATH=$PATH -E PYTHONPATH=$PYTHOPATH -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH flux start --test-size=4
$ whoami
fluxuser
$ merlin run feature_demo/feature_demo.yaml
```

TODO: update to run as fluxuser (and not root!)
