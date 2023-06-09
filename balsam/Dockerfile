ARG tag=focal
FROM fluxrm/flux-sched:${tag}

ENV DEBIAN_FRONTEND=nonintercative
USER root
RUN apt-get update && apt-get install -y tzdata && \
    python3 -m pip install numpy matplotlib scipy && \
    python3 -m pip install balsam && \
    apt-get clean
