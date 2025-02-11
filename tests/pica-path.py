import csv
import subprocess
from pathlib import Path
import json

script_dir = Path(__file__).resolve().parent
csv_file = script_dir / "pica-path.csv"
records_dir = script_dir.parent / "examples"
results = []
version_result = subprocess.run(["picadata", "--version"], capture_output=True, text=True, check=True)
version = version_result.stdout.strip()


with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
        
    for row in reader:
            
        path, description, record, *expected = row
        expected_output = "\n".join(expected).strip()
            
        record_path = records_dir / record            
        result = subprocess.run(["picadata", "-p", path, record_path], capture_output=True, text=True, check=True)
        actual_output = result.stdout.strip()
            
        if actual_output == expected_output:
            status = "passed"
        else:
            status = "failed"
        results.append({"name": path, "description": description, "picadata "+version: status})

output_file = script_dir / "path-test.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
