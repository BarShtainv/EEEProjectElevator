#!/usr/bin/env python3
"""Refresh updateable indexes and fields in a DOCX through LibreOffice UNO."""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import uno
from com.sun.star.beans import PropertyValue


def _property(name: str, value: object) -> PropertyValue:
    item = PropertyValue()
    item.Name = name
    item.Value = value
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--port", type=int, default=2002)
    parser.add_argument("--pdf-output", type=Path)
    parser.add_argument("--no-store", action="store_true")
    args = parser.parse_args()

    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    remote_context = None
    for _ in range(40):
        try:
            remote_context = resolver.resolve(
                f"uno:socket,host=localhost,port={args.port};urp;StarOffice.ComponentContext"
            )
            break
        except Exception:
            time.sleep(0.25)
    if remote_context is None:
        raise RuntimeError("could not connect to LibreOffice UNO service")

    desktop = remote_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", remote_context
    )
    url = uno.systemPathToFileUrl(str(args.document.resolve()))
    document = desktop.loadComponentFromURL(
        url,
        "_blank",
        0,
        (_property("Hidden", True), _property("ReadOnly", False)),
    )
    if document is None:
        raise RuntimeError("LibreOffice could not open the document")
    try:
        document.updateLinks()
        document.getTextFields().refresh()
        indexes = document.getDocumentIndexes()
        for index in range(indexes.getCount()):
            indexes.getByIndex(index).update()
        if args.pdf_output:
            output_url = uno.systemPathToFileUrl(str(args.pdf_output.resolve()))
            document.storeToURL(
                output_url,
                (_property("FilterName", "writer_pdf_Export"),),
            )
        if not args.no_store:
            document.store()
    finally:
        document.close(True)


if __name__ == "__main__":
    main()
