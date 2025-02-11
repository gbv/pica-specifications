import csv
import subprocess
from pathlib import Path
import json

script_dir = Path(__file__).resolve().parent
csv_file = script_dir / "pica-path.csv"
records_dir = script_dir.parent / "examples"
results = []

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
        results.append({"name": path, "description": description, "status": status})
print(json.dumps(results, indent=2))  