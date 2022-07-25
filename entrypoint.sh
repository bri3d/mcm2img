#!/usr/bin/env bash

set -e
set -E
set -u

for font in $(find /app/fonts -type f -name \*.mcm); do
	bin="${font/.mcm/}"
	echo "Converting ${font} -> ${bin}"
	python3 /app/mcm2img.py "${font}" "${bin}" RGBA ${RGB:-255 255 255}
done
