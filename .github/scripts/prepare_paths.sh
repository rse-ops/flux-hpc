#!/bin/bash

set -e
parsed=""
for file in ${changed_files}; do
    filename=$(basename ${file})

    # In this case, we just have one uptodate per recipe!
    if [[ "$filename" == "Dockerfile" ]]; then
        folder=$(dirname ${file})
        ignorefile=${folder}/.uptodate-ignore

        # Ignore these directories
        if [[ ! -f "$ignorefile" ]]; then
            parsed="${parsed} ${folder}"
        fi
    fi
done
echo ${parsed}

# No parsed results will build ALL
if [[ "${parsed}" == "" ]]; then
    parsed="/does/not/exist/pathy"
fi

echo "parsed_files=${parsed}" >> $GITHUB_OUTPUT
