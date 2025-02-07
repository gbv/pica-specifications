#!/bin/bash

tail -n +2 tests/pica_path.csv | while IFS=, read -r col1 _ col3 _; do
    picadata -p "$col1" "examples/$col3"
    echo ""
done
