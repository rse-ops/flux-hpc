# Merlin Demo with Flux

> This is a modified demo to include certs with the containers, only to make it easier to test on the Flux Operator. This is not recommended for a production workflow!

This small demo will run merlin alongside redis and Flux. We will do this by way
of following [this tutorial](https://merlin.readthedocs.io/en/latest/modules/installation/installation.html#id5) 
and using a container with redis, and a container we build with Flux and the demo.

## 1. Certificates

See [merlin-demos](../merlin-demos) for how the certificates were generated.

## 2. Docker Build

**IMPORTANT** these containers (and the configs for rabbitmq and app.yaml) have been modified to work with the root user. 
If you want to fall back a container with fluxuser you'll need to change them back. The change was made on October 23, 2023
if you want to go back in git history. I figure nobody cares so I'm moving forward with the updated Flux Operator design
(that just uses root).

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
NAME                IMAGE                   COMMAND                  SERVICE             CREATED             STATUS              PORTS
merlin              merlin-demos-merlin     "tail -f /dev/null"      merlin              16 seconds ago      Up 15 seconds       
rabbitmq            merlin-demos-rabbitmq   "/bin/sh -c '/entryp…"   rabbitmq            17 seconds ago      Up 15 seconds       0.0.0.0:5671-5672->5671-5672/tcp, :::5671-5672->5671-5672/tcp, 4369/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15671-15672->15671-15672/tcp, :::15671-15672->15671-15672/tcp
redis               merlin-demos-redis      "/bin/sh -c /entrypo…"   redis               17 seconds ago      Up 15 seconds       0.0.0.0:6379->6379/tcp, :::6379->6379/tcp
```

## 3. Merlin

Next, let's shell into the Merlin container.

```bash
$ docker exec -it merlin bash
```

Start a flux instance:

```bash
$ flux start --test-size=4
```

You can check the status of your redis and rabbitmq (both should be OK before proceeding):

```bash
$ merlin info
```

<details>

<summary>Output of merlin info</summary>

```console
[2023-03-22 05:19:34: INFO] Reading app config from file /home/fluxuser/.merlin/app.yaml
  
                                                
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

 config_file        | /home/fluxuser/.merlin/app.yaml
 is_debug           | False
 merlin_home        | /home/fluxuser/.merlin
 merlin_home_exists | True
 broker server      | amqps://fluxuser:******@rabbitmq:5671//merlinu
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

Note the content of `/home/fluxuser/.merlin/app.yaml` that defines interactions with redis and rabbitmq,
and the password in plain text in /home/fluxuser/.merlin/rabbit.pass. Within each service container,
the ownership of the certificates (and also being bound to the merlin container) is really important - 
and that is handled in the respective entrypoint scripts in [scripts](scripts). First, look at all the
demos we can choose from:

```bash
$ merlin example list
```

Generate flux par assets and copy our tweaked file:

```bash
$ merlin example flux_par
$ cp flux_par.yaml ./flux/flux_par.yaml
```

The tweaked example is customized to have the
queue removed (/workflow/flux/flux_par.yaml). And then run:

```bash
$ merlin run flux/flux_par.yaml
```

If I understand this correctly, that doesn't actually run anything, but it queues
up the tasks (this interaction is a bit confusing). To run:

```bash
$ merlin run-workers flux/flux_par.yaml
```

You'll see a ton of output!

<details>

<summary>Output of run-workers</summary>

Note that this example output is from the `flux_test` workflow (I tested first).

```bash
fluxuser@f47514a02ad9:/workflow$ flux-mini: WARNING: ⚠️ flux-mini is deprecated, use flux-batch, flux-run, etc.⚠️
 
 -------------- celery@f47514a02ad9 v5.2.7 (dawn-chorus)
--- ***** ----- 
-- ******* ---- Linux-5.15.0-67-generic-x86_64-with-glibc2.27 2023-03-22 05:51:10
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         merlin:0x7f2d766ced10
- ** ---------- .> transport:   amqps://fluxuser:**@rabbitmq:5671//merlinu
- ** ---------- .> results:     rediss://redis:6379/0
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> [merlin]_flux_test exchange=[merlin]_flux_test(direct) key=[merlin]_flux_test
                

[tasks]
  . merlin.common.tasks.add_merlin_expanded_chain_to_chord
  . merlin.common.tasks.expand_tasks_with_samples
  . merlin.common.tasks.merlin_step
  . merlin:chordfinisher
  . merlin:queue_merlin_study
  . merlin:shutdown_workers

[2023-03-22 05:51:10,544: INFO] Connected to amqps://fluxuser:**@rabbitmq:5671//merlinu
[2023-03-22 05:51:10,555: INFO] mingle: searching for neighbors
[2023-03-22 05:51:11,589: INFO] mingle: all alone
[2023-03-22 05:51:11,607: INFO] celery@f47514a02ad9 ready.
[2023-03-22 05:51:11,610: INFO] Task merlin.common.tasks.expand_tasks_with_samples[443dbd42-86c5-43e9-a4f5-78a4607778de] received
[2023-03-22 05:51:11,713: INFO] generating next step for range 0:10 10
[2023-03-22 05:51:11,713: INFO] queuing expansion task 0:10
[2023-03-22 05:51:11,777: INFO] merlin expansion task 0:10 queued
[2023-03-22 05:51:11,781: INFO] Task merlin.common.tasks.expand_tasks_with_samples[443dbd42-86c5-43e9-a4f5-78a4607778de] succeeded in 0.06810438202228397s: None
[2023-03-22 05:51:11,783: INFO] Task merlin.common.tasks.expand_tasks_with_samples[041123cd-3f25-4be8-9e66-3458ad4cd0ac] received
[2023-03-22 05:51:11,784: INFO] generating next step for range 0:10 10
[2023-03-22 05:51:11,784: INFO] queuing expansion task 0:10
[2023-03-22 05:51:11,798: INFO] merlin expansion task 0:10 queued
[2023-03-22 05:51:11,800: INFO] Task merlin.common.tasks.expand_tasks_with_samples[041123cd-3f25-4be8-9e66-3458ad4cd0ac] succeeded in 0.01624516403535381s: None
[2023-03-22 05:51:11,802: INFO] Task merlin.common.tasks.add_merlin_expanded_chain_to_chord[1df822ce-044e-4e50-aca7-120ab454d0ab] received
[2023-03-22 05:51:11,960: INFO] Task merlin.common.tasks.add_merlin_expanded_chain_to_chord[1df822ce-044e-4e50-aca7-120ab454d0ab] succeeded in 0.1564375190064311s: ReturnCode.OK
[2023-03-22 05:51:11,961: INFO] Task merlin.common.tasks.merlin_step[4792709d-f792-44f9-a423-e535e79cbac6] received
[2023-03-22 05:51:11,962: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/00
[2023-03-22 05:51:11,963: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/00
[2023-03-22 05:51:11,963: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:11,963: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:11,963: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/00/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:11,963: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/00'...
[2023-03-22 05:51:12,321: INFO] Execution returned status OK.
[2023-03-22 05:51:12,321: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/00' finished successfully.
[2023-03-22 05:51:12,324: INFO] Task merlin.common.tasks.merlin_step[4792709d-f792-44f9-a423-e535e79cbac6] succeeded in 0.36166557495016605s: ReturnCode.OK
[2023-03-22 05:51:12,325: INFO] Task merlin.common.tasks.merlin_step[2f64215f-6264-4f86-becb-0b7dfc94cb04] received
[2023-03-22 05:51:12,326: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/01
[2023-03-22 05:51:12,326: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/01
[2023-03-22 05:51:12,326: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:12,326: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:12,327: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/01/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:12,327: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/01'...
[2023-03-22 05:51:12,490: INFO] Execution returned status OK.
[2023-03-22 05:51:12,490: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/01' finished successfully.
[2023-03-22 05:51:12,492: INFO] Task merlin.common.tasks.merlin_step[2f64215f-6264-4f86-becb-0b7dfc94cb04] succeeded in 0.16563368804054335s: ReturnCode.OK
[2023-03-22 05:51:12,493: INFO] Task merlin.common.tasks.merlin_step[6f264ba0-a21a-4bc1-a06e-163e6d1315d4] received
[2023-03-22 05:51:12,494: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/02
[2023-03-22 05:51:12,494: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/02
[2023-03-22 05:51:12,494: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:12,494: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:12,494: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/02/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:12,494: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/02'...
[2023-03-22 05:51:12,660: INFO] Execution returned status OK.
[2023-03-22 05:51:12,660: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/02' finished successfully.
[2023-03-22 05:51:12,662: INFO] Task merlin.common.tasks.merlin_step[6f264ba0-a21a-4bc1-a06e-163e6d1315d4] succeeded in 0.16836108401184902s: ReturnCode.OK
[2023-03-22 05:51:12,663: INFO] Task merlin.common.tasks.merlin_step[9dbf7dce-00af-401e-9349-7f338c4cf139] received
[2023-03-22 05:51:12,664: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/03
[2023-03-22 05:51:12,664: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/03
[2023-03-22 05:51:12,665: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:12,665: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:12,665: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/03/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:12,665: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/03'...
[2023-03-22 05:51:12,853: INFO] Execution returned status OK.
[2023-03-22 05:51:12,853: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/03' finished successfully.
[2023-03-22 05:51:12,859: INFO] Task merlin.common.tasks.merlin_step[9dbf7dce-00af-401e-9349-7f338c4cf139] succeeded in 0.19443597499048337s: ReturnCode.OK
[2023-03-22 05:51:12,862: INFO] Task merlin.common.tasks.merlin_step[29652b1f-2a46-431b-aeea-8e22afe27203] received
[2023-03-22 05:51:12,865: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/04
[2023-03-22 05:51:12,866: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/04
[2023-03-22 05:51:12,866: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:12,866: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:12,866: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/04/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:12,866: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/04'...
[2023-03-22 05:51:13,053: INFO] Execution returned status OK.
[2023-03-22 05:51:13,053: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/04' finished successfully.
[2023-03-22 05:51:13,054: INFO] Task merlin.common.tasks.merlin_step[29652b1f-2a46-431b-aeea-8e22afe27203] succeeded in 0.1896344079868868s: ReturnCode.OK
[2023-03-22 05:51:13,056: INFO] Task merlin.common.tasks.merlin_step[54ee43e7-cb13-4482-bdd4-2786a9023ce1] received
[2023-03-22 05:51:13,057: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/05
[2023-03-22 05:51:13,057: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/05
[2023-03-22 05:51:13,057: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:13,057: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:13,057: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/05/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:13,057: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/05'...
[2023-03-22 05:51:13,210: INFO] Execution returned status OK.
[2023-03-22 05:51:13,211: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/05' finished successfully.
[2023-03-22 05:51:13,212: INFO] Task merlin.common.tasks.merlin_step[54ee43e7-cb13-4482-bdd4-2786a9023ce1] succeeded in 0.15559175796806812s: ReturnCode.OK
[2023-03-22 05:51:13,214: INFO] Task merlin.common.tasks.merlin_step[fd7efcbe-bbdb-4fb8-96d6-196afedb30c7] received
[2023-03-22 05:51:13,214: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/06
[2023-03-22 05:51:13,215: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/06
[2023-03-22 05:51:13,215: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:13,215: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:13,215: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/06/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:13,215: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/06'...
[2023-03-22 05:51:13,380: INFO] Execution returned status OK.
[2023-03-22 05:51:13,381: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/06' finished successfully.
[2023-03-22 05:51:13,382: INFO] Task merlin.common.tasks.merlin_step[fd7efcbe-bbdb-4fb8-96d6-196afedb30c7] succeeded in 0.16786708805011585s: ReturnCode.OK
[2023-03-22 05:51:13,384: INFO] Task merlin.common.tasks.merlin_step[f3e1ab38-8196-4f5f-bd35-7967d185a072] received
[2023-03-22 05:51:13,385: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/07
[2023-03-22 05:51:13,385: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/07
[2023-03-22 05:51:13,385: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:13,385: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:13,385: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/07/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:13,385: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/07'...
[2023-03-22 05:51:13,547: INFO] Execution returned status OK.
[2023-03-22 05:51:13,548: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/07' finished successfully.
[2023-03-22 05:51:13,555: INFO] Task merlin.common.tasks.merlin_step[f3e1ab38-8196-4f5f-bd35-7967d185a072] succeeded in 0.1702787569956854s: ReturnCode.OK
[2023-03-22 05:51:13,560: INFO] Task merlin.common.tasks.merlin_step[8ef5cd4e-e355-418e-a7b8-bb0daca352c7] received
[2023-03-22 05:51:13,564: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/08
[2023-03-22 05:51:13,565: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/08
[2023-03-22 05:51:13,565: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:13,565: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:13,567: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/08/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:13,567: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/08'...
[2023-03-22 05:51:13,745: INFO] Execution returned status OK.
[2023-03-22 05:51:13,746: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/08' finished successfully.
[2023-03-22 05:51:13,753: INFO] Task merlin.common.tasks.merlin_step[8ef5cd4e-e355-418e-a7b8-bb0daca352c7] succeeded in 0.1891501930076629s: ReturnCode.OK
[2023-03-22 05:51:13,759: INFO] Task merlin.common.tasks.merlin_step[c45c50b2-307d-41a2-8879-b5430641b7bb] received
[2023-03-22 05:51:13,762: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/runs/09
[2023-03-22 05:51:13,763: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-053246/runs/09
[2023-03-22 05:51:13,763: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:13,763: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:13,764: INFO] Script: /workflow/studies/flux_test_20230322-053246/runs/09/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:13,764: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/09'...
[2023-03-22 05:51:13,939: INFO] Execution returned status OK.
[2023-03-22 05:51:13,939: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-053246/runs/09' finished successfully.
[2023-03-22 05:51:14,007: INFO] Task merlin.common.tasks.merlin_step[c45c50b2-307d-41a2-8879-b5430641b7bb] succeeded in 0.24564087996259332s: ReturnCode.OK
[2023-03-22 05:51:14,009: INFO] Task merlin.common.tasks.add_merlin_expanded_chain_to_chord[394d0a99-2488-4bfa-8a11-ebcc6e0697fe] received
[2023-03-22 05:51:14,114: INFO] Task merlin.common.tasks.add_merlin_expanded_chain_to_chord[394d0a99-2488-4bfa-8a11-ebcc6e0697fe] succeeded in 0.10358296299818903s: ReturnCode.OK
[2023-03-22 05:51:14,116: INFO] Task merlin.common.tasks.merlin_step[2bb02f07-7bc7-427c-9f22-9d93ded92e55] received
[2023-03-22 05:51:14,117: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/00
[2023-03-22 05:51:14,117: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/00
[2023-03-22 05:51:14,117: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:14,117: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:14,117: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/00/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:14,117: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/00'...
[2023-03-22 05:51:14,274: INFO] Execution returned status OK.
[2023-03-22 05:51:14,274: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/00' finished successfully.
[2023-03-22 05:51:14,280: INFO] Task merlin.common.tasks.merlin_step[2bb02f07-7bc7-427c-9f22-9d93ded92e55] succeeded in 0.16346353199332952s: ReturnCode.OK
[2023-03-22 05:51:14,285: INFO] Task merlin.common.tasks.merlin_step[a0219885-67d8-4941-bef3-4da047e49ef9] received
[2023-03-22 05:51:14,288: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/01
[2023-03-22 05:51:14,288: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/01
[2023-03-22 05:51:14,289: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:14,289: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:14,290: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/01/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:14,290: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/01'...
[2023-03-22 05:51:14,493: INFO] Execution returned status OK.
[2023-03-22 05:51:14,493: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/01' finished successfully.
[2023-03-22 05:51:14,500: INFO] Task merlin.common.tasks.merlin_step[a0219885-67d8-4941-bef3-4da047e49ef9] succeeded in 0.213047060999088s: ReturnCode.OK
[2023-03-22 05:51:14,506: INFO] Task merlin.common.tasks.merlin_step[294bd503-78b4-4f34-877c-3aaeb3c6cd93] received
[2023-03-22 05:51:14,510: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/02
[2023-03-22 05:51:14,510: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/02
[2023-03-22 05:51:14,511: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:14,511: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:14,511: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/02/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:14,512: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/02'...
[2023-03-22 05:51:14,737: INFO] Execution returned status OK.
[2023-03-22 05:51:14,737: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/02' finished successfully.
[2023-03-22 05:51:14,739: INFO] Task merlin.common.tasks.merlin_step[294bd503-78b4-4f34-877c-3aaeb3c6cd93] succeeded in 0.22986012801993638s: ReturnCode.OK
[2023-03-22 05:51:14,740: INFO] Task merlin.common.tasks.merlin_step[4c5660d3-332a-4837-8992-88bc32407c36] received
[2023-03-22 05:51:14,741: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/03
[2023-03-22 05:51:14,741: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/03
[2023-03-22 05:51:14,741: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:14,741: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:14,741: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/03/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:14,741: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/03'...
[2023-03-22 05:51:14,913: INFO] Execution returned status OK.
[2023-03-22 05:51:14,913: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/03' finished successfully.
[2023-03-22 05:51:14,921: INFO] Task merlin.common.tasks.merlin_step[4c5660d3-332a-4837-8992-88bc32407c36] succeeded in 0.18002809304744005s: ReturnCode.OK
[2023-03-22 05:51:14,925: INFO] Task merlin.common.tasks.merlin_step[1210027f-ab04-4e92-b842-6f0da673e789] received
[2023-03-22 05:51:14,927: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/04
[2023-03-22 05:51:14,927: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/04
[2023-03-22 05:51:14,927: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:14,927: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:14,928: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/04/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:14,928: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/04'...
[2023-03-22 05:51:15,091: INFO] Execution returned status OK.
[2023-03-22 05:51:15,092: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/04' finished successfully.
[2023-03-22 05:51:15,093: INFO] Task merlin.common.tasks.merlin_step[1210027f-ab04-4e92-b842-6f0da673e789] succeeded in 0.16660284798126668s: ReturnCode.OK
[2023-03-22 05:51:15,095: INFO] Task merlin.common.tasks.merlin_step[60a5057b-a14e-4f32-8a0c-a1ad27ee07eb] received
[2023-03-22 05:51:15,096: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/05
[2023-03-22 05:51:15,096: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/05
[2023-03-22 05:51:15,096: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:15,096: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:15,096: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/05/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:15,096: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/05'...
[2023-03-22 05:51:15,253: INFO] Execution returned status OK.
[2023-03-22 05:51:15,253: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/05' finished successfully.
[2023-03-22 05:51:15,255: INFO] Task merlin.common.tasks.merlin_step[60a5057b-a14e-4f32-8a0c-a1ad27ee07eb] succeeded in 0.15964628802612424s: ReturnCode.OK
[2023-03-22 05:51:15,256: INFO] Task merlin.common.tasks.merlin_step[52e02a38-3c74-4df4-bd46-23d53a336ee0] received
[2023-03-22 05:51:15,257: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/06
[2023-03-22 05:51:15,257: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/06
[2023-03-22 05:51:15,257: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:15,257: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:15,258: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/06/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:15,258: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/06'...
[2023-03-22 05:51:15,451: INFO] Execution returned status OK.
[2023-03-22 05:51:15,451: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/06' finished successfully.
[2023-03-22 05:51:15,453: INFO] Task merlin.common.tasks.merlin_step[52e02a38-3c74-4df4-bd46-23d53a336ee0] succeeded in 0.19548914197366685s: ReturnCode.OK
[2023-03-22 05:51:15,454: INFO] Task merlin.common.tasks.merlin_step[38df79b1-2963-4fd6-b3d1-29257aa1038d] received
[2023-03-22 05:51:15,455: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/07
[2023-03-22 05:51:15,455: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/07
[2023-03-22 05:51:15,455: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:15,455: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:15,456: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/07/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:15,456: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/07'...
[2023-03-22 05:51:15,629: INFO] Execution returned status OK.
[2023-03-22 05:51:15,629: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/07' finished successfully.
[2023-03-22 05:51:15,631: INFO] Task merlin.common.tasks.merlin_step[38df79b1-2963-4fd6-b3d1-29257aa1038d] succeeded in 0.17561967996880412s: ReturnCode.OK
[2023-03-22 05:51:15,632: INFO] Task merlin.common.tasks.merlin_step[8e3d21bb-5932-4ddf-9aa2-03f94cb5933d] received
[2023-03-22 05:51:15,633: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/08
[2023-03-22 05:51:15,633: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/08
[2023-03-22 05:51:15,633: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:15,633: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:15,633: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/08/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:15,633: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/08'...
[2023-03-22 05:51:15,819: INFO] Execution returned status OK.
[2023-03-22 05:51:15,819: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/08' finished successfully.
[2023-03-22 05:51:15,821: INFO] Task merlin.common.tasks.merlin_step[8e3d21bb-5932-4ddf-9aa2-03f94cb5933d] succeeded in 0.18843841599300504s: ReturnCode.OK
[2023-03-22 05:51:15,823: INFO] Task merlin.common.tasks.merlin_step[76abe8a8-50b2-4819-97a2-c35179c9faef] received
[2023-03-22 05:51:15,824: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/runs/09
[2023-03-22 05:51:15,825: INFO] Generating script for runs into /workflow/studies/flux_test_20230322-055101/runs/09
[2023-03-22 05:51:15,825: WARNING] 'shell' is not supported -- ommitted.
[2023-03-22 05:51:15,825: INFO] Scheduling workflow step 'runs'.
[2023-03-22 05:51:15,825: INFO] Script: /workflow/studies/flux_test_20230322-055101/runs/09/runs.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:15,825: INFO] Executing step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/09'...
[2023-03-22 05:51:15,988: INFO] Execution returned status OK.
[2023-03-22 05:51:15,988: INFO] Step 'runs' in '/workflow/studies/flux_test_20230322-055101/runs/09' finished successfully.
[2023-03-22 05:51:16,004: INFO] Task merlin.common.tasks.merlin_step[76abe8a8-50b2-4819-97a2-c35179c9faef] succeeded in 0.17956527002388611s: ReturnCode.OK
[2023-03-22 05:51:16,005: INFO] Task merlin:chordfinisher[4a456e6a-f72e-4aff-b26c-1f80cfee9158] received
[2023-03-22 05:51:16,019: INFO] Task merlin:chordfinisher[4a456e6a-f72e-4aff-b26c-1f80cfee9158] succeeded in 0.01287389500066638s: 'SYNC'
[2023-03-22 05:51:16,020: INFO] Task merlin:chordfinisher[db743f54-ba96-49a1-a42b-55eac74b85cb] received
[2023-03-22 05:51:16,034: INFO] Task merlin:chordfinisher[db743f54-ba96-49a1-a42b-55eac74b85cb] succeeded in 0.01272493600845337s: 'SYNC'
[2023-03-22 05:51:16,035: INFO] Task merlin.common.tasks.expand_tasks_with_samples[bb09bebc-ee54-4de2-ba53-e8bde0f9fae4] received
[2023-03-22 05:51:16,051: INFO] Task merlin.common.tasks.expand_tasks_with_samples[bb09bebc-ee54-4de2-ba53-e8bde0f9fae4] succeeded in 0.014096813974902034s: None
[2023-03-22 05:51:16,052: INFO] Task merlin.common.tasks.merlin_step[c8c6ce50-9d71-4fdd-b1a2-eeb2df7e9053] received
[2023-03-22 05:51:16,052: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-053246/data
[2023-03-22 05:51:16,052: INFO] Generating script for data into /workflow/studies/flux_test_20230322-053246/data
[2023-03-22 05:51:16,053: INFO] Running workflow step 'data' locally.
[2023-03-22 05:51:16,053: INFO] Script: /workflow/studies/flux_test_20230322-053246/data/data.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:16,053: INFO] Executing step 'data' in '/workflow/studies/flux_test_20230322-053246/data'...
[2023-03-22 05:51:16,152: WARNING] Unrecognized Merlin Return code: 1, returning SOFT_FAIL
[2023-03-22 05:51:16,152: WARNING] *** Step 'data' in '/workflow/studies/flux_test_20230322-053246/data' soft failed. Continuing with workflow.
[2023-03-22 05:51:16,164: INFO] Task merlin.common.tasks.merlin_step[c8c6ce50-9d71-4fdd-b1a2-eeb2df7e9053] succeeded in 0.11185956600820646s: ReturnCode.SOFT_FAIL
[2023-03-22 05:51:16,165: INFO] Task merlin.common.tasks.expand_tasks_with_samples[cb814056-3450-4b30-870e-e3ea48802e5e] received
[2023-03-22 05:51:16,179: INFO] Task merlin.common.tasks.expand_tasks_with_samples[cb814056-3450-4b30-870e-e3ea48802e5e] succeeded in 0.012469756009522825s: None
[2023-03-22 05:51:16,180: INFO] Task merlin.common.tasks.merlin_step[d72b719e-e335-4350-a845-30a90b8a4a70] received
[2023-03-22 05:51:16,181: INFO] Directory does not exist. Creating directories to /workflow/studies/flux_test_20230322-055101/data
[2023-03-22 05:51:16,181: INFO] Generating script for data into /workflow/studies/flux_test_20230322-055101/data
[2023-03-22 05:51:16,181: INFO] Running workflow step 'data' locally.
[2023-03-22 05:51:16,181: INFO] Script: /workflow/studies/flux_test_20230322-055101/data/data.slurm.sh
Restart: None
Scheduled?: True
[2023-03-22 05:51:16,181: INFO] Executing step 'data' in '/workflow/studies/flux_test_20230322-055101/data'...
[2023-03-22 05:51:16,268: WARNING] Unrecognized Merlin Return code: 1, returning SOFT_FAIL
[2023-03-22 05:51:16,268: WARNING] *** Step 'data' in '/workflow/studies/flux_test_20230322-055101/data' soft failed. Continuing with workflow.
[2023-03-22 05:51:16,281: INFO] Task merlin.common.tasks.merlin_step[d72b719e-e335-4350-a845-30a90b8a4a70] succeeded in 0.10009911801898852s: ReturnCode.SOFT_FAIL
[2023-03-22 05:51:16,282: INFO] Task merlin:chordfinisher[f306c532-1b76-47ab-a672-8daa5b4be4d5] received
[2023-03-22 05:51:16,283: INFO] Task merlin:chordfinisher[f306c532-1b76-47ab-a672-8daa5b4be4d5] succeeded in 0.0008299860055558383s: 'SYNC'
[2023-03-22 05:51:16,284: INFO] Task merlin:chordfinisher[6f0eb3a3-f987-4304-9bab-32af5b2ebf66] received
[2023-03-22 05:51:16,285: INFO] Task merlin:chordfinisher[6f0eb3a3-f987-4304-9bab-32af5b2ebf66] succeeded in 0.0007048519910313189s: 'SYNC'
```

<details>


Given that batch is changed to flux, you should see a job launched with `flux jobs -a`. Note the way this is
currently designed is to create a flux allocation. You can check for output by presence of `MERLIN_FINISHED` files, e.g.,

```bash
$ tree studies/flux_par_20230322-165729/runs/
```
```console
├── 00
│   ├── MERLIN_FINISHED
│   ├── flux_run.out
│   ├── runs.slurm.err
│   ├── runs.slurm.out
│   └── runs.slurm.sh
├── 01
│   ├── MERLIN_FINISHED
│   ├── flux_run.out
│   ├── runs.slurm.err
│   ├── runs.slurm.out
│   └── runs.slurm.sh
├── 02
│   ├── MERLIN_FINISHED
│   ├── flux_run.out
│   ├── runs.slurm.err
│   ├── runs.slurm.out
│   └── runs.slurm.sh
...
├── 07
│   ├── MERLIN_FINISHED
│   ├── flux_run.out
│   ├── runs.slurm.err
│   ├── runs.slurm.out
│   └── runs.slurm.sh
├── 08
│   ├── MERLIN_FINISHED
│   ├── flux_run.out
│   ├── runs.slurm.err
│   ├── runs.slurm.out
│   └── runs.slurm.sh
└── 09
    ├── MERLIN_FINISHED
    ├── flux_run.out
    ├── runs.slurm.err
    ├── runs.slurm.out
    └── runs.slurm.sh
```

And that seems to be it! We will optimally modify this to be a more substantial MPI
job that we can scale.
