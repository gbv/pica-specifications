import csv
import subprocess
from pathlib import Path

script_dir = Path(__file__).resolve().parent
csv_file = script_dir / "pica-path.csv"
records_dir = script_dir.parent / "examples"
    
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
        
    for row in reader:
            
        path, description, record, *expected = row
        expected_output = "\n".join(expected).strip()
            
        print(description)
        record_path = records_dir / record            
        result = subprocess.run(["picadata", "-p", path, record_path], capture_output=True, text=True, check=True)
        actual_output = result.stdout.strip()
            
        if actual_output == expected_output:
            print(f"OK {path}")
        else:
            print("---got:")
            print(actual_output)
            print("---expected:")
            print(expected_output)
        print()
