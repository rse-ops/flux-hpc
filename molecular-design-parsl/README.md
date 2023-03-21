# Molecular Design with Parsl + Flux

This example workflow will walk you through running the 
the [EXAWorks Molecular Design Demo](https://github.com/ExaWorks/molecular-design-parsl-demo)
using Parsl and Flux. We have adopted the scripts to be command line interfaces instead
of notebooks. First, build the container:

```bash
$ docker build -t mdparsl .
```

And shell inside:

```bash
$ docker run -it --rm --name mdparsl mdparsl
```

You'll need to be inside a Flux instance:

```bash
$ flux start --test-size=4
```

And activate the conda environment. Note that flux is actually installed alongside mamba!

```bash
$ conda activate /opt/conda/envs/moldesign-demo/
```

## 0. Molecular Design

And then check out the usage of the script:
```bash
python3 ./scripts/0_molecular-design-with-parsl.py --help
```
```console
usage: 0_molecular-design-with-parsl.py [-h] [--workers WORKERS] [--outdir OUTDIR] [--working-dir WORKING_DIR] [--search-space SEARCH_SPACE]
                                        [--initial-count INITIAL_COUNT] [--search-count SEARCH_COUNT] [--batch-size BATCH_SIZE]
                                        [--flux-workers FLUX_WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --workers WORKERS     Number of workers (defaults to cpu count)
  --outdir OUTDIR       Output directory (defaults PWD if not defined)
  --working-dir WORKING_DIR
                        Working directory for Flux (defaults to PWD)
  --search-space SEARCH_SPACE
                        search space of molecules (selected randomly from the QM9 database)
  --initial-count INITIAL_COUNT
                        Number of calculations to run at first
  --search-count SEARCH_COUNT
                        Number of molecules to evaluate in total
  --batch-size BATCH_SIZE
                        Number of molecules to evaluate in each batch of simulations
  --flux-workers FLUX_WORKERS
                        Number of flux node available to run
```

For now you can use the defaults:

```bash
$ python3 ./scripts/0_molecular-design-with-parsl.py
```

Then to copy over data from your host:

```bash
$ mkdir -p ./data && cd ./data
$ docker cp mdparsl:/workflow/training-data-vs-time.svg .
$ docker cp mdparsl:/workflow/parsl-results.csv .
```

Check out the results of this run under [data](data):


<img src="./data/training-data-vs-time.svg">

And this is created from `parsl-results.csv`.
Before you exit the container, notice in the working directory there are a ton of output pickle and text files,
and a "runinfo" directory. There might be more data here you are interested in. You can also look at the various
shell scripts created to run jobs, e.g.,

<details>

<summary>cat parsl.localprovider.1678976440.9403515.sh</summary>

```bash
export JOBNAME=$parsl.localprovider.1678976440.9403515
set -e
export CORES=$(getconf _NPROCESSORS_ONLN)
[[ "1" == "1" ]] && echo "Found cores : $CORES"
WORKERCOUNT=1
FAILONANY=0
PIDS=""

CMD() {
/usr/bin/flux start /opt/conda/envs/moldesign-demo/bin/python3 /opt/conda/envs/moldesign-demo/lib/python3.9/site-packages/parsl/executors/flux/flux_instance_manager.py tcp e25b3d4a9787 45085
}
for COUNT in $(seq 1 1 $WORKERCOUNT); do
    [[ "1" == "1" ]] && echo "Launching worker: $COUNT"
    CMD $COUNT &
    PIDS="$PIDS $!"
done

ALLFAILED=1
ANYFAILED=0
for PID in $PIDS ; do
    wait $PID
    if [ "$?" != "0" ]; then
        ANYFAILED=1
    else
        ALLFAILED=0
    fi
done

[[ "1" == "1" ]] && echo "All workers done"
if [ "$FAILONANY" == "1" ]; then
    exit $ANYFAILED
else
    exit $ALLFAILED
fi
(moldesign-demo) root@e25b3d4a9787:/workflow# cat parsl.localprovider.1678976440.9403515.sh

export JOBNAME=$parsl.localprovider.1678976440.9403515
set -e
export CORES=$(getconf _NPROCESSORS_ONLN)
[[ "1" == "1" ]] && echo "Found cores : $CORES"
WORKERCOUNT=1
FAILONANY=0
PIDS=""

CMD() {
/usr/bin/flux start /opt/conda/envs/moldesign-demo/bin/python3 /opt/conda/envs/moldesign-demo/lib/python3.9/site-packages/parsl/executors/flux/flux_instance_manager.py tcp e25b3d4a9787 45085
}
for COUNT in $(seq 1 1 $WORKERCOUNT); do
    [[ "1" == "1" ]] && echo "Launching worker: $COUNT"
    CMD $COUNT &
    PIDS="$PIDS $!"
done

ALLFAILED=1
ANYFAILED=0
for PID in $PIDS ; do
    wait $PID
    if [ "$?" != "0" ]; then
        ANYFAILED=1
    else
        ALLFAILED=0
    fi
done

[[ "1" == "1" ]] && echo "All workers done"
if [ "$FAILONANY" == "1" ]; then
    exit $ANYFAILED
else
    exit $ALLFAILED
fi
```

</details>

## 1. Interleaving simulation

This step is really cool because it attempts to parallelize tasks, and it requires a redis database!
For our testing here, we will install (and run redis) inside the same container. For our
Flux Operator attempt, we will run it as a sidecar service. For this reason, we will
add redis to the container manually:

```bash
$ docker run -it --rm --name mdparsl mdparsl
```

As follows:

```bash
$ apt-get update && apt-get install -y redis
```

Note there is a `redis.conf` in the working directory.
And then start running it:

```bash
$ redis-server redis.conf
```

You can shell into the container from another terminal (since redis takes the terminal)
Then check out the script to run:

```bash
$ docker exec -it mdparsl bash
$ flux start --test-size=4
$ conda activate /opt/conda/envs/moldesign-demo/
```

Stopped here - this is hanging.

```bash
$ python scripts/1_interleaving-simulation-and-steering.py
```

## 2. Contrast Performance

TBA
