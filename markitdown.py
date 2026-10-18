#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
from pathlib import Path


def _markdown_output_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.md")


def convert_file(path: Path) -> Path | None:
    if not path.is_file() or path.suffix.lower() == ".md":
        return None

    output_path = _markdown_output_path(path)

    try:
        text_content = path.read_text(encoding="utf-8")
        body = (
            f"# {path.name}\n\n"
            f"Source file: `{path}`\n\n"
            "```text\n"
            f"{text_content}\n"
            "```\n"
        )
    except UnicodeDecodeError:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        body = (
            f"# {path.name}\n\n"
            f"Source file: `{path}`\n\n"
            "This file was not UTF-8 text, so it is represented as Base64.\n\n"
            "```text\n"
            f"{encoded}\n"
            "```\n"
        )

    output_path.write_text(body, encoding="utf-8")
    return output_path


def convert_path(path: Path) -> list[Path]:
    outputs: list[Path] = []
    if path.is_file():
        converted = convert_file(path)
        if converted:
            outputs.append(converted)
        return outputs

    if path.is_dir():
        for file_path in path.rglob("*"):
            if ".git" in file_path.parts:
                continue
            converted = convert_file(file_path)
            if converted:
                outputs.append(converted)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert uploaded files into Markdown files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to convert",
    )
    args = parser.parse_args()

    converted: list[Path] = []
    for raw_path in args.paths:
        converted.extend(convert_path(Path(raw_path)))

    if not converted:
        print("No files converted.")
        return 0

    print("Converted files:")
    for item in converted:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
