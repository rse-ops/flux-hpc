# Maestro Hello World

Build the container:

```bash
$ docker build -t demo .
```

Shell in!

```bash
$ docker run -it demo bash
```

We have two examples in "study":

```bash
$ ls study/
```
```console
hello-world-multi-flux.yaml  hello-world-multi.yaml
```

## Hello World without Flux

Let's first run the non Flux workflow to get a sense for Maestro. We use maestro run.

```bash
$ maestro run study/hello-world-multi.yaml
```
It will ask you for a y/n to run the study (this can be forced with `-y`)

```console
[2023-03-23 01:22:48: INFO] INFO Logging Level -- Enabled
[2023-03-23 01:22:48: WARNING] WARNING Logging Level -- Enabled
[2023-03-23 01:22:48: CRITICAL] CRITICAL Logging Level -- Enabled
[2023-03-23 01:22:48: INFO] Loading specification -- path = study/hello-world-multi.yaml
[2023-03-23 01:22:48: INFO] Directory does not exist. Creating directories to /workflow/studies/hello_world/hello_world_multiparam_20230323-012248/logs
[2023-03-23 01:22:48: INFO] Adding step 'hello' to study 'hello_world_multiparam'...
[2023-03-23 01:22:48: INFO] 
------------------------------------------
Submission attempts =       1
Submission restart limit =  1
Submission throttle limit = 0
Use temporary directory =   False
Hash workspaces =           False
Dry run enabled =           False
Output path =               /workflow/studies/hello_world/hello_world_multiparam_20230323-012248
------------------------------------------
Would you like to launch the study? [yn] y
Study launched successfully.
```
It won't hang on the submit. You need to explicitly ask for status, and point
that at the study folder, which will be present now in `studies`:

```bash
root@4423908a5bc7:/workflow# maestro status studies/hello_world/hello_world_multiparam_20230323-012248/
                                                  Study: /workflow/studies/hello_world/hello_world_multiparam_20230323-012248                                                   
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Step Name          ┃ Job ID ┃ Workspace         ┃ State    ┃ Run Time       ┃ Elapsed Time   ┃ Start Time         ┃ Submit Time       ┃ End Time           ┃ Number Restarts ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ hello_GREETING.Hel │ 16     │ hello/GREETING.He │ FINISHED │ 0d:00h:00m:01s │ 0d:00h:00m:01s │ 2023-03-23         │ 2023-03-23        │ 2023-03-23         │ 0               │
│ lo.NAME.Pam        │        │ llo.NAME.Pam      │          │                │                │ 01:22:51           │ 01:22:51          │ 01:22:52           │                 │
│ hello_GREETING.Cia │ 17     │ hello/GREETING.Ci │ FINISHED │ 0d:00h:00m:02s │ 0d:00h:00m:02s │ 2023-03-23         │ 2023-03-23        │ 2023-03-23         │ 0               │
│ o.NAME.Jim         │        │ ao.NAME.Jim       │          │                │                │ 01:22:52           │ 01:22:52          │ 01:22:54           │                 │
│ hello_GREETING.Hey │ 18     │ hello/GREETING.He │ FINISHED │ 0d:00h:00m:01s │ 0d:00h:00m:01s │ 2023-03-23         │ 2023-03-23        │ 2023-03-23         │ 0               │
│ .NAME.Michael      │        │ y.NAME.Michael    │          │                │                │ 01:22:54           │ 01:22:54          │ 01:22:55           │                 │
│ hello_GREETING.Hi. │ 19     │ hello/GREETING.Hi │ FINISHED │ 0d:00h:00m:01s │ 0d:00h:00m:01s │ 2023-03-23         │ 2023-03-23        │ 2023-03-23         │ 0               │
│ NAME.Dwight        │        │ .NAME.Dwight      │          │                │                │ 01:22:55           │ 01:22:55          │ 01:22:56           │                 │
└────────────────────┴────────┴───────────────────┴──────────┴────────────────┴────────────────┴────────────────────┴───────────────────┴────────────────────┴─────────────────┘
```

## Hello World with Flux

Now let's run the workflow with Flux! First start a Flux instance.
This targets the broker socket we have defined in our Maestro workflow.

```bash
$ flux start --test-size=4
```

Note that maestro will find the `FLUX_URI` in the environment.
Then run with Flux!

```bash
$ maestro run study/lulesh-flux.yaml -y
```

