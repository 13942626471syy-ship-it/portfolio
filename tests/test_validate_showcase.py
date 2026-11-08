"""Regression cases for broken links and unintended public files."""

import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import unittest
import uuid

SPEC = importlib.util.spec_from_file_location(
    "validate_showcase", Path(__file__).parents[1] / "scripts/validate_showcase.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUB"
    "AScY42YAAAAASUVORK5CYII="
)


class ShowcaseValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp_base = (Path(__file__).parents[1] / ".test-tmp").resolve()
        self.root = self.temp_base / uuid.uuid4().hex
        self.root.mkdir(parents=True)
        self.addCleanup(self.cleanup)

    def cleanup(self):
        # Only remove this test's verified isolated directory.
        if self.root.resolve().parent != self.temp_base:
            raise ValueError("test directory escaped its temporary root")
        shutil.rmtree(self.root)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def media(self):
        path = self.root / "assets/demo.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(PNG)
        self.write("assets/manifest.json", json.dumps([{
            "file": "assets/demo.png", "width": 1, "height": 1,
            "sha256": hashlib.sha256(PNG).hexdigest(),
        }]))

    def test_unicode_heading_encoded_path_and_duplicate_heading(self):
        self.write("docs/技术 案例.md", "# 技术案例\n## 实现与取舍\n## 实现与取舍\n")
        self.write("README.md", "[案例](docs/技术%20案例.md#实现与取舍-1)\n")
        self.assertEqual(validator.check_links(self.root, ["README.md"]), [])

    def test_missing_nested_image_and_bad_fragment_are_rejected(self):
        self.write("README.md", "# 首页\n[![示例](assets/missing.png)](#不存在)\n")
        errors = validator.check_links(self.root, ["README.md"])
        self.assertEqual(len(errors), 2)

    def test_code_examples_are_not_followed_as_links(self):
        self.write("README.md", "# 首页\n```md\n[示例](missing.md)\n```\n`[示例](also-missing.md)`\n")
        self.assertEqual(validator.check_links(self.root, ["README.md"]), [])

    def test_links_cannot_escape_repository_or_run_javascript(self):
        self.write("README.md", "[越界](../private.md)\n[错误](javascript:alert)\n")
        self.assertEqual(len(validator.check_links(self.root, ["README.md"])), 2)

    def test_valid_manifest_is_accepted(self):
        self.media()
        self.assertEqual(validator.check_media(self.root), [])

    def test_changed_image_is_rejected(self):
        self.media()
        (self.root / "assets/demo.png").write_bytes(PNG + b"changed")
        self.assertTrue(validator.check_media(self.root))

    def test_unlisted_image_is_rejected(self):
        self.media()
        (self.root / "assets/unreviewed.png").write_bytes(PNG)
        self.assertTrue(validator.check_media(self.root))

    def test_manifest_dimension_mismatch_is_rejected(self):
        self.media()
        path = self.root / "assets/manifest.json"
        entries = json.loads(path.read_text(encoding="utf-8"))
        entries[0]["width"] = 99
        path.write_text(json.dumps(entries), encoding="utf-8")
        self.assertTrue(validator.check_media(self.root))

    def test_reference_and_html_links_are_checked(self):
        self.write("README.md", '[案例][ref]\n[ref]: missing.md\n<img src="missing.png" alt="示例">\n')
        self.assertEqual(len(validator.check_links(self.root, ["README.md"])), 2)

    def test_runtime_files_are_rejected_but_docs_are_allowed(self):
        paths = ["README.md", "docs/deployment.md", ".env", "data/demo.sqlite", "video.mp4"]
        for path in paths:
            self.write(path, "example")
        self.assertEqual(len(validator.check_inventory(self.root, paths)), 3)

    def test_recognizable_credential_is_rejected(self):
        self.write("README.md", "example: " + "ghp_" + "a" * 36)
        self.assertTrue(validator.check_inventory(self.root, ["README.md"]))


if __name__ == "__main__":
    unittest.main()
