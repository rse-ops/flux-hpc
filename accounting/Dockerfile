ARG tag=latest
FROM ghcr.io/flux-framework/flux-restful-api:${tag}
ENV FLUX_REQUIRE_AUTH="true"

# Install flux accounting
RUN git clone --depth 1 https://github.com/flux-framework/flux-accounting && \
    cd flux-accounting && \
   ./autogen.sh && \
   ./configure --localstatedir=/var/ && \
   make && \
   make check && \
   sudo make install