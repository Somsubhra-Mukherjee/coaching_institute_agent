import asyncio
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from slugify import slugify


# ── Windows event loop fix for Playwright ──────────────────────────────────
# On Windows, asyncio needs ProactorEventLoop for subprocess (which Playwright uses)
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass


# ── Output folder for screenshots ──────────────────────────────────────────
import os
if os.getenv("VERCEL"):
    SCREENSHOTS_DIR = Path("/tmp/outputs/screenshots")
else:
    SCREENSHOTS_DIR = Path("outputs/screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    """Remove extra whitespace and blank lines."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_domain(url: str) -> str:
    """Extract clean domain name for use in filenames."""
    url = url.replace("https://", "").replace("http://", "").replace("www.", "")
    domain = url.split("/")[0]
    return slugify(domain)


async def scrape_website(url: str) -> dict:
    """
    Main scraping function.
    Opens the URL with Playwright, extracts content, takes screenshot.
    Returns a structured dict with all extracted data.
    """

    print(f"\n[SCRAPER] Starting scrape for: {url}")

    domain_slug = extract_domain(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"{domain_slug}_{timestamp}.png"
    screenshot_path = SCREENSHOTS_DIR / screenshot_filename

    scraped_data = {
        "url": url,
        "domain": domain_slug,
        "timestamp": timestamp,
        "screenshot_path": str(screenshot_path),
        "meta": {},
        "headings": [],
        "paragraphs": [],
        "buttons": [],
        "nav_items": [],
        "forms": [],
        "testimonials": [],
        "cta_texts": [],
        "images_alt": [],
        "raw_text": "",
        "detected_primary": "#1a237e",
        "all_colors": [],
        "scrape_success": False,
        "error": None
    }

    try:
        try:
            async with async_playwright() as p:

                print("[SCRAPER] Launching Chromium browser...")
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )

                context = await browser.new_context(
                    viewport={"width": 1440, "height": 900},
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                )

                page = await context.new_page()

                print(f"[SCRAPER] Navigating to {url} ...")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                # Wait a bit for JS to render
                await asyncio.sleep(3)

                # ── Take full-page screenshot ───────────────────────────────
                print("[SCRAPER] Taking full-page screenshot...")
                await page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )
                print(f"[SCRAPER] Screenshot saved: {screenshot_path}")

                # ── Get full HTML content ───────────────────────────────────
                html_content = await page.content()
                page_title = await page.title()

                # ── Extract colors from computed styles ───────────────────────
                print("[SCRAPER] Extracting computed style colors...")
                try:
                    colors_data = await page.evaluate("""() => {
                        function rgbToHex(rgb) {
                            if (!rgb) return null;
                            const matches = rgb.match(/^rgb\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)$/);
                            if (!matches) {
                                const rgbaMatches = rgb.match(/^rgba\\((\\d+),\\s*(\\d+),\\s*(\\d+),\\s*([\\d.]+)\\)$/);
                                if (rgbaMatches && parseFloat(rgbaMatches[4]) === 0) return null;
                                if (rgbaMatches) return "#" + rgbaMatches.slice(1, 4).map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
                                return null;
                            }
                            return "#" + matches.slice(1, 4).map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
                        }

                        const colorStats = {};
                        const elements = document.querySelectorAll('button, a, h1, h2, header, [class*="nav"], [class*="menu"], [class*="btn"], [class*="button"]');
                        elements.forEach(el => {
                            const style = window.getComputedStyle(el);
                            const bg = rgbToHex(style.backgroundColor);
                            const fg = rgbToHex(style.color);
                            
                            if (bg && bg !== '#ffffff' && bg !== '#000000' && bg !== '#transparent') {
                                colorStats[bg] = (colorStats[bg] || 0) + 1;
                            }
                            if (fg && fg !== '#ffffff' && fg !== '#000000' && fg !== '#333333' && fg !== '#222222' && fg !== '#1a1a2e') {
                                colorStats[fg] = (colorStats[fg] || 0) + 1;
                            }
                        });

                        let primaryHex = '#1a237e';
                        let maxCount = 0;
                        for (const [color, count] of Object.entries(colorStats)) {
                            if (count > maxCount) {
                                maxCount = count;
                                primaryHex = color;
                            }
                        }
                        return {
                            detected_primary: primaryHex,
                            all_colors: Object.keys(colorStats).slice(0, 5)
                        };
                    }""")
                    scraped_data["detected_primary"] = colors_data.get("detected_primary", "#1a237e")
                    scraped_data["all_colors"] = colors_data.get("all_colors", [])
                    print(f"[SCRAPER] Detected primary color: {scraped_data['detected_primary']}, all: {scraped_data['all_colors']}")
                except Exception as e:
                    print(f"[SCRAPER] Color extraction failed: {e}")

                await browser.close()
        except Exception as playwright_err:
            print(f"[SCRAPER] Playwright launching failed/not installed: {playwright_err}. Falling back to HTTPX/Requests + thum.io...")
            import httpx
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
                resp = await client.get(url, headers=headers)
                html_content = resp.text
                
            page_title = url
            title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
            if title_match:
                page_title = title_match.group(1).strip()
                
            try:
                print("[SCRAPER] Fetching screenshot from thum.io...")
                screenshot_url = f"https://image.thum.io/get/width/1280/{url}"
                async with httpx.AsyncClient(timeout=15.0) as client:
                    s_resp = await client.get(screenshot_url)
                    if s_resp.status_code == 200:
                        with open(screenshot_path, "wb") as f:
                            f.write(s_resp.content)
                        print(f"[SCRAPER] Screenshot saved from thum.io: {screenshot_path}")
                    else:
                        print(f"[SCRAPER] thum.io returned status {s_resp.status_code}")
            except Exception as se:
                print(f"[SCRAPER] Failed to fetch screenshot: {se}")

        # ── Parse with BeautifulSoup ────────────────────────────────────
        print("[SCRAPER] Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style tags to clean text
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # ── Meta data ──────────────────────────────────────────────────
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        og_title = soup.find("meta", attrs={"property": "og:title"})
        og_desc = soup.find("meta", attrs={"property": "og:description"})

        scraped_data["meta"] = {
            "title": clean_text(page_title),
            "description": clean_text(meta_desc["content"]) if meta_desc and meta_desc.get("content") else "",
            "keywords": clean_text(meta_keywords["content"]) if meta_keywords and meta_keywords.get("content") else "",
            "og_title": clean_text(og_title["content"]) if og_title and og_title.get("content") else "",
            "og_description": clean_text(og_desc["content"]) if og_desc and og_desc.get("content") else "",
        }

        # ── Headings ───────────────────────────────────────────────────
        headings = []
        for tag in ["h1", "h2", "h3", "h4"]:
            for el in soup.find_all(tag):
                text = clean_text(el.get_text())
                if text and len(text) > 2:
                    headings.append({"tag": tag, "text": text})
        scraped_data["headings"] = headings[:30]  # cap at 30

        # ── Paragraphs ─────────────────────────────────────────────────
        paragraphs = []
        for el in soup.find_all("p"):
            text = clean_text(el.get_text())
            if text and len(text) > 20:
                paragraphs.append(text)
        scraped_data["paragraphs"] = paragraphs[:20]  # cap at 20

        # ── Buttons and CTAs ───────────────────────────────────────────
        buttons = []
        cta_texts = []

        for el in soup.find_all(["button", "a"]):
            text = clean_text(el.get_text())
            if text and len(text) > 1 and len(text) < 80:
                buttons.append(text)
                # Identify CTA-like text
                cta_keywords = [
                    "enroll", "register", "join", "contact", "apply",
                    "download", "get", "start", "book", "call", "whatsapp",
                    "free", "demo", "trial", "admission", "enquire", "enquiry"
                ]
                if any(kw in text.lower() for kw in cta_keywords):
                    cta_texts.append(text)

        scraped_data["buttons"] = list(set(buttons))[:25]
        scraped_data["cta_texts"] = list(set(cta_texts))[:10]

        # ── Navigation items ───────────────────────────────────────────
        nav_items = []
        nav_tags = soup.find_all("nav")
        if nav_tags:
            for nav in nav_tags:
                for el in nav.find_all("a"):
                    text = clean_text(el.get_text())
                    if text and len(text) > 1:
                        nav_items.append(text)
        scraped_data["nav_items"] = list(set(nav_items))[:15]

        # ── Forms ──────────────────────────────────────────────────────
        forms = []
        for form in soup.find_all("form"):
            form_data = {
                "fields": [],
                "submit_text": ""
            }
            for inp in form.find_all(["input", "select", "textarea"]):
                field_type = inp.get("type", inp.name)
                placeholder = inp.get("placeholder", "")
                label = inp.get("name", "")
                if field_type not in ["hidden", "submit"]:
                    form_data["fields"].append({
                        "type": field_type,
                        "placeholder": clean_text(placeholder),
                        "name": clean_text(label)
                    })
            submit = form.find(["input", "button"], attrs={"type": "submit"})
            if submit:
                form_data["submit_text"] = clean_text(
                    submit.get("value", "") or submit.get_text()
                )
            if form_data["fields"]:
                forms.append(form_data)
        scraped_data["forms"] = forms[:5]

        # ── Testimonials ───────────────────────────────────────────────
        testimonials = []
        testimonial_keywords = [
            "testimonial", "review", "feedback", "student", "parent",
            "success", "result", "topper", "rank", "selected"
        ]
        for el in soup.find_all(attrs={"class": True}):
            classes = " ".join(el.get("class", []))
            if any(kw in classes.lower() for kw in testimonial_keywords):
                text = clean_text(el.get_text())
                if text and len(text) > 30:
                    testimonials.append(text[:300])
        scraped_data["testimonials"] = testimonials[:6]

        # ── Image alt texts ────────────────────────────────────────────
        images_alt = []
        for img in soup.find_all("img"):
            alt = clean_text(img.get("alt", ""))
            if alt and len(alt) > 2:
                images_alt.append(alt)
        scraped_data["images_alt"] = images_alt[:15]

        # ── Raw text (full page text dump, capped) ─────────────────────
        raw_text = clean_text(soup.get_text(separator=" "))
        scraped_data["raw_text"] = raw_text[:10000]  # cap at 10000 chars

        scraped_data["scrape_success"] = True
        print(f"[SCRAPER] Scraping complete for {url}")
        print(f"[SCRAPER] Found: {len(headings)} headings, {len(paragraphs)} paragraphs, {len(buttons)} buttons")

    except Exception as e:
        scraped_data["error"] = str(e)
        scraped_data["scrape_success"] = False
        print(f"[SCRAPER] ERROR: {e}")

    return scraped_data


def format_scraped_data_for_prompt(data: dict) -> str:
    """
    Converts scraped data dict into a clean readable string
    to be passed into LLM prompts.
    """
    lines = []

    lines.append(f"WEBSITE URL: {data.get('url', '')}")
    lines.append(f"PAGE TITLE: {data['meta'].get('title', 'N/A')}")
    lines.append(f"META DESCRIPTION: {data['meta'].get('description', 'N/A')}")
    lines.append(f"META KEYWORDS: {data['meta'].get('keywords', 'N/A')}")
    lines.append(f"DETECTED PRIMARY COLOR: {data.get('detected_primary', '#1a237e')}")
    lines.append(f"DETECTED BRAND COLORS: {', '.join(data.get('all_colors', []))}")
    lines.append("")

    lines.append("--- HEADINGS ---")
    for h in data.get("headings", []):
        lines.append(f"[{h['tag'].upper()}] {h['text']}")
    lines.append("")

    lines.append("--- NAVIGATION ITEMS ---")
    lines.append(", ".join(data.get("nav_items", [])) or "None found")
    lines.append("")

    lines.append("--- CALL TO ACTION BUTTONS ---")
    lines.append(", ".join(data.get("cta_texts", [])) or "None found")
    lines.append("")

    lines.append("--- ALL BUTTONS / LINKS ---")
    lines.append(", ".join(data.get("buttons", [])[:15]) or "None found")
    lines.append("")

    lines.append("--- PARAGRAPHS (first 5) ---")
    for p in data.get("paragraphs", [])[:5]:
        lines.append(f"• {p}")
    lines.append("")

    lines.append("--- FORMS ---")
    for i, form in enumerate(data.get("forms", []), 1):
        lines.append(f"Form {i}:")
        for field in form.get("fields", []):
            lines.append(f"  - {field['type']}: {field['placeholder'] or field['name']}")
        lines.append(f"  Submit: {form.get('submit_text', 'N/A')}")
    lines.append("")

    lines.append("--- TESTIMONIALS ---")
    for t in data.get("testimonials", []):
        lines.append(f"• {t[:200]}")
    lines.append("")

    lines.append("--- IMAGE ALT TEXTS ---")
    lines.append(", ".join(data.get("images_alt", [])) or "None found")
    lines.append("")

    lines.append("--- RAW PAGE TEXT (excerpt) ---")
    lines.append(data.get("raw_text", "")[:8000])

    return "\n".join(lines)


# ── Quick test runner ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

    async def main():
        data = await scrape_website(test_url)
        print("\n========== SCRAPE RESULT ==========")
        print(json.dumps(data, indent=2, default=str)[:3000])
        print("\n========== FORMATTED FOR PROMPT ==========")
        print(format_scraped_data_for_prompt(data))

    asyncio.run(main())