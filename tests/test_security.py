import tempfile
import unittest
from pathlib import Path
from unittest import mock

import codeveil


class SecureFileHandlingTests(unittest.TestCase):
    def test_rejects_oversized_input_before_reading_it(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "large.ps1")
            source.write_bytes(b"x" * 16)
            with mock.patch.object(codeveil, "MAX_INPUT_SIZE", 15):
                with self.assertRaisesRegex(ValueError, "exceeds"):
                    codeveil.read_input_file(source)

    def test_rejects_non_utf8_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "binary.ps1")
            source.write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                codeveil.read_input_file(source)

    def test_atomic_write_does_not_follow_output_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            victim = Path(directory, "victim")
            output = Path(directory, "output")
            victim.write_text("unchanged", encoding="utf-8")
            output.symlink_to(victim)

            codeveil.write_output_file(output, "safe")

            self.assertEqual(victim.read_text(encoding="utf-8"), "unchanged")
            self.assertFalse(output.is_symlink())
            self.assertEqual(output.read_text(encoding="utf-8"), "safe")
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_rejects_same_input_and_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "script.ps1")
            source.write_text("Write-Host test", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must be different"):
                codeveil.main(source, source)


if __name__ == "__main__":
    unittest.main()
