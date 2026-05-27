#!/usr/bin/env python3

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
HEADER = ROOT / "ext" / "php_opentelemetry.h"
PACKAGE = ROOT / "ext" / "package.xml"


def main() -> int:
    header = HEADER.read_text(encoding="utf-8")
    match = re.search(r'#define\s+PHP_OPENTELEMETRY_VERSION\s+"([^"]+)"', header)
    if not match:
        print("Unable to find PHP_OPENTELEMETRY_VERSION in ext/php_opentelemetry.h", file=sys.stderr)
        return 1

    header_version = match.group(1)
    ns = {"pkg": "http://pear.php.net/dtd/package-2.0"}
    release_version = ET.parse(PACKAGE).getroot().findtext("pkg:version/pkg:release", namespaces=ns)
    if not release_version:
        print("Unable to find version/release in ext/package.xml", file=sys.stderr)
        return 1

    if header_version != release_version:
        print(
            f"Version mismatch: ext/php_opentelemetry.h={header_version} "
            f"ext/package.xml={release_version}",
            file=sys.stderr,
        )
        return 1

    print(f"Validated extension version: {header_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
