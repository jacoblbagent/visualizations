#!/usr/bin/env python3
"""Check the Visualizations hub against what actually exists on disk.

Answers two questions every run:

  * Is every card on the hub still sound?  Thumbnail present, thumbnail the
    right aspect, localhost port registered in the Hermes web UI, project
    directory still on disk, source repo linked.
  * Is anything that looks like a visualization missing from the hub?

Exit status is 0 when the hub is sound and nothing is unflagged, 1 otherwise.
The start script runs this on every boot; run it by hand any time:

    python3 tools/check_hub.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HOME = Path.home()
HUB = Path(__file__).resolve().parent.parent
CODE = HOME / "Code"
INDEX = HUB / "index.html"
REGISTRY = CODE / "hermes-web-ui" / "scripts" / "projects.json"
EXCLUDE = HUB / "tools" / "hub-exclude.txt"

# Index.html is hand-written markup; these pull the same four facts the README
# tells you to change when you add a card.
RE_CARD = re.compile(r'<article class="card">(.*?)</article>', re.S)
RE_PORT = re.compile(r'http://localhost:(\d+)')
RE_TITLE = re.compile(r"<h2>\s*<a[^>]*>(.*?)<svg", re.S)
RE_THUMB = re.compile(r'<img src="([^"]+)"[^>]*width="(\d+)" height="(\d+)"')
RE_REPO = re.compile(r'href="(https://github\.com/[^"]+)"')


def read_excludes() -> set[str]:
    if not EXCLUDE.exists():
        return set()
    out = set()
    for line in EXCLUDE.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(line)
    return out


def parse_cards() -> list[dict]:
    raw = INDEX.read_text()
    cards = []
    for block in RE_CARD.findall(raw):
        port = RE_PORT.search(block)
        title = RE_TITLE.search(block)
        thumb = RE_THUMB.search(block)
        repo = RE_REPO.search(block)
        cards.append(
            {
                "title": html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else "(no title)",
                "port": int(port.group(1)) if port else None,
                "thumb": thumb.group(1) if thumb else None,
                "declared": (int(thumb.group(2)), int(thumb.group(3))) if thumb else None,
                "repo": repo.group(1) if repo else None,
            }
        )
    return cards


def parse_registry() -> dict[int, dict]:
    """Every registered project by check_port — the sidebar's own rows AND the
    pieces nested under one (a project's `children`).

    A hub card's piece is registered in the same file whether it is a row of its
    own or a piece of another project: same keys, same start script, same probe.
    Only its PLACEMENT differs — the sidebar draws it in a fold under its
    parent — so the hub's check has to read both levels or every card looks
    unregistered.
    """
    if not REGISTRY.exists():
        return {}
    data = json.loads(REGISTRY.read_text())
    out: dict[int, dict] = {}
    for p in data.get("projects", []):
        for q in (p, *(p.get("children") or [])):
            if "check_port" in q:
                out[q["check_port"]] = q
    return out


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def main() -> int:
    cards = parse_cards()
    registry = parse_registry()
    excludes = read_excludes()

    problems: list[str] = []
    card_ids: set[str] = set()
    seen_ports: set[int] = set()

    for card in cards:
        label = card["title"]

        if card["port"] is None:
            problems.append(f"{label}: no localhost link in the card")
        elif card["port"] in seen_ports:
            problems.append(f"{label}: port {card['port']} used by another card")
        else:
            seen_ports.add(card["port"])
            entry = registry.get(card["port"])
            if entry is None:
                problems.append(f"{label}: port {card['port']} is not in projects.json")
            else:
                card_ids.add(entry["id"])
                if not (CODE / entry["id"]).is_dir():
                    problems.append(f"{label}: ~/Code/{entry['id']} is gone")
                if not (CODE / "hermes-web-ui" / "scripts" / f"start-{entry['id']}.sh").exists():
                    problems.append(f"{label}: no start-{entry['id']}.sh")

        if card["thumb"] is None:
            problems.append(f"{label}: no thumbnail")
        else:
            path = HUB / card["thumb"]
            if not path.exists():
                problems.append(f"{label}: {card['thumb']} is missing")
            elif card["declared"]:
                actual = image_size(path)
                if actual and actual != card["declared"]:
                    problems.append(
                        f"{label}: thumbnail is {actual[0]}x{actual[1]}, card declares "
                        f"{card['declared'][0]}x{card['declared'][1]}"
                    )

        if card["repo"] is None:
            problems.append(f"{label}: no source repo link")

    # Anything on disk that looks like a visualization but has no card.
    candidates = []
    for entry in sorted(CODE.iterdir()):
        if not entry.is_dir() or entry.name.startswith(".") or entry.name == HUB.name:
            continue
        if entry.name in card_ids or entry.name in excludes:
            continue
        if not (entry / "index.html").exists():
            continue
        candidates.append(entry.name)

    print(f"cards: {len(cards)}    not in hub: {len(candidates)}    problems: {len(problems)}")

    if candidates:
        print("\n  not in hub (add a card, or list it in tools/hub-exclude.txt):")
        for name in candidates:
            print(f"    {name}")

    if problems:
        print("\n  problems:")
        for p in problems:
            print(f"    {p}")

    if not candidates and not problems:
        print("  clean")

    return 1 if (problems or candidates) else 0


if __name__ == "__main__":
    sys.exit(main())
