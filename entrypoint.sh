#!/usr/bin/env bash

set -e
set -E
set -u

for font in /app/fonts/*.mcm; do
	bin="${font/#mcm/bin}"
	echo "Converting ${font} -> ${bin}"
	python3 /app/mcm2img.py "${font}" "${bin}" RGBA ${RGB:-255 255 255}
done
