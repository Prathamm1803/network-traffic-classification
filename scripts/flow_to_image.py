import re
import os
import numpy as np
from PIL import Image
from pathlib import Path
import argparse


def extract_hex_values(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    hex_values = re.findall(r'0x[0-9A-Fa-f]{2}', content)
    return [int(x, 16) for x in hex_values]


def flow_to_image(input_file, output_file, scale_factor=50):
    data = extract_hex_values(input_file)

    print(f"[{os.path.basename(input_file)}] Found {len(data)} byte values")

    if len(data) != 784:
        print(
            f"Skipping {os.path.basename(input_file)} "
            f"(expected 784 bytes, found {len(data)})"
        )
        return

    arr = np.array(data, dtype=np.uint8)
    img_matrix = arr.reshape((28, 28))

    img = Image.fromarray(img_matrix, mode="L")

    width, height = img.size

    scaled_img = img.resize(
        (width * scale_factor, height * scale_factor),
        Image.Resampling.NEAREST
    )

    scaled_img.save(output_file)

    print(f"Saved: {output_file}")
    print(f"Saved: {scaled_output}")


def process_folder(input_folder, output_folder, scale_factor):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    txt_files = list(input_folder.iterdir())
    print("Files found:")
    for f in txt_files:
        print(f.name)

    print(f"Found {len(txt_files)} txt files")

    for txt_file in txt_files:
        output_file = output_folder / f"{txt_file.stem}.png"

        try:
            flow_to_image(
                str(txt_file),
                str(output_file),
                scale_factor
            )
        except Exception as e:
            print(f"Error processing {txt_file.name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert all flow txt files in a folder to grayscale images"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Folder containing txt files"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Folder to save images"
    )

    parser.add_argument(
        "--scale",
        type=int,
        default=50,
        help="Scale factor"
    )

    args = parser.parse_args()

    process_folder(
        args.input,
        args.output,
        args.scale
    )