You can then get the status:

```bash
$ maestro status 
```
```console
# maestro status studies/lulesh/lulesh_sample1_20230323-031150/
                                                   Study: /workflow/studies/lulesh/lulesh_sample1_20230323-031150                                                   
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃                 ┃        ┃                 ┃             ┃                ┃                ┃                 ┃                ┃                 ┃ Number         ┃
┃ Step Name       ┃ Job ID ┃ Workspace       ┃ State       ┃ Run Time       ┃ Elapsed Time   ┃ Start Time      ┃ Submit Time    ┃ End Time        ┃ Restarts       ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ make-lulesh     │ 178    │ make-lulesh     │ FINISHED    │ 0d:00h:00m:03s │ 0d:00h:00m:03s │ 2023-03-23      │ 2023-03-23     │ 2023-03-23      │ 0              │
│                 │        │                 │             │                │                │ 03:12:04        │ 03:12:04       │ 03:12:07        │                │
│ run-lulesh_ITER │ --     │ run-lulesh/ITER │ INITIALIZED │ --:--:--       │ --:--:--       │ --              │ --             │ --              │ 0              │
│ .10.SIZE.100    │        │ .10.SIZE.100    │             │                │                │                 │                │                 │                │
│ run-lulesh_ITER │ --     │ run-lulesh/ITER │ INITIALIZED │ --:--:--       │ --:--:--       │ --              │ --             │ --              │ 0              │
│ .20.SIZE.100    │        │ .20.SIZE.100    │             │                │                │                 │                │                 │                │
│ run-lulesh_ITER │ --     │ run-lulesh/ITER │ INITIALIZED │ --:--:--       │ --:--:--       │ --              │ --             │ --              │ 0              │
│ .30.SIZE.100    │        │ .30.SIZE.100    │             │                │                │                 │                │                 │                │
└─────────────────┴────────┴─────────────────┴─────────────┴────────────────┴────────────────┴─────────────────┴────────────────┴─────────────────┴────────────────┘
```

Note that the jobs take a bit to submit - but you'll see them eventually with `flux jobs -a`:

```bash
root@ff13d7344bcc:/workflow# flux jobs -a
```
```console
       JOBID USER     NAME       ST NTASKS NNODES     TIME INFO
    ƒd6B8zvb root     run-lules+  R      1      1   9.917s ff13d7344bcc
    ƒcY82XYB root     run-lules+  R      1      1   11.16s ff13d7344bcc
    ƒbiroRUb root     run-lules+  R      1      1   13.02s ff13d7344bcc
```

Also note there is an error/warning message when running flux with root - you can ignore for this demo.
When you see it, however, it indicates a flux job was submit!

```console
2023-03-23T03:13:10.411916Z job-manager.err[0]: jobtap: job.new: callback returned error
```

It takes usually (on my machine) about 4-5 minutes per job. Here are the completed jobs.

```bash
root@ff13d7344bcc:/workflow# flux jobs -a
       JOBID USER     NAME       ST NTASKS NNODES     TIME INFO
    ƒd6B8zvb root     run-lules+ CD      1      1   5.207m ff13d7344bcc
    ƒcY82XYB root     run-lules+ CD      1      1   4.974m ff13d7344bcc
    ƒbiroRUb root     run-lules+ CD      1      1   3.556m ff13d7344bcc
```
The command `flux job attach` can normally show you output, but in this case the workflow tool
redirects them to files. You can thus check the files in `lulesh-run`:

```bash
studies/lulesh/lulesh_sample1_20230323-031150/run-lulesh/
├── ITER.10.SIZE.100
│   ├── SIZE.100.ITER.10.log
│   ├── run-lulesh_ITER.10.SIZE.100.flux.sh
│   ├── run-lulesh_ITER.10.SIZE.100.ƒbiroRUb.err
│   └── run-lulesh_ITER.10.SIZE.100.ƒbiroRUb.out
├── ITER.20.SIZE.100
│   ├── SIZE.100.ITER.20.log
│   ├── run-lulesh_ITER.20.SIZE.100.flux.sh
│   ├── run-lulesh_ITER.20.SIZE.100.ƒcY82XYB.err
│   └── run-lulesh_ITER.20.SIZE.100.ƒcY82XYB.out
└── ITER.30.SIZE.100
    ├── SIZE.100.ITER.30.log
    ├── run-lulesh_ITER.30.SIZE.100.flux.sh
    ├── run-lulesh_ITER.30.SIZE.100.ƒd6B8zvb.err
    └── run-lulesh_ITER.30.SIZE.100.ƒd6B8zvb.out
```

