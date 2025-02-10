from pathlib import Path
import subprocess

script_dir = Path(__file__).resolve().parent
records_dir = script_dir.parent / "examples"

files = sorted([f.name for f in records_dir.iterdir() if f.is_file() and f.name.endswith("pp")])

file_groups = {}

for file in files:
    for prefix in ("example", "patch", "result"):
        if file.startswith(prefix):
            core_id = file[len(prefix):-3]
            if core_id not in file_groups:
                file_groups[core_id] = []
            file_groups[core_id].append(file)

for files in file_groups.values():
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
        print(f"OK {patch}")
    else:
        print("---got:")
        print(actual_output)
        print("---expected:")
        print(expected_output)
    print()