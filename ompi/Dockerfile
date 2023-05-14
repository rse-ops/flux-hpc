ARG tag=focal
FROM fluxrm/flux-sched:${tag}
ENV DEBIAN_FRONTEND=noninteractive

# Example runs, as user flux
# flux run -n 4 ./hello_c
# flux run -n 4 ./hello_cxx
# flux run -n 4 ./connectivity_c
# flux run -n 4 ./hello_usempi
# flux run -n 4 ./ring_c
# flux run -n 4 ./ring_usempi
# flux run -n 4 ./ring_mpifh

# not sure how to reproduce:
# mpirun -np 2 --mca mpi_spc_attach all --mca mpi_spc_dump_enabled true ./spc_example [num_messages] [message_size]


USER root
WORKDIR /opt/
RUN apt-get update && \
    apt-get install -y gfortran && \
    wget https://docs.it4i.cz/src/ompi/ompi.tar.gz && \
    tar -xzvf ompi.tar.gz && \
    rm ompi/Makefile
WORKDIR /opt/ompi

# We can't build java ones
COPY ./Makefile ./Makefile
RUN make

# Create a home to put the examples in, and
# ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN useradd -ms /bin/bash -u 1234 flux && \
    chown -R 1234 /opt/ompi
    
# Target this example
ENV PATH=/opt/ompi:$PATH
WORKDIR /opt/ompi
