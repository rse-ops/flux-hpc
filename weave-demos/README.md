# Weave Demos

This is an example container where you can build (optional) and run
the [weave demos](https://github.com/LLNL/weave-demos), specifically
to simualte bouncing a ball.

```bash
$ docker build -t demos .
```

Then shell inside

```bash
$ docker run --entrypoint bash -it demos 
```

## Manual Run (without Flux)

To run the tutorial as is (without Flux) do:

```bash
# The "y" says yes to prompts
$ maestro run ball_bounce_suite.yaml --pgen pgen.py -y
```

Output will appear in "output" and you can dig into the subdirectory to find logs:

```bash
$ cat output/ball-bounce_20230315-035713/logs/ball-bounce.log 
```
```console
...
2023-03-15 03:57:22,708 - maestrowf.datastructures.core.executiongraph:_execute_record:584 - INFO - Attempting submission of 'run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.8d0688.RUN_ID.7.X_POS_INITIAL.45.X_VEL_INITIAL.-2.Y_POS_INITIAL.37.Y_VEL_INITIAL.8.Z_POS_INITIAL.19.Z_VEL_INITIAL.-1' (attempt 1 of 1)...
2023-03-15 03:57:22,775 - maestrowf.interfaces.script.localscriptadapter:submit:151 - INFO - Execution returned status OK.
```
The last line should say it returned OK and shouldn't say FAILED! I found the output directories (length!) a little overwhelming to browse, so I installed and used tree:

```bash
$ apt-get update && apt-get install -y tree
$ tree output/*/run-ball-bounce/
```
```console
└── BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.8d0688.RUN_ID.9.X_POS_INITIAL.45.X_VEL_INITIAL.7.Y_POS_INITIAL.37.Y_VEL_INITIAL.-6.Z_POS_INITIAL.19.Z_VEL_INITIAL.-2
    ├── output.dsv
    ├── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.8d0688.RUN_ID.9.X_POS_INITIAL.45.X_VEL_INITIAL.7.Y_POS_INITIAL.37.Y_VEL_INITIAL.-6.Z_POS_INITIAL.19.Z_VEL_INITIAL.-2.33.err
    ├── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.8d0688.RUN_ID.9.X_POS_INITIAL.45.X_VEL_INITIAL.7.Y_POS_INITIAL.37.Y_VEL_INITIAL.-6.Z_POS_INITIAL.19.Z_VEL_INITIAL.-2.33.out
    └── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.8d0688.RUN_ID.9.X_POS_INITIAL.45.X_VEL_INITIAL.7.Y_POS_INITIAL.37.Y_VEL_INITIAL.-6.Z_POS_INITIAL.19.Z_VEL_INITIAL.-2.sh
```
It looks like each directory has a script, and output, and an error file. I found the output/error to be empty, but the `output.dsv` is some kind of matric of numbers, and the submit script
(the shell script) is just a single line:

```
#!/bin/bash

python /workflow/ball_bounce/./ball_bounce.py output.dsv 45 37 19 -3 3 1 0.5 100 8d0688 2
```

This is probably what they mean when they say running a single simulation. That command runs one simulation. For
fun, I tried this on my own:

```bash
$ mkdir test
$ cd test
$ python /workflow/ball_bounce/./ball_bounce.py output.dsv 45 37 19 -3 3 1 0.5 100 8d0688 2
```

It generated an output.dsv almost immediately. We could likely adjust the simulation parameters for the calculation.

## Quick Start with Flux

We can basically run the workflow to run the simulation, generate a (partial) notebook (note there were bugs with the
final visualization) and then copy it over to view it locally.

```bash
$ docker run --entrypoint bash --rm --name demo -it demos 
$ flux start --test-size=4
$ maestro run ball_bounce_suite_flux.yaml --pgen pgen.py -y
```

**Important** the current notebook has bugs (and is commented out) but if someone can fix them,
we should be able to uncomment the step and copy it over to our local machine as follows:

```bash
$ docker cp demo:/workflow/ball_bounce/render.ipynb ./scripts/render.ipynb
```

If we were doing this with the operator, we would copy this result to a bound volume to save (and maybe some of the simulation data).

## Run with Flux

I then wanted to run with Flux. Start an instance:

```bash
$ flux start --test-size=4
```

And then use the modified yaml to run:

```bash
$ maestro run ball_bounce_suite_flux.yaml --pgen pgen.py -y
```

Check the logs again for OK and we can also see the new run-ball-bounce output directory has scripts for "*flux.sh"

```bash
# tree output/ball-bounce_20230315-040614/run-ball-bounce/
```
```console
output/ball-bounce_20230315-040614/run-ball-bounce/
├── BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.dcb980.RUN_ID.1.X_POS_INITIAL.73.X_VEL_INITIAL.4.Y_POS_INITIAL.48.Y_VEL_INITIAL.-8.Z_POS_INITIAL.11.Z_VEL_INITIAL.-5
│   ├── output.dsv
│   ├── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.dcb980.RUN_ID.1.X_POS_INITIAL.73.X_VEL_INITIAL.4.Y_POS_INITIAL.48.Y_VEL_INITIAL.-8.Z_POS_INITIAL.11.Z_VEL_INITIAL.-5.461.err
│   ├── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.dcb980.RUN_ID.1.X_POS_INITIAL.73.X_VEL_INITIAL.4.Y_POS_INITIAL.48.Y_VEL_INITIAL.-8.Z_POS_INITIAL.11.Z_VEL_INITIAL.-5.461.out
│   └── run-ball-bounce_BOX_SIDE_LENGTH.100.GRAVITY.0.5.GROUP_ID.dcb980.RUN_ID.1.X_POS_INITIAL.73.X_VEL_INITIAL.4.Y_POS_INITIAL.48.Y_VEL_INITIAL.-8.Z_POS_INITIAL.11.Z_VEL_INITIAL.-5.flux.sh
```

The content of each looks like:

```bash
#!/bin/bash
#INFO (nodes) 1
#INFO (walltime) 0
#INFO (flux_uri) local:///tmp/flux-eDXqPs/local-0
#INFO (flux version) 0.26.0

$(LAUNCHER) python /workflow/ball_bounce/./ball_bounce.py output.dsv 73 48 11 1 4 5 0.5 100 dcb980 9
```

I saw [an example for LAUNCHER](https://github.com/LLNL/maestrowf/blob/51056ccfe279495a329036597510d1489dd0c1b1/samples/lulesh/lulesh_sample1_unix_flux.yaml#L19)
and mimicked it to make a variable named launcher that is basically an alias for `flux submit`.

```bash
flux jobs -a
```
```console
       JOBID USER     NAME       ST NTASKS NNODES     TIME INFO
   ƒ54WdmqKm root     python     CD      1      1   0.396s 10864fec333d
   ƒ4bEzL2vs root     python     CD      1      1   0.041s 10864fec333d
   ƒ4aZKRFZh root     python     CD      1      1   0.059s 10864fec333d
   ƒ4ZfCWVxb root     python     CD      1      1   0.045s 10864fec333d
   ƒ4Z5npgdu root     python     CD      1      1   0.061s 10864fec333d
   ƒ4YLYMdpT root     python     CD      1      1   0.059s 10864fec333d
   ƒ4XqCPrJb root     python     CD      1      1   0.045s 10864fec333d
   ƒ4WsqCfuh root     python     CD      1      1   0.055s 10864fec333d
   ƒ4WA9AsHH root     python     CD      1      1   0.061s 10864fec333d
   ƒ4VPLGaGo root     python     CD      1      1   0.060s 10864fec333d
   ƒ4Uis3D9q root     python     CD      1      1   0.067s 10864fec333d
   ƒ4B8u3KCB root     python     CD      1      1   0.078s 10864fec333d
   ƒ41BYo11Z root     python     CD      1      1   0.059s 10864fec333d
```
Note that you'll get callback errors because flux is running as root. We can likely get around this running in the operator.
When everything is done, you'll see an output.sqlite database in the root directory where you ran maestro, and a render.ipynb
in the output path.

A high level note - given that Maestro doesn't stay attached to the job, if we are running via the operator the "run as a command" single-user
mode likely won't work - we would need to run via an interactive job, and determine (on our own) when the workflow is done.
We can likely use the presence of this file.

```bash
# ls
```
```console
01_baseline_simulation   04_manage_data        README.md       ball_bounce_suite.yaml       output         requirements.txt  visualization.ipynb
02_uncertainty_bounds    05_post-process_data  __pycache__     ball_bounce_suite_flux.yaml  output.sqlite  setup.sh
03_simulation_ensembles  06_surrogate_model    ball_bounce.py  dsv_to_sina.py               pgen.py        teardown.sh
```
