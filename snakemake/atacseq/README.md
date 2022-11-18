# Flux Snakemake Example

This is an example container where you can build (optional) and run
the [Snakemake tutorial workflow](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html):

```bash
$ docker build -t snakemake .
```

or with a tag for the restful API:

```bash
$ docker build --no-cache --build-arg app="latest" -t snakemake .
```

## Running the Workflow

### RESTFul API and Interface

To use the Flux RESTFul API and interface:

```
$ docker run -it -p 5000:5000 snakemake
```

Requiring a Flux user/token (fluxuser and 12345)

```bash
$ docker run -it --env require_auth=true -p 5000:5000 snakemake
```

And then enter the fluxuser and 123456 as the user and token, and try submitting a job to
the examples like:

```console
# Potential command and workdir
# command: snakemake --cores 1 --flux 
# workdir: /workflow
```

![img/submit.png](img/submit.png)

And then browse to the table and click on the ID to see the log.

![img/log.png](img/log.png)

You can also try using the [RESTFul API](https://flux-framework.org/flux-restful-api/getting_started/user-guide.html#getting-started-user-guide--page-root). Have fun!

### Manual

Or just shell into the container:

```bash
$ docker run -it --entrypoint bash snakemake
```

Activate the environment:

```bash
$ micromamba shell init --shell=bash --prefix=~/micromamba
$ source /root/.bashrc
$ eval $(micromamba shell hook --shell=bash)
$ micromamba activate snakemake
```

And then start the flux instance:

```bash
$ flux start --test-size=4
```

And go to the snakemake workflow, and run it with Flux!

```bash
$ cd /workflow
$ snakemake --cores 1 --flux
```
That's it! 
