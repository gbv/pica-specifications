#!/bin/bash

csv=$(dirname $0)/pica-path.csv
records=$(dirname $0)/../examples

tail -n +2 "$csv" | while IFS=, read -r -a row; do
    path=${row[0]}
    description=${row[1]}
    record=${row[2]}
    expect=$(printf '%s\n' "${row[@]:3}")  # separated by line

    echo "$description"
    got=$(picadata -p "$path" "$records/$record")

    if [ "$got" == "$expect" ]; then
        echo "OK $path"
    else
        echo "---got:"
        echo "$got"
        echo "---expected:"
        echo "$expect"
    fi
    echo
done
