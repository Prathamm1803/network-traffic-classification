import hashlib
import os

seen = {}
duplicates = []

for file in os.listdir("."):
    if os.path.isfile(file) and file.startswith("flow_"):

        with open(file, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash in seen:
            duplicates.append((file, seen[file_hash]))
        else:
            seen[file_hash] = file

print(f"Checked {len(seen)} files")

if duplicates:
    print("\nDuplicate contents found:")
    for a, b in duplicates:
        print(f"{a} == {b}")
else:
    print("\nNo duplicate file contents found.")