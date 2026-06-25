# Network Traffic to Grayscale Image Conversion

## Overview

This project converts network traffic into grayscale images for use in network traffic classification experiments.

The preprocessing pipeline follows a **manual methodology** for extracting TCP streams from PCAP files using Wireshark, ensuring consistency with the project requirements. The extracted TCP streams are then converted into 28×28 grayscale images using Python.

Only the **C-array to image conversion** is automated. The raw PCAP extraction remains manual to preserve the original extraction methodology.

---

## Project Workflow

```
PCAP File
    │
    ▼
Open in Wireshark
    │
    ▼
Filter TCP packets
(frame.len > 100)
    │
    ▼
Follow TCP Stream
    │
    ▼
Export as C Array
    │
    ▼
Save each stream as a text file
    │
    ▼
Zero bytes 0–11 and 26–33
    │
    ▼
Trim/Pad to exactly 784 bytes
    │
    ▼
Convert to 28×28 grayscale image
    │
    ▼
Scale ×50 using Nearest-Neighbor interpolation
```

---

## Repository Structure

```
.
├── src/
│   ├── image_generator.py
│   ├── validation.py
│   └── ...
│
├── c_arrays/
│   ├── Chat/
│   ├── Email/
│   └── ...
│
├── images/
│   ├── Chat/
│   ├── Email/
│   └── ...
│
├── validation/
│
├── requirements.txt
├── README.md
└── .gitignore
```

The original PCAP dataset is **not included** in this repository and is ignored using `.gitignore`.

---

## Image Generation Methodology

Each processed TCP stream contains exactly **784 bytes** after preprocessing.

These bytes are interpreted directly as unsigned 8-bit grayscale values:

* 1 byte → 1 pixel
* 784 bytes → 28 × 28 image

No additional image processing is performed.

The generated images preserve the original grayscale values of the packet bytes.

---

## Image Scaling

The original 28×28 images are enlarged by a factor of **50×** using **nearest-neighbor interpolation**.

This enlargement is performed **only for visualization**.

Nearest-neighbor interpolation replicates existing pixels without creating new grayscale values, ensuring that the visualized image is an exact scaled representation of the original data.

The following image processing techniques are intentionally **not** used:

* Contrast enhancement
* Histogram equalization
* Brightness adjustment
* Sharpening
* Smoothing
* Normalization
* Interpolating filters (Bilinear, Bicubic, Lanczos)

---

## Validation

The extracted TCP streams were validated by:

* Verifying the expected number of extracted streams
* Ensuring continuous flow numbering
* Detecting duplicate files using MD5 hashing

The image generation script additionally verifies that every processed file contains exactly **784 bytes** before creating an image.

---

## Technologies Used

* Python
* Wireshark
* Pillow (PIL)
* NumPy
* Git
* GitHub

---

## Running the Image Generator

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the converter:

```bash
python image_generator.py \
    --input c_arrays/Chat \
    --output images/Chat
```

Optional:

```bash
--scale 50
```

---

## Notes

* Raw PCAP files are intentionally excluded from the repository.
* This project automates only the C-array to image conversion stage.
* TCP stream extraction is performed manually in Wireshark to preserve the original project methodology.

---

## Future Improvements

* Byte-level validation tools
* Additional preprocessing verification
* Automated methodology comparison against Wireshark exports
* Network traffic classification using the generated image dataset