Here is an example output (*.log):

```bash
# cat studies/lulesh/lulesh_sample1_20230323-031150/run-lulesh/ITER.30.SIZE.100/SIZE.100.ITER.30.log 
Running problem size 100^3 per domain until completion
Num processors: 1
Num threads: 2
Total number of elements: 1000000 

To run other sizes, use -s <integer>.
To run a fixed number of iterations, use -i <integer>.
To run a more or less balanced region set, use -b <integer>.
To change the relative costs of regions, use -c <integer>.
To print out progress, use -p
To write an output file for VisIt, use -v
See help (-h) for more options

cycle = 1, time = 1.910718e-07, dt=1.910718e-07
cycle = 2, time = 4.203581e-07, dt=2.292862e-07
cycle = 3, time = 4.989486e-07, dt=7.859057e-08
cycle = 4, time = 5.645779e-07, dt=6.562923e-08
cycle = 5, time = 6.230838e-07, dt=5.850593e-08
cycle = 6, time = 6.774092e-07, dt=5.432541e-08
cycle = 7, time = 7.290587e-07, dt=5.164946e-08
cycle = 8, time = 7.789464e-07, dt=4.988778e-08
cycle = 9, time = 8.276916e-07, dt=4.874515e-08
cycle = 10, time = 8.757493e-07, dt=4.805775e-08
cycle = 11, time = 9.334186e-07, dt=5.766930e-08
cycle = 12, time = 9.985303e-07, dt=6.511161e-08
cycle = 13, time = 1.060082e-06, dt=6.155140e-08
cycle = 14, time = 1.118087e-06, dt=5.800581e-08
cycle = 15, time = 1.172544e-06, dt=5.445676e-08
cycle = 16, time = 1.224534e-06, dt=5.198930e-08
cycle = 17, time = 1.274973e-06, dt=5.043991e-08
cycle = 18, time = 1.324652e-06, dt=4.967896e-08
cycle = 19, time = 1.374324e-06, dt=4.967114e-08
cycle = 20, time = 1.423995e-06, dt=4.967114e-08
cycle = 21, time = 1.473666e-06, dt=4.967114e-08
cycle = 22, time = 1.523337e-06, dt=4.967114e-08
cycle = 23, time = 1.573008e-06, dt=4.967114e-08
cycle = 24, time = 1.627986e-06, dt=5.497832e-08
cycle = 25, time = 1.682965e-06, dt=5.497832e-08
cycle = 26, time = 1.737943e-06, dt=5.497832e-08
cycle = 27, time = 1.800609e-06, dt=6.266569e-08
cycle = 28, time = 1.863274e-06, dt=6.266569e-08
cycle = 29, time = 1.938109e-06, dt=7.483443e-08
cycle = 30, time = 2.023029e-06, dt=8.492029e-08
Run completed:
   Problem size        =  100
   MPI tasks           =  1
   Iteration count     =  30
   Final Origin Energy =  1.174431e+08
   Testing Plane 0 of Energy Array on rank 0:
        MaxAbsDiff   = 1.117587e-08
        TotalAbsDiff = 1.260178e-08
        MaxRelDiff   = 1.339561e-10

Elapsed time         =    3.1e+02 (s)
Grind time (us/z/c)  =  10.293708 (per dom)  ( 308.81124 overall)
FOM                  =  97.146722 (z/s)
```

Cool!

Next, let's exit from the flux instance and try running as the fluxuser.
This ideally should work for use in the flux operator.

```bash
# Make sure the fluxuser owns everything!
$ sudo chown -R fluxuser .

$ sudo -u fluxuser -E PATH=$PATH -E PYTHONPATH=$PYTHONPATH -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH flux start --test-size=4
```

It's up to you, but I deleted the entire studies folder to start fresh, and then submit again:

```bash
$ rm -rf ./studies
$ maestro run study/lulesh-flux.yaml -y
$ maestro status ./studies/lulesh/lulesh_sample1_20230323-033808
```

The interaction should be the same as before, meaning it works with the flux user (without the root errors!)
When you are done, exit from the flux instance and container. Yer done!
