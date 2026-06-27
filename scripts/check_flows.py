import os
import re

flows = []

for f in os.listdir("."):
    m = re.match(r"flow_(\d+)_", f)
    if m:
        flows.append(int(m.group(1)))

flows.sort()

print("Found flows:", len(flows))
print("Min:", min(flows))
print("Max:", max(flows))

missing = [
    i for i in range(min(flows), max(flows) + 1)
    if i not in flows
]

if missing:
    print("Missing flow numbers:")
    print(missing)
else:
    print("No missing flow numbers.")