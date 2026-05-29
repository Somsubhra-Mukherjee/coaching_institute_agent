import os
import json
from pathlib import Path
from datetime import datetime
from slugify import slugify


# ── Output directories ──────────────────────────────────────────────────────
BASE_OUTPUT_DIR = Path("outputs")
AUDITS_DIR = BASE_OUTPUT_DIR / "audits"
REDESIGNS_DIR = BASE_OUTPUT_DIR / "redesigns"
SCREENSHOTS_DIR = BASE_OUTPUT_DIR / "screenshots"
METADATA_DIR = BASE_OUTPUT_DIR / "metadata"

for d in [AUDITS_DIR, REDESIGNS_DIR, SCREENSHOTS_DIR, METADATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def generate_file_slug(url: str) -> str:
    """Generate a unique slug from URL + timestamp."""
    clean = url.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = clean.split("/")[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{slugify(domain)}_{timestamp}"


def get_domain_slug(url: str) -> str:
    """Get clean domain-only slug (no timestamp), used as redesign folder name."""
    clean = url.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = clean.split("/")[0]
    return slugify(domain)


def save_audit(audit_text: str, slug: str) -> str:
    """Save audit text to .txt file. Returns file path."""
    filename = f"{slug}_audit.txt"
    filepath = AUDITS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"WEBSITE AUDIT REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(audit_text)

    print(f"[FILE MANAGER] Audit saved: {filepath}")
    return str(filepath)


def save_redesign(html_code: str, slug: str) -> str:
    """Save HTML redesign to outputs/redesigns/<domain>/index.html. Returns file path."""
    # Strip _YYYYMMDD_HHMMSS timestamp suffix → just the domain part
    parts = slug.split("_")
    domain_folder = "_".join(parts[:-2]) if len(parts) >= 3 else slug

    folder = REDESIGNS_DIR / domain_folder
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / "index.html"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"[FILE MANAGER] Redesign saved: {filepath}")
    return str(filepath)


def save_metadata(metadata: dict, slug: str) -> str:
    """Save run metadata to JSON file."""
    filename = f"{slug}_meta.json"
    filepath = METADATA_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)

    print(f"[FILE MANAGER] Metadata saved: {filepath}")
    return str(filepath)


def list_previous_runs() -> list:
    """Return list of all previous generation runs."""
    runs = []

    for meta_file in sorted(METADATA_DIR.glob("*_meta.json"), reverse=True):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                runs.append(data)
        except Exception as e:
            print(f"[FILE MANAGER] Error reading {meta_file}: {e}")

    return runs


def read_file(filepath: str) -> str:
    """Read and return content of any saved file."""
    path = Path(filepath)
    if not path.exists():
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()