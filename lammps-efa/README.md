# Flux Lammps (with efa) Example

This is an example container where you can build (optional) and run:

```bash
$ docker build --no-cache --build-arg ubuntu_version=20.04 -t test .
```

Then to submit:

```bash
$ docker run -it --entrypoint bash test
$ source /opt/spack-environment/spack/share/spack/setup-env.sh
$ cd /opt/spack-environment
$ spack env activate .
$ cd /home/flux/examples/reaxff/HNS
```
```bash
# Potential entrypoint:
#    sudo -u flux mpirun -x PATH -np 2 --map-by socket lmp -v x 2 -v y 2 -v z 2 -in in.reaxc.hns -nocite
# To run with flux
#    flux start --test-size=4 
#    flux mini submit -ompi=openmpi@5 lmp -v x 2 -v y 2 -v z 2 -in in.reaxc.hns -nocite
#    flux job attach <outid>
```

Note that for networking efa you'd need:

```bash
$ sudo -u flux mpirun -x PATH -x FI_EFA_USE_DEVICE_RDMA -x RDMAV_FORK_SAFE -np 2 --map-by socket lmp -v x 2 -v y 2 -v z 2 -in in.reaxc.hns -nocite
```

The variables should be set in the environment already to 1.
