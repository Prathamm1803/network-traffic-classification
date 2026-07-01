import re
from pathlib import Path

# ---------------- Configuration ---------------- #

DATA_DIR = Path("data")

# Bytes to anonymize
ZERO_INDICES = list(range(0, 12)) + list(range(26, 34))

TARGET_SIZE = 784
PAD_THRESHOLD = 500

# ------------------------------------------------ #

def process_file(filepath: Path):
    """Preprocess a single C-array file."""

    with open(filepath, "r") as f:
        content = f.read()

    # Ensure the file looks like a C-array
    if "{" not in content:
        print(f"Invalid C-array: {filepath.relative_to(DATA_DIR)}")
        return False

    # Extract all hexadecimal byte values
    hex_values = re.findall(r"0x[0-9A-Fa-f]{2}", content)

    original_length = len(hex_values)

    # Skip packets that are too small
    if original_length < PAD_THRESHOLD:
        print(
            f"Skipped : {filepath.relative_to(DATA_DIR)} "
            f"({original_length} bytes < {PAD_THRESHOLD})"
        )
        return False

    # Zero MAC and IP address bytes
    for idx in ZERO_INDICES:
        if idx < len(hex_values):
            hex_values[idx] = "0x00"

    # Trim or Pad
    if len(hex_values) > TARGET_SIZE:
        hex_values = hex_values[:TARGET_SIZE]

    elif len(hex_values) < TARGET_SIZE:
        hex_values.extend(["0x00"] * (TARGET_SIZE - len(hex_values)))

    # Final sanity check
    assert len(hex_values) == TARGET_SIZE, (
        f"{filepath} has {len(hex_values)} bytes after processing!"
    )

    # Use filename as C-array variable name
    variable_name = filepath.stem

    header = f"char {variable_name}[] = {{\n"

    body = ""

    for i in range(0, TARGET_SIZE, 8):
        body += "  " + ", ".join(hex_values[i:i + 8])

        if i + 8 < TARGET_SIZE:
            body += ","

        body += "\n"

    output = header + body + "};\n"

    # Overwrite original file
    with open(filepath, "w") as f:
        f.write(output)

    print(
        f"Processed : {filepath.relative_to(DATA_DIR)} "
        f"({original_length} -> {TARGET_SIZE} bytes)"
    )

    return True

def main():

    processed = 0
    skipped = 0
    folder = Path("data/Email/email1b")

    for file in folder.iterdir():
        if file.is_file():

            if process_file(file):
                processed += 1
            else:
                skipped += 1

    print("\n========== SUMMARY ==========")
    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped}")
    print(f"Total     : {processed + skipped}")

if __name__ == "__main__":
    main()