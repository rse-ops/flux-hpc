#!/bin/bash

# redis user (999) needs to own these
chown -R rabbitmq /cert_rabbitmq/

# Wrap the existing entrypoint (in /usr/local/bin)
exec docker-entrypoint.sh rabbitmq-server $@
