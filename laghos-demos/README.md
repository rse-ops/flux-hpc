# Laghos Demos

Build the container:

```bash
$ docker build -t demo .
```

Shell in!

```bash
$ docker run -it demo bash
```

Then go to the Laghos install location, run the tests, and then try in flux!

```bash
$ flux start --test-size=4
$ cd /workflow/Laghos 
$ flux run make tests
```

We will hopefully be testing this in the Flux Operator next.
