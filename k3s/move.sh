#!/bin/bash

set -ex

for f in ./bin/*; do 
    base=$(basename $f)
    dest=/bin/$base
    if [[ ! -e "${dest}" ]]; then
        echo "Copying $f to ${dest}..."; 
        cp -R $f /bin/
    fi
done
mv dist/artifacts/k3s /usr/bin/k3s
