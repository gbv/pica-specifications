#!/bin/bash
set -euo pipefail

PICARS=./pica
PICADATA=picadata

cd "$(dirname $0)"

python pica-path.py > path-test.json 
python pica-patch.py > patch-test.json 
