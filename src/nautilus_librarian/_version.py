"""Get Version from pyproject.toml"""

from pathlib import Path
from typing import Any

import atoml
from atoml import TOMLDocument

from nautilus_librarian._helpers import get_unicode_document, path_to_pyproject_toml


def parse_toml_doc_from_string(string: str) -> TOMLDocument:
    """Get the Toml Document from Path"""

    return atoml.parse(string=string)


def extract_version_from_toml_doc(doc: TOMLDocument) -> str:
    """Get the version from the Toml Document"""

    # ["tool"]["poetry"]["version"]
    tools: Any = doc["tool"]
    poetry: Any = tools["poetry"]
    version: str = poetry["version"]

    return version


def get_version() -> str:
    """Get the version from the Toml Document"""
    path: Path = path_to_pyproject_toml()
    doc: str = get_unicode_document(path)
    toml_doc: TOMLDocument = parse_toml_doc_from_string(doc)
    version: str = extract_version_from_toml_doc(toml_doc)

    return version


# We expect poetry-dynamic-versioning to replace the 0.0.0 string with the version from the latest git tag at build time
__version__: str = "0.0.0"

if __version__ == "0.0.0":
    __version__ = get_version()

if __name__ == "__main__":
    print(get_version())
