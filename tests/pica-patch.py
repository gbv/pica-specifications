from pathlib import Path
import subprocess
import json

script_dir = Path(__file__).resolve().parent
records_dir = script_dir.parent / "examples"
results = []

files = sorted([f.name for f in records_dir.iterdir() if f.is_file() and f.name.endswith("pp")])

file_groups = {}
version_result = subprocess.run(["picadata", "--version"], capture_output=True, text=True, check=True)
version = version_result.stdout.strip()
test_num = 1
for file in files:
    for prefix in ("example", "patch", "result"):
        if file.startswith(prefix):
            core_id = file[len(prefix):-3]
            if core_id not in file_groups:
                file_groups[core_id] = []
            file_groups[core_id].append(file)

for files in file_groups.values():
    message = ""
    example_path = records_dir / files[0]
    patch_path = records_dir / files[1]
    result_path = records_dir / files[2]
    with open(result_path, "r") as result_file:
        expected_output = result_file.read().strip()
    with open(patch_path, "r") as patch_file:
        patch = patch_file.read().strip()
    result = subprocess.run(["picadata", "patch", example_path, patch_path], capture_output=True, text=True, check=True)
    actual_output = result.stdout.strip()
    if actual_output == expected_output:
        status = "passed"
        results.append({"name": test_num, "picadata "+version: status})
    else:
        status = "failed"
        message = result.stderr.strip()
        results.append({"name": test_num, "picadata "+version: status, "message": message})
    test_num += 1

print(json.dumps(results, indent=2, ensure_ascii=False))