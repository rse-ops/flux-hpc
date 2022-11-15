ARG app
FROM ghcr.io/rse-ops/lammps-mpi:${app}
ARG FLUX_USER="fluxuser"
ARG FLUX_TOKEN="123456"

# docker build --build-arg app="ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0" -t app-test .
# docker run -it -p 5000:5000 app-test

# Potential command and workdir
#    command: lmp -v x 2 -v y 2 -v z 2 -in in.reaxc.hns -nocite
#    workdir: /home/flux/examples/reaxff/HNS

# Install extra bits for restful server
RUN git clone --depth 1 https://github.com/flux-framework/flux-restful-api /flux-restful-api && \
    cd /flux-restful-api && \
    python3 -m pip install -r requirements.txt && \
    chmod +x /home/flux/examples/reaxff/HNS/*.hns
ENV PYTHONPATH=/lib/python3.8/site-packages

# Tokens for development
ENV FLUX_USER=${FLUX_USER}
ENV FLUX_TOKEN=${FLUX_TOKEN}
ENV FLUX_REQUIRE_AUTH="true"

# No token required for development
EXPOSE 5000
WORKDIR /flux-restful-api
ENTRYPOINT ["sudo", "-u", "flux", "flux", "start", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=5000"]
