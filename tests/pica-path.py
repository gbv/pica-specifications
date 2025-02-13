import csv
import subprocess
from pathlib import Path
from sys import stderr
import json
import re
import shlex

script_dir = Path(__file__).resolve().parent
csv_file = script_dir / "pica-path.csv"
records_dir = script_dir.parent / "examples"
results = []
version_result = subprocess.run(["picadata", "--version"], capture_output=True, text=True, check=True)
version = version_result.stdout.strip()
rs_version_result = subprocess.run(["pica", "--version"], capture_output=True, text=True, check=True)
rs_version = rs_version_result.stdout.strip().replace("pica","pica-rs")

def exec(cmd):
    print(" ".join(map(shlex.quote,cmd)),file=stderr)
    return subprocess.run(cmd, capture_output=True, text=True)

def dat2pp(dat):
    return dat.replace('$','$$').replace('\x1E','\n').replace('\x1F','$')

def pp2dat(dat): # TODO: use this instead of calling picadata
    return re.sub(r'\$([A-Za-z0-9])',r'\x1F\1',dat.replace('\n','\x1E').replace('$$','$'))

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        path, sf, description, record, *expected = row
        expected = "\n".join(expected).strip()

        record_dat = record.replace("pp", "dat")
        record_path = str(records_dir / record)
        record_dat_path =  records_dir / record_dat
        cmd = ["picadata", "-p", path, record_path + ".pp"]
        result = exec(cmd)
        output = result.stdout.strip()
        status = "passed" if output == expected else "failed"

        record_path = record_path + ".dat"
        if sf == '1':
            cmd = ["pica", "select", path, record_path]
        else:
            cmd = ["pica", "filter", "-k", path, "....?", record_path]
        rs_result = exec(cmd)
        output = dat2pp(rs_result.stdout.strip())
        rs_message = rs_result.stderr
        rs_status = "passed" if output == expected else "failed"

        results.append({"name": path, "description": description, "picadata "+version: status, rs_version: rs_status, "message": rs_message})

print(json.dumps(results, indent=2, ensure_ascii=False))
