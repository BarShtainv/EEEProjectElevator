#!/usr/bin/env python3
"""Create styled report-use PNGs from the protected SP-07 timing SVGs."""

from __future__ import annotations

import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

import cairosvg


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "docs" / "figures"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

ACCEPTED_SOURCES = {
    "sp07_mixed_controller_average_ns": "7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930",
    "sp07_lookup_average_ns": "26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096",
    "sp07_authorization_average_ns": "433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9",
}

STYLE_ATTRIBUTES = {
    "fill",
    "stroke",
    "stroke-width",
    "font-family",
    "font-size",
    "font-weight",
}

NAVY = "#274C77"
BLUE = "#2F6690"
TEAL = "#2F7F7B"
TEXT = "#1F2933"
SECONDARY_TEXT = "#526574"
AXIS = "#405464"
GRID = "#D9E1E7"


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _quantitative_contract(root: ET.Element) -> tuple[tuple[object, ...], ...]:
    """Capture every non-visual attribute and text value before restyling."""
    records: list[tuple[object, ...]] = []
    for element in root.iter():
        attributes = tuple(
            sorted((key, value) for key, value in element.attrib.items() if key not in STYLE_ATTRIBUTES)
        )
        records.append((_local_name(element), attributes, element.text or ""))
    return tuple(records)


def _style_svg(source: bytes) -> bytes:
    ET.register_namespace("", SVG_NAMESPACE)
    root = ET.fromstring(source)
    before = _quantitative_contract(root)
    root.set("font-family", "Liberation Sans, Arial, sans-serif")

    for element in root.iter():
        tag = _local_name(element)
        css_class = element.get("class", "")

        if tag == "rect" and not css_class:
            element.set("fill", "#FFFFFF")
        elif tag == "line" and css_class == "whisker":
            element.set("stroke", AXIS)
            element.set("stroke-width", "2.25")
        elif tag == "line" and element.get("stroke") == "#cccccc":
            element.set("stroke", GRID)
            element.set("stroke-width", "1.2")
        elif tag == "line":
            element.set("stroke", AXIS)
            element.set("stroke-width", "2")
        elif tag == "rect" and css_class == "repetition-point":
            element.set("fill", "#FFFFFF")
            element.set("stroke", TEAL)
            element.set("stroke-width", "2")
        elif tag == "circle" and css_class == "median-point":
            element.set("fill", BLUE)
            element.set("stroke", NAVY)
            element.set("stroke-width", "1.25")
        elif tag == "polyline" and css_class == "median-line":
            element.set("stroke", BLUE)
            element.set("stroke-width", "3")
        elif tag == "text":
            element.set("fill", TEXT)
            y = element.get("y")
            if y == "36":
                element.set("fill", NAVY)
                element.set("font-size", "23")
                element.set("font-weight", "700")
            elif y == "510" or element.get("transform", "").startswith("rotate(-90"):
                element.set("font-size", "16")
                element.set("font-weight", "600")
            elif y in {"535", "558", "578"}:
                element.set("fill", SECONDARY_TEXT)
            else:
                element.set("font-size", "14")

    after = _quantitative_contract(root)
    if after != before:
        raise RuntimeError("restyling changed a quantitative attribute or text value")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def main() -> None:
    for stem, expected_hash in ACCEPTED_SOURCES.items():
        source_path = FIGURES / f"{stem}.svg"
        output_path = FIGURES / f"{stem}.png"
        source = source_path.read_bytes()
        actual_hash = hashlib.sha256(source).hexdigest()
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"protected source hash mismatch for {source_path}: {actual_hash} != {expected_hash}"
            )
        styled = _style_svg(source)
        cairosvg.svg2png(
            bytestring=styled,
            write_to=str(output_path),
            output_width=1920,
            output_height=1200,
            background_color="#FFFFFF",
        )
        print(f"styled {output_path.relative_to(ROOT)} from protected SVG {actual_hash}")


if __name__ == "__main__":
    main()
