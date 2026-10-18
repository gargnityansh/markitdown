from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from markitdown import convert_path


class MarkItDownTests(unittest.TestCase):
    def test_converts_text_file_to_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "note.txt"
            file_path.write_text("hello world", encoding="utf-8")

            outputs = convert_path(file_path)

            self.assertEqual(len(outputs), 1)
            markdown_file = Path(tmpdir) / "note.txt.md"
            self.assertEqual(outputs[0], markdown_file)
            content = markdown_file.read_text(encoding="utf-8")
            self.assertIn("# note.txt", content)
            self.assertIn("hello world", content)

    def test_converts_binary_file_to_base64_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.bin"
            file_path.write_bytes(b"\x00\xff\x10")

            outputs = convert_path(file_path)

            self.assertEqual(len(outputs), 1)
            content = outputs[0].read_text(encoding="utf-8")
            self.assertIn("Base64", content)
            self.assertIn("AP8Q", content)

    def test_directory_conversion_skips_markdown_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "already.md").write_text("existing", encoding="utf-8")
            (root / "upload.txt").write_text("file to convert", encoding="utf-8")

            outputs = convert_path(root)

            self.assertEqual([output.name for output in outputs], ["upload.txt.md"])
            self.assertFalse((root / "already.md.md").exists())


if __name__ == "__main__":
    unittest.main()
