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
rs_version_result = subprocess.run(["pica", "--version"], capture_output=True, text=True, check=True)
rs_version = rs_version_result.stdout.strip()


with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
        
    for row in reader:
            
        path, description, record, *expected = row
        expected_output = "\n".join(expected).strip()
        
        record_dat = record.replace("pp", "dat")
        record_path = records_dir / record      
        record_dat_path =  records_dir / record_dat
        result = subprocess.run(["picadata", "-p", path, record_path], capture_output=True, text=True, check=True)
        actual_output = result.stdout.strip()


        file_path = Path("temp.dat")

        with open(file_path, "w") as f:
            rs_result = subprocess.run(["pica", "filter", "....?", "-k", path, record_dat_path], stdout=f, stderr=subprocess.PIPE, text=True)
        rs_convert = subprocess.run(["picadata", "-t", "plain", "temp.dat"], capture_output=True, text=True)
        file_path.unlink()
        rs_output = rs_convert.stdout.strip()
        rs_message = rs_result.stderr
        if actual_output == expected_output:
            status = "passed"
        else:
            status = "failed"
        
        if rs_output == expected_output:
            rs_status = "passed"
        else:
            rs_status = "failed"


        results.append({"name": path, "description": description, "picadata "+version: status, "pica-rs "+rs_version: rs_status, "message": rs_message})

print(json.dumps(results, indent=2, ensure_ascii=False))