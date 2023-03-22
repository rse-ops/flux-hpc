#!/bin/bash

# redis user (999) needs to own these
chown -R redis /cert_redis/

# Wrap the existing entrypoint (in /usr/local/bin)
exec docker-entrypoint.sh redis-server \
  --port 0 \
  --tls-port 6379 \
  --tls-ca-cert-file /cert_redis/ca_certificate.pem \
  --tls-key-file /cert_redis/server_redis_key.pem \
  --tls-cert-file /cert_redis/server_redis_certificate.pem \
  --tls-auth-clients no
