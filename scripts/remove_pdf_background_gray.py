from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, NumberObject


def whiten_background(image: Image.Image, low: float, white_point: float) -> Image.Image:
    """Whiten neutral scan highlights without changing pixel dimensions."""
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    source = np.asarray(image, dtype=np.uint8)
    work = source.astype(np.float32)

    if image.mode == "L":
        value = work
        neutral = np.ones(value.shape, dtype=bool)
    else:
        value = work.mean(axis=2)
        neutral = (work.max(axis=2) - work.min(axis=2)) <= 18.0

    t = np.clip((value - low) / (white_point - low), 0.0, 1.0)
    smooth = t * t * (3.0 - 2.0 * t)
    amount = smooth * neutral

    if image.mode == "L":
        result = work + (255.0 - work) * amount
    else:
        result = work + (255.0 - work) * amount[:, :, None]

    return Image.fromarray(np.rint(result).astype(np.uint8), mode=image.mode)


def make_xobject(image: Image.Image):
    decoded = DecodedStreamObject()
    decoded.set_data(image.tobytes())
    decoded[NameObject("/Type")] = NameObject("/XObject")
    decoded[NameObject("/Subtype")] = NameObject("/Image")
    decoded[NameObject("/Width")] = NumberObject(image.width)
    decoded[NameObject("/Height")] = NumberObject(image.height)
    decoded[NameObject("/ColorSpace")] = NameObject(
        "/DeviceGray" if image.mode == "L" else "/DeviceRGB"
    )
    decoded[NameObject("/BitsPerComponent")] = NumberObject(8)
    return decoded.flate_encode()


def image_dimensions(reader: PdfReader) -> list[tuple[int, int]]:
    return [image.image.size for page in reader.pages for image in page.images]


def process(input_path: Path, output_path: Path, low: float, white_point: float) -> None:
    if not 0 <= low < white_point <= 255:
        raise ValueError("Require 0 <= low < white-point <= 255")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must differ")

    reader = PdfReader(input_path)
    input_boxes = [tuple(page.mediabox) for page in reader.pages]
    input_dimensions = image_dimensions(reader)
    if not input_dimensions:
        raise ValueError("No embedded page images found; this is not an image-based scan PDF")

    writer = PdfWriter(clone_from=reader)
    processed: set[int] = set()

    for page_number, page in enumerate(writer.pages, start=1):
        for image_file in page.images:
            ref = image_file.indirect_reference
            if ref is None:
                raise ValueError(f"Inline image found on page {page_number}; aborting safely")
            if ref.idnum in processed:
                continue

            image_object = ref.get_object()
            if "/SMask" in image_object or "/Mask" in image_object:
                raise ValueError(
                    f"Transparency mask found on page {page_number}; aborting safely"
                )

            cleaned = whiten_background(image_file.image, low, white_point)
            replacement = make_xobject(cleaned)
            replacement.indirect_reference = ref
            writer._objects[ref.idnum - 1] = replacement
            processed.add(ref.idnum)

        if page_number % 20 == 0 or page_number == len(writer.pages):
            print(f"Processed page {page_number}/{len(writer.pages)}", flush=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as stream:
        writer.write(stream)

    output_reader = PdfReader(output_path)
    if len(output_reader.pages) != len(reader.pages):
        raise RuntimeError("Verification failed: page count changed")
    if [tuple(page.mediabox) for page in output_reader.pages] != input_boxes:
        raise RuntimeError("Verification failed: page geometry changed")
    if image_dimensions(output_reader) != input_dimensions:
        raise RuntimeError("Verification failed: image pixel dimensions changed")

    print(f"Updated {len(processed)} unique image objects", flush=True)
    print("Verified page count, page geometry, and image pixel dimensions", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove gray scan backgrounds without resizing PDF images."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--low", type=float, default=230.0)
    parser.add_argument("--white-point", type=float, default=252.0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process(args.input, args.output, args.low, args.white_point)
