from backend.utils.ollama_client import call_audit_model
from backend.utils.image_utils import screenshot_to_base64, get_image_size_kb


def build_prompt_generator_system() -> str:
    return (
        "You are a senior UI/UX strategist and conversion rate optimization expert "
        "specializing in Indian coaching institute websites. "
        "You analyze websites deeply and write extremely detailed, specific design briefs "
        "that frontend developers use to build high-converting landing pages. "
        "Be specific. Be visual. Be conversion-focused. Reference actual content from the website."
    )


def build_prompt_generator_input(
    url: str,
    website_data: str,
    audit: str,
    screenshot_base64: str = ""
) -> str:
    """
    Build the input prompt for the prompt generator agent.
    """

    screenshot_note = ""
    if screenshot_base64:
        screenshot_note = (
            "A full-page screenshot of the current website has been captured. "
            "Use it to understand the current visual design, color scheme, layout problems, "
            "branding elements, and overall aesthetic quality.\n"
        )
    else:
        screenshot_note = (
            "No screenshot available. "
            "Base your visual analysis entirely on the scraped content below.\n"
        )

    return f"""
You are analyzing a coaching institute website to write a detailed redesign prompt.

WEBSITE URL: {url}

{screenshot_note}

SCRAPED WEBSITE CONTENT:
{website_data}

AUDIT FINDINGS (problems identified):
{audit}

YOUR TASK:
Write a comprehensive, detailed HTML redesign prompt that another AI (a frontend developer agent)
will use to build the complete landing page.

The prompt you write must be SO detailed and specific that the developer agent
can build the entire page without asking any questions.

FOLLOW THIS EXACT STRUCTURE FOR YOUR OUTPUT PROMPT:

---START OF REDESIGN PROMPT---

Create a premium, modern, mobile-first coaching institute website redesign for [INSTITUTE NAME].

Extract and use:
- The institute's actual name from the scraped content
- Their actual courses/programs, exact terminology, and key marketing keywords
- Their actual location/city
- Their actual contact details if available
- Their actual testimonials if available
- Their actual results/achievements if available
- Their actual faculty names if available
- Their actual color scheme or branding colors (Use the DETECTED PRIMARY COLOR from the scraping metadata. If the main color from the screenshot/site is red, use red; if blue, use blue, etc.)

THE DESIGN MUST FEEL:
[Write 5-7 specific feeling descriptors based on what this institute needs]

AVOID:
[List 3-5 specific things to avoid based on current website problems]

COLOR SCHEME:
[Specify exact colors based on current branding OR recommend a professional palette. Strictly use the detected brand color as Primary]
Primary: #[hex]
Secondary: #[hex]  
Accent: #[hex]
Text: #[hex]
Background: #[white or near-white]

CUSTOM CSS / LAYOUT OVERRIDES:
[Provide 3-5 specific CSS rules to override default layouts, such as custom hero gradients, card shadow effects, customized list markers, or section padding tweaks to make the template look highly personalized, unique, and non-generic]

CURRENT WEBSITE PROBLEMS TO SOLVE:
[List every problem from the audit in bullet points, be specific]

REDESIGN PRIORITIES:
[List 8-10 specific priorities based on the audit]

SECTION 1 — HERO
[Write detailed specs for hero section including:
- Exact headline (use institute name and actual courses)
- Exact subheadline
- CTA button labels and colors
- What stats/numbers to show (use real ones from scrape if available)
- Visual style description
- Mobile behavior
- Sticky mobile CTA bar specs]

SECTION 2 — TRUST/WHY US
[Write detailed specs including:
- Icon card layout
- Specific points to highlight (use real info from website)
- Card design style
- Mobile layout behavior]

SECTION 3 — COURSES
[Write detailed specs for each actual course found on the website:
- Card structure
- What info each card shows
- CTA on each card
- How cards behave on mobile]

SECTION 4 — RESULTS & TESTIMONIALS
[Write detailed specs including:
- How to display results (use real numbers if found)
- Testimonial card design
- Mobile carousel behavior
- Trust badge design]

SECTION 5 — FACULTY + LEAD FORM
[Write detailed specs including:
- Faculty card design (use real names if found)
- Lead form fields
- Form CTA text
- Layout split on desktop vs mobile]

SECTION 6 — FAQ + FOOTER
[Write detailed specs including:
- 5 specific FAQ questions relevant to this institute and location
- Footer layout
- Contact info placement
- WhatsApp button specs
- Google Maps embed]

SEO REQUIREMENTS:
[List 8-10 specific SEO requirements with actual keywords for this institute]

UI/COMPONENT REQUIREMENTS:
[List 15-20 specific UI requirements]

TECHNICAL REQUIREMENTS:
- Single HTML file
- All CSS in <style> tags
- All JS in <script> tags
- No external CSS frameworks
- Google Fonts via @import only
- Font Awesome via CDN for icons
- Fully responsive mobile-first
- Must open directly in browser

OUTPUT ONLY HTML. No explanation outside the HTML.
Start with <!DOCTYPE html> end with </html>

---END OF REDESIGN PROMPT---

IMPORTANT RULES FOR YOUR OUTPUT:
1. Replace ALL placeholders like [INSTITUTE NAME] with actual values from the scraped data
2. Include real course names, real location, real contact info where available
3. Make the color scheme match the current branding or improve it specifically
4. Reference actual problems found — not generic problems
5. Be extremely specific about every section's layout and content
6. The prompt you write should be 600-900 words minimum
7. Output ONLY the prompt text between the ---START--- and ---END--- markers
"""


