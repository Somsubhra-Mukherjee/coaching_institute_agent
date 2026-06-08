import os
import json
from pathlib import Path
from datetime import datetime
from slugify import slugify


# ── Output directories ──────────────────────────────────────────────────────
if os.getenv("VERCEL"):
    BASE_OUTPUT_DIR = Path("/tmp/outputs")
else:
    BASE_OUTPUT_DIR = Path("outputs")

AUDITS_DIR = BASE_OUTPUT_DIR / "audits"
REDESIGNS_DIR = BASE_OUTPUT_DIR / "redesigns"
SCREENSHOTS_DIR = BASE_OUTPUT_DIR / "screenshots"
METADATA_DIR = BASE_OUTPUT_DIR / "metadata"
SITE_TEXT_DIR = BASE_OUTPUT_DIR / "site-text"

for d in [AUDITS_DIR, REDESIGNS_DIR, SCREENSHOTS_DIR, METADATA_DIR, SITE_TEXT_DIR]:
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


def save_site_text(scraped_data: dict, slug: str) -> str:
    """Save scraped website raw text and individual text types to site-text folder."""
    # 1. Save raw text
    raw_path = SITE_TEXT_DIR / f"{slug}_sitetext.txt"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(scraped_data.get("raw_text", ""))

    # 2. Save headings
    headings_path = SITE_TEXT_DIR / f"{slug}_headings.txt"
    with open(headings_path, "w", encoding="utf-8") as f:
        for h in scraped_data.get("headings", []):
            f.write(f"[{h.get('tag', 'H')}] {h.get('text', '')}\n")

    # 3. Save paragraphs
    paragraphs_path = SITE_TEXT_DIR / f"{slug}_paragraphs.txt"
    with open(paragraphs_path, "w", encoding="utf-8") as f:
        for p in scraped_data.get("paragraphs", []):
            f.write(f"{p}\n")

    # 4. Save buttons & CTA
    buttons_path = SITE_TEXT_DIR / f"{slug}_buttons.txt"
    with open(buttons_path, "w", encoding="utf-8") as f:
        f.write("--- CTA BUTTONS ---\n")
        for btn in scraped_data.get("cta_texts", []):
            f.write(f"{btn}\n")
        f.write("\n--- ALL BUTTONS/LINKS ---\n")
        for btn in scraped_data.get("buttons", []):
            f.write(f"{btn}\n")

    # 5. Save testimonials
    testimonials_path = SITE_TEXT_DIR / f"{slug}_testimonials.txt"
    with open(testimonials_path, "w", encoding="utf-8") as f:
        for t in scraped_data.get("testimonials", []):
            f.write(f"{t}\n")

    # 6. Save image alt texts
    alts_path = SITE_TEXT_DIR / f"{slug}_image_alts.txt"
    with open(alts_path, "w", encoding="utf-8") as f:
        for alt in scraped_data.get("images_alt", []):
            f.write(f"{alt}\n")

    # 7. Also save a structured overview summary
    overview_path = SITE_TEXT_DIR / f"{slug}_overview.txt"
    from backend.scraper.website_scraper import format_scraped_data_for_prompt
    with open(overview_path, "w", encoding="utf-8") as f:
        f.write(format_scraped_data_for_prompt(scraped_data))

    print(f"[FILE MANAGER] Saved all text types to {SITE_TEXT_DIR} with slug {slug}")
    return str(raw_path)


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