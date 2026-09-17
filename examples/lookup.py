#!/usr/bin/env python3
"""Offline queries against the unified model catalog.

    python examples/lookup.py --spec image --sort price
    python examples/lookup.py --grep nano-banana --columns id,name,unit
    python examples/lookup.py --id gpt-image-2.5-ext
    python examples/lookup.py --models
"""
from __future__ import annotations

import argparse
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "models.json"


def headline(record: dict) -> float | None:
    """Lowest effective price in the record, for sorting."""
    prices = record.get("prices") or {}
    values = []
    for cell in prices.values():
        if isinstance(cell, dict):
            value = cell.get("effective", cell.get("list"))
            if isinstance(value, (int, float)):
                values.append(float(value))
    return min(values) if values else None


def main() -> None:
    ap = argparse.ArgumentParser(description="Query the offline model catalog")
    ap.add_argument("--spec", help="image | second | token | times")
    ap.add_argument("--grep", help="substring match on the model id or display name")
    ap.add_argument("--id", help="print one record")
    ap.add_argument("--models", action="store_true", help="print model ids only")
    ap.add_argument("--sort", choices=["price", "id"], default="id")
    ap.add_argument("--columns", default="id,name,specification,unit,headline")
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    records = json.loads(DATA.read_text())["models"]
    if args.id:
        match = next((r for r in records if r["id"] == args.id), None)
        if not match:
            raise SystemExit(f"unknown model id {args.id!r}")
        print(json.dumps(match, indent=2, ensure_ascii=False))
        return

    rows = records
    if args.spec:
        rows = [r for r in rows if r.get("specification") == args.spec]
    if args.grep:
        needle = args.grep.lower()
        rows = [r for r in rows if needle in r["id"].lower() or needle in (r.get("name") or "").lower()]

    if args.models:
        for r in rows[: args.limit]:
            print(r["id"])
        return

    if args.sort == "price":
        rows = sorted(rows, key=lambda r: (headline(r) is None, headline(r) or 0.0))

    columns = [c.strip() for c in args.columns.split(",")]
    for r in rows[: args.limit]:
        values = []
        for column in columns:
            if column == "headline":
                value = headline(r)
                values.append(f"${value:.4f}" if value is not None else "—")
            else:
                values.append(str(r.get(column, "—")))
        print("  ".join(values))


if __name__ == "__main__":
    main()
