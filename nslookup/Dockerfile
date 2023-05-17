ARG tag=focal
FROM fluxrm/flux-sched:${tag}
ENV DEBIAN_FRONTEND=noninteractive

# It's good to be root :)
USER root
WORKDIR /opt/
RUN apt-get update && \
    apt-get install -y dnsutils telnet strace

# Create a home to put the examples in, and
# ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN useradd -ms /bin/bash -u 1234 flux
