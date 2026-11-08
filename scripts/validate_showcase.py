"""Offline checks for the public showcase. No product or network access.

The link syntax supported here is the Markdown/HTML subset used in this repo.
Credential patterns and file rules are guardrails, not a privacy certification.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


ALLOWED_FILES = {
    "README.md", "CHANGELOG.md", ".gitignore", "assets/README.md",
    "assets/manifest.json", "scripts/validate_showcase.py",
    "tests/test_validate_showcase.py", ".github/workflows/showcase.yml",
}
ALLOWED_PATTERNS = (
    re.compile(r"(?:docs|projects)/(?:[a-z0-9-]+/)*[a-z0-9-]+\.md\Z"),
    re.compile(r"assets/[a-z0-9-]+/[a-z0-9-]+\.png\Z"),
)
SECRET_PATTERN = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,}|"
    r"sk-(?:proj-)?[A-Za-z0-9_-]{32,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def without_fences(text):
    output, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "\n".join(output)


def link_targets(text):
    text = re.sub(r"(`+).*?\1", "", without_fences(text))
    # Find destinations, rather than labels, so linked images work too.
    targets = re.findall(r"\]\(\s*(<[^>]+>|[^\s)]+)", text)
    targets += re.findall(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text, re.M)
    targets += re.findall(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", text, re.I)
    return [target.strip("<>") for target in targets]


def heading_anchors(text):
    anchors, duplicates = set(), {}
    for label in re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", without_fences(text), re.M):
        label = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", label)
        label = re.sub(r"<[^>]+>", "", label).lower()
        slug = "".join(
            char for char in label
            if char in " _-" or unicodedata.category(char)[0] in "LNM"
        ).replace(" ", "-")
        ordinal = duplicates.get(slug, 0)
        duplicates[slug] = ordinal + 1
        anchors.add(f"{slug}-{ordinal}" if ordinal else slug)
    anchors.update(re.findall(r"(?:id|name)=[\"']([^\"']+)[\"']", text))
    return anchors


def check_links(root, paths):
    root, errors = Path(root).resolve(), []
    for name in paths:
        source = root / name
        for target in link_targets(source.read_text(encoding="utf-8")):
            try:
                url = urlsplit(target)
                if url.scheme in {"https", "http", "mailto"}:
                    continue  # External availability is checked separately before publishing.
                if url.scheme or url.netloc:
                    errors.append(f"{name}: unsupported link scheme")
                    continue
                path = unquote(url.path)
                destination = (root / path.lstrip("/") if path.startswith("/")
                               else source.parent / path if path else source).resolve()
                if not destination.is_relative_to(root):
                    errors.append(f"{name}: link escapes repository")
                elif not destination.exists():
                    errors.append(f"{name}: missing link target {target}")
                elif url.fragment and destination.suffix == ".md":
                    anchors = heading_anchors(destination.read_text(encoding="utf-8"))
                    if unquote(url.fragment) not in anchors:
                        errors.append(f"{name}: missing heading {target}")
            except (OSError, UnicodeError, ValueError) as error:
                errors.append(f"{name}: unreadable link target ({type(error).__name__})")
    return errors


def check_media(root):
    root, errors, listed = Path(root).resolve(), [], set()
    try:
        entries = json.loads((root / "assets/manifest.json").read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ValueError("manifest must be a list")
        for entry in entries:
            name = entry["file"]
            if not isinstance(name, str) or not re.fullmatch(r"assets/(?:[a-z0-9-]+/)*[a-z0-9-]+\.png", name):
                raise ValueError("invalid media path")
            if name in listed:
                errors.append(f"{name}: duplicate manifest entry")
            listed.add(name)
            path = (root / name).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append(f"{name}: missing or unsafe image")
                continue
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                errors.append(f"{name}: image fingerprint changed; review required")
            if len(data) < 24 or data[:8] != PNG_SIGNATURE or data[12:16] != b"IHDR":
                errors.append(f"{name}: invalid PNG header")
                continue
            if struct.unpack(">II", data[16:24]) != (entry["width"], entry["height"]):
                errors.append(f"{name}: dimensions differ from manifest")
            offset = 8
            while offset + 12 <= len(data):
                size = struct.unpack(">I", data[offset:offset + 4])[0]
                chunk = data[offset + 4:offset + 8]
                end = offset + size + 12
                if end > len(data):
                    errors.append(f"{name}: truncated PNG chunk")
                    break
                if chunk in {b"tEXt", b"zTXt", b"iTXt", b"eXIf"}:
                    errors.append(f"{name}: embedded metadata requires manual review")
                offset = end
                if chunk == b"IEND":
                    if offset != len(data):
                        errors.append(f"{name}: data after PNG end")
                    break
        actual = {path.relative_to(root).as_posix() for path in (root / "assets").rglob("*.png")}
        for name in sorted(actual - listed):
            errors.append(f"{name}: image missing from reviewed manifest")
    except (OSError, KeyError, TypeError, ValueError) as error:
        errors.append(f"assets/manifest.json: invalid manifest ({type(error).__name__})")
    return errors


def check_inventory(root, paths):
    root, errors = Path(root).resolve(), []
    for name in paths:
        if name not in ALLOWED_FILES and not any(pattern.fullmatch(name) for pattern in ALLOWED_PATTERNS):
            errors.append(f"{name}: file outside public showcase allowlist")
            continue
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(f"{name}: symlink or escaped path is not allowed")
        elif path.suffix != ".png":
            try:
                if SECRET_PATTERN.search(path.read_text(encoding="utf-8")):
                    errors.append(f"{name}: recognizable credential pattern; value withheld")
            except (OSError, UnicodeError):
                errors.append(f"{name}: expected readable UTF-8 text")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable summary")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    )
    paths = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
    markdown = [name for name in paths if name.endswith(".md")]
    errors = check_inventory(root, paths) + check_links(root, markdown) + check_media(root)
    report = {"status": "failed" if errors else "passed", "files": len(paths),
              "markdown": len(markdown), "images": len(list((root / "assets").rglob("*.png"))),
              "errors": errors, "external_links_checked": False}
    if options.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        for error in errors:
            print(f"ERROR {error}")
        print(f"Showcase {report['status']}: {len(paths)} files, {len(markdown)} Markdown files, {report['images']} images")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
