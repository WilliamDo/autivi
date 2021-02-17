#!/bin/bash
ps xao pgid,comm | grep chromedriver | sed -e 's/^[[:space:]]*//' | cut -d " " -f 1 | xargs -n1 -I {} sh -c "kill -- -{}"
