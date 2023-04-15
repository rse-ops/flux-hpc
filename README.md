# Flux HPC Containers

This is a demo repository of HPC applications that are containerized, with
the intention of being run via Flux. This means we provide a Flux installation
in the container, and you can use with the [Flux Operator](https://github.com/flux-framework/flux-operator).
However, this isn't required - you can use the container to test the HPC app
regardless of Flux!

The builds are done via [this workflow](.github/workflows/build-matrices.yaml)
that uses [uptodate](https://github.com/vsoch/uptodate) on changed files.
Automated builds for each subdirectory is provided, and these examples
are intending to be ported to be run with the Flux Operator.


## Flux Operator
 
You can use these containers as examples of how you should build your flux container
to use with the operator. Generally we recommend using the flux-sched base
so that the install locations are consistent. This assumes that:

 - `/etc/flux` is used for configuration and general setup
 - `/usr/libexec/flux` has executables like flux-imp, flux-shell
 - flux-core / flux-sched with flux-security should be installed.
 - If you haven't created a flux user, one will be created for you (with a common user id 1234)
 - Any executables that the flux user needs for your job should be on the path.
 - The container (for now) should start with user root, and we run commands on behalf of flux.
 - You don't need to install the flux-restful-api (it will be installed by the operator)
  
If you intend to use the [Flux RESTful API](https://github.com/flux-framework/flux-restful-api)
to interact with your cluster, ensure that flux (python bindings) are on the path, along with
either python or python3 (depending on which you used to install Flux).
If/when needed we can lift some of these constraints, but for now they are 
reasonable. Note that we will soon be moving the instructions above to live alongside
the operator, but will keep them here until we do.

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
