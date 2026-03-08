"""Utilities for updating cat records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


IMMUTABLE_FIELDS = {"id", "created_at"}


class CatUpdateError(ValueError):
    """Raised when a cat update payload is invalid."""


def update_cat_record(current: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Return an updated cat record.

    Rules:
    - Immutable fields ("id", "created_at") cannot be changed.
    - Unknown fields are accepted to keep the updater flexible.
    - None values in updates delete fields from the record.
    """
    if not isinstance(current, dict):
        raise CatUpdateError("current record must be an object")
    if not isinstance(updates, dict):
        raise CatUpdateError("updates must be an object")

    merged = dict(current)

    for key, value in updates.items():
        if key in IMMUTABLE_FIELDS and current.get(key) != value:
            raise CatUpdateError(f'field "{key}" is immutable')

        if value is None:
            merged.pop(key, None)
            continue

        merged[key] = value

    return merged


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CatUpdateError(f"{path} must contain a JSON object")
    return data


def run_cli() -> int:
    parser = argparse.ArgumentParser(description="Update a cat JSON record")
    parser.add_argument("current", type=Path, help="Current cat JSON file")
    parser.add_argument("updates", type=Path, help="Update payload JSON file")
    parser.add_argument("--output", "-o", type=Path, help="Optional output file")
    args = parser.parse_args()

    updated = update_cat_record(_load_json(args.current), _load_json(args.updates))
    payload = json.dumps(updated, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(run_cli())
