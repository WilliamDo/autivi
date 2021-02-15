#!/bin/bash
ps xao pgid,comm | grep chromedriver | cut -d " " -f 2 | xargs -n1 -I {} sh -c "kill -- -{}"