def extract_generated_prompt(response: str) -> str:
    """
    Extract the prompt text between the START and END markers.
    Falls back to full response if markers not found.
    """
    import re

    # Try to extract between markers
    match = re.search(
        r"---START OF REDESIGN PROMPT---(.*?)---END OF REDESIGN PROMPT---",
        response,
        re.DOTALL | re.IGNORECASE
    )
    if match:
        return match.group(1).strip()

    # Fallback: return full response stripped
    return response.strip()


def run_prompt_generator(
    url: str,
    website_data: str,
    audit: str,
    screenshot_path: str = ""
) -> str:
    """
    Main function: runs the prompt generator agent.
    Returns the generated redesign prompt string.
    """
    print("\n[PROMPT GENERATOR] Starting prompt generation...")

    # Load screenshot if available
    screenshot_base64 = ""
    if screenshot_path:
        size_kb = get_image_size_kb(screenshot_path)
        print(f"[PROMPT GENERATOR] Screenshot size: {size_kb:.1f} KB")

        # Only include if reasonably sized (under 2MB)
        if size_kb < 2048:
            screenshot_base64 = screenshot_to_base64(screenshot_path)
        else:
            print("[PROMPT GENERATOR] Screenshot too large, skipping image encoding")

    # Build the input prompt
    input_prompt = build_prompt_generator_input(
        url=url,
        website_data=website_data[:10000],
        audit=audit,
        screenshot_base64=screenshot_base64
    )

    system = build_prompt_generator_system()

    try:
        print("[PROMPT GENERATOR] Calling LLM to generate redesign prompt...")
        response = call_audit_model(input_prompt, system)
        generated_prompt = extract_generated_prompt(response)

        print(f"[PROMPT GENERATOR] Prompt generated. Length: {len(generated_prompt)} chars")
        return generated_prompt

    except Exception as e:
        print(f"[PROMPT GENERATOR] ERROR: {e}")
        # Return a basic fallback prompt
        return f"""
Create a premium, modern, mobile-first coaching institute landing page.
Website: {url}

Use the following scraped content to build the page:
{website_data[:2000]}

Problems to fix based on audit:
{audit[:1000]}

Build a clean, conversion-focused single HTML file with:
1. Hero section with strong headline and 2 CTAs
2. Why Choose Us section with icon cards
3. Courses section with course cards
4. Testimonials section
5. Lead capture form
6. FAQ and Footer

Requirements:
- Single HTML file, CSS in style tags, JS in script tags
- Mobile-first responsive
- WhatsApp floating button
- Professional Indian education website aesthetic
Output only HTML starting with <!DOCTYPE html>
"""