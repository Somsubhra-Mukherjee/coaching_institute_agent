import json
import re
from backend.utils.ollama_client import call_redesign_model
from backend.agents.base_template import (
    get_base_template,
    get_all_placeholders,
    TEMPLATE_PLACEHOLDERS
)


def build_filler_prompt(
    website_data: str,
    audit: str,
    previous_values: dict = None,
    feedback: str = ""
) -> str:

    # Strip the raw text excerpt to save tokens and prevent request size limits
    clean_data = website_data
    if "--- RAW PAGE TEXT (excerpt) ---" in website_data:
        clean_data = website_data.split("--- RAW PAGE TEXT (excerpt) ---")[0]

    placeholders_list = "\n".join([f"  - {{{{{p}}}}}" for p in TEMPLATE_PLACEHOLDERS])

    base_prompt = f"""You are a premium CRO copywriter and brand designer filling in placeholders inside a high-converting coaching institute landing page.

WEBSITE DATA (scraped content — use this as your primary source of facts):
{clean_data}

AUDIT FINDINGS:
{audit[:1000]}
"""

    if previous_values and feedback:
        refinement_part = f"""
We already generated an initial set of placeholder values, but the evaluator rejected them with the following feedback:

EVALUATOR FEEDBACK / ISSUES:
{feedback}

PREVIOUS GENERATED VALUES:
{json.dumps(previous_values, indent=2)}

YOUR TASK:
Review the evaluator feedback and the previous values, then output a corrected/refined JSON object mapping. 
You must address the evaluator's feedback (e.g. adjust copy length, fix missing information, correct colors, or provide values for missing keys).
Output the complete corrected mapping for all keys.
"""
    else:
        refinement_part = f"""
YOUR TASK:
Output a single JSON object that maps every placeholder key in the list below to its appropriate replacement value.
Select a premium brand color palette and typography that suits the coaching niche. 

BRANDING & STYLE REQUIREMENTS:
1. COLOR_PRIMARY: Main brand color. If a "DETECTED PRIMARY COLOR" is specified in the website data above, you MUST use that hex color (or a very close premium equivalent).
2. COLOR_PRIMARY_DARK: A darker shade of the primary color (for hovers/active states).
3. COLOR_PRIMARY_LIGHT: A very light pastel/background version of the primary color.
4. COLOR_ACCENT: A vibrant, high-contrast accent color (e.g. orange, gold, teal, or yellow).
5. COLOR_ACCENT_LIGHT: A very light pastel version of the accent color.
6. GOOGLE_FONTS_IMPORT: Import clean, premium Google Fonts (e.g. Outfit, Inter, Syne, Cabinet Grotesk, Roboto) using a CSS @import statement.
7. FONT_HEADING & FONT_BODY: The font-family names mapping to the imported fonts (e.g. "'Outfit', sans-serif").
8. CUSTOM_STYLE_OVERRIDES: Optional custom CSS rules to refine the design (e.g., custom border accents, hover shadows, form focus outlines). Output ONLY clean CSS inside this value, no style tags.

COLOR HARMONY WARNING: Avoid generic, un-premium raw colors like pure red (#ff0000), pure blue (#0000ff), or raw primary colors. Select a highly harmonized, modern premium palette (e.g., if primary is a yellow/gold color, choose a deep slate, charcoal, or elegant teal accent color, not raw red). Use clean HSL-tailored colors.

CONVERSION COPY RULES:
- Use real information (institute name, courses, phone, address) found on the website.
- Never invent numbers or statistics. If student counts or success rates are missing, use feature highlights (e.g. STAT_1_NUM="Expert" STAT_1_LABEL="IITian Faculty", STAT_2_NUM="Live" STAT_2_LABEL="Doubt Support").
- Keep hero headline (HERO_TITLE) under 12 words and subheadline (HERO_SUBTITLE) under 30 words.
- Benefits (TRUST_X_DESC) should be concise (under 12 words).
- FAQs should have clear, direct answers under 25 words.
- All course outcome fields must highlight career prospects (e.g. "Prepare for IIT JEE & NEET - Open doors to Top Engineering & Medical colleges").

REQUIRED PLACEHOLDER KEYS:
{placeholders_list}
"""

    footer_part = """
Output ONLY valid JSON.
No explanation. No markdown fences. No extra text.
Start with { and end with }
Every single key must be mapped to a valid, non-empty string value (e.g. "KEY": "VALUE").
Ensure there are no missing colons, values, or trailing commas at the end of the JSON object.
"""

    return base_prompt + refinement_part + footer_part


def fill_template_with_values(template: str, values: dict) -> str:
    """
    Replace all {{PLACEHOLDER}} occurrences in template with values from dict.
    """
    result = template
    for key, value in values.items():
        placeholder = "{{" + key + "}}"
        result = result.replace(placeholder, str(value))
    return result


def fill_remaining_placeholders(html: str) -> str:
    """
    Find any unfilled {{PLACEHOLDER}} and replace with sensible defaults.
    """
    remaining = re.findall(r'\{\{([A-Z_0-9]+)\}\}', html)

    defaults = {
        "META_TITLE":         "Premier Coaching Institute",
        "META_DESCRIPTION":   "Top coaching institute offering professional courses.",
        "GOOGLE_FONTS_IMPORT":"@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');",
        "COLOR_PRIMARY":      "#1a237e",
        "COLOR_PRIMARY_DARK": "#0d1257",
        "COLOR_PRIMARY_LIGHT":"#e8eaf6",
        "COLOR_ACCENT":       "#e53935",
        "COLOR_ACCENT_LIGHT": "#ffebee",
        "COLOR_TEXT_DARK":    "#1a1a2e",
        "COLOR_TEXT_BODY":    "#374151",
        "COLOR_TEXT_MUTED":   "#6b7280",
        "COLOR_BG_LIGHT":     "#f8fafc",
        "COLOR_BG_SECTION":   "#f1f5f9",
        "COLOR_BORDER":       "#e5e7eb",
        "FONT_HEADING":       "Inter, sans-serif",
        "FONT_BODY":          "Inter, sans-serif",
        "NAV_LOGO_LETTER":    "A",
        "NAV_INSTITUTE_NAME": "Academy",
        "NAV_CTA":            "Enquire Now",
        "PHONE_NUMBER":       "+91 98765 43210",
        "WHATSAPP_LINK":      "https://wa.me/919876543210",
        "EMAIL_ADDRESS":      "info@academy.com",
        "WEBSITE_URL":        "https://academy.com",
        "INSTITUTE_NAME":     "Academy",
        "CITY_NAME":          "India",
        "HERO_TAG":           "Trusted by 5000+ Students",
        "HERO_TITLE":         "Build Your Career with",
        "HERO_TITLE_HIGHLIGHT":"Expert Mentorship",
        "HERO_SUBTITLE":      "Join India's most result-oriented coaching institute.",
        "CTA_PRIMARY":        "Book Free Counselling",
        "CTA_SECONDARY":      "Explore Courses",
        "STAT_1_NUM":         "Daily",
        "STAT_1_LABEL":       "Practice Tests",
        "STAT_2_NUM":         "Live",
        "STAT_2_LABEL":       "Doubt Support",
        "STAT_3_NUM":         "Expert",
        "STAT_3_LABEL":       "Faculty Team",
        "STAT_4_NUM":         "100%",
        "STAT_4_LABEL":       "Syllabus Coverage",
        "BADGE_TITLE":        "Top Ranked Institute",
        "BADGE_SUBTITLE":     "Consistently producing rank holders",
        "TRUST_HEADING":      "Why Students Choose Us",
        "TRUST_SUBHEADING":   "We combine expert teaching with personal mentorship.",
        "TRUST_1_TITLE":      "Expert Faculty",
        "TRUST_1_DESC":       "Experienced faculty with proven track records.",
        "TRUST_2_TITLE":      "Regular Tests",
        "TRUST_2_DESC":       "Weekly tests to ensure consistent progress.",
        "TRUST_3_TITLE":      "Personal Mentorship",
        "TRUST_3_DESC":       "One-on-one guidance for every student.",
        "TRUST_4_TITLE":      "Online + Offline",
        "TRUST_4_DESC":       "Flexible learning modes to suit your schedule.",
        "TRUST_5_TITLE":      "Result Oriented",
        "TRUST_5_DESC":       "Our methods are designed for exam success.",
        "TRUST_6_TITLE":      "Career Guidance",
        "TRUST_6_DESC":       "Complete career support beyond just coaching.",
        "COURSES_HEADING":    "Our Courses",
        "COURSES_SUBHEADING": "Comprehensive programs for your career goals.",
        "COURSE_1_NAME":      "CA",
        "COURSE_1_TAGLINE":   "Chartered Accountancy",
        "COURSE_1_LEVELS":    '<span class="course-level-tag">Foundation</span><span class="course-level-tag">Intermediate</span><span class="course-level-tag">Final</span>',
        "COURSE_1_SUBJECTS":  "<li>Accounting</li><li>Law</li><li>Taxation</li>",
        "COURSE_1_OUTCOME":   "Chartered Accountant — Finance & Business Leader",
        "COURSE_2_NAME":      "CMA",
        "COURSE_2_TAGLINE":   "Cost & Management Accountancy",
        "COURSE_2_LEVELS":    '<span class="course-level-tag">Foundation</span><span class="course-level-tag">Intermediate</span><span class="course-level-tag">Final</span>',
        "COURSE_2_SUBJECTS":  "<li>Cost Accounting</li><li>Management</li><li>Finance</li>",
        "COURSE_2_OUTCOME":   "Management Accountant — Industry Expert",
        "COURSE_3_NAME":      "CS",
        "COURSE_3_TAGLINE":   "Company Secretary",
        "COURSE_3_LEVELS":    '<span class="course-level-tag">Foundation</span><span class="course-level-tag">Executive</span><span class="course-level-tag">Professional</span>',
        "COURSE_3_SUBJECTS":  "<li>Company Law</li><li>Governance</li><li>Compliance</li>",
        "COURSE_3_OUTCOME":   "Company Secretary — Corporate Governance",
        "RESULTS_HEADING":    "Our Results Speak for Themselves",
        "RESULTS_SUBHEADING": "Consistent results year after year.",
        "RESULT_1_NUM":       "Concept",
        "RESULT_1_LABEL":     "Clarity First",
        "RESULT_2_NUM":       "Regular",
        "RESULT_2_LABEL":     "Assessments",
        "RESULT_3_NUM":       "Personal",
        "RESULT_3_LABEL":     "Attention",
        "RESULT_4_NUM":       "Proven",
        "RESULT_4_LABEL":     "Study Methods",
        "TESTIMONIAL_1_TEXT": "The faculty here is exceptional. I cleared my CA Final in the first attempt thanks to their structured approach.",
        "TESTIMONIAL_1_INITIAL":"R",
        "TESTIMONIAL_1_NAME": "Rahul Sharma",
        "TESTIMONIAL_1_META": "CA Final — AIR 42",
        "TESTIMONIAL_2_TEXT": "Best coaching for CMA in the city. Personal attention and regular tests made all the difference.",
        "TESTIMONIAL_2_INITIAL":"P",
        "TESTIMONIAL_2_NAME": "Priya Nair",
        "TESTIMONIAL_2_META": "CMA Intermediate — First Attempt",
        "TESTIMONIAL_3_TEXT": "My parents were worried about online classes but the quality here is outstanding. Highly recommended!",
        "TESTIMONIAL_3_INITIAL":"A",
        "TESTIMONIAL_3_NAME": "Arjun Mehta",
        "TESTIMONIAL_3_META": "CS Foundation — Distinction",
        "FORM_HEADING":       "Get Free Career Guidance",
        "FORM_SUBHEADING":    "Talk to our expert counsellors and find the right path for your career.",
        "FORM_BULLET_1":      "Free 1-on-1 career counselling session",
        "FORM_BULLET_2":      "Course syllabus and fee structure",
        "FORM_BULLET_3":      "Flexible batch timings available",
        "FORM_CARD_TITLE":    "Book Your Free Session",
        "FORM_COURSE_OPTIONS":"<option value='ca'>CA Course</option><option value='cma'>CMA Course</option><option value='cs'>CS Course</option>",
        "FORM_CTA":           "Get Free Career Guidance",
        "FORM_NOTE":          "Your information is 100% private. No spam.",
        "FORM_SUCCESS_TITLE": "We'll Call You Soon!",
        "FORM_SUCCESS_MSG":   "Our counsellor will contact you within 24 hours.",
        "FAQ_HEADING":        "Frequently Asked Questions",
        "FAQ_SUBHEADING":     "Everything you need to know before enrolling.",
        "FAQ_1_Q":            "What courses do you offer?",
        "FAQ_1_A":            "We offer comprehensive coaching for CA, CMA, and CS at all levels.",
        "FAQ_2_Q":            "Do you offer online classes?",
        "FAQ_2_A":            "Yes, we offer both online and offline classes with recorded lectures.",
        "FAQ_3_Q":            "What is the fee structure?",
        "FAQ_3_A":            "Fees vary by course and level. Contact us for detailed fee information.",
        "FAQ_4_Q":            "How experienced is your faculty?",
        "FAQ_4_A":            "Our faculty has 10+ years of experience with proven results.",
        "FAQ_5_Q":            "What is your pass rate?",
        "FAQ_5_A":            "We consistently maintain a 95%+ pass rate across all courses.",
        "FOOTER_ABOUT":       "Premier coaching institute dedicated to student success.",
        "FOOTER_ADDRESS":     "123 Main Street, Your City, India",
        "FOOTER_COPYRIGHT":   "© 2024 Academy. All rights reserved.",
        "FOOTER_COURSE_LINKS":"<li><a href='#courses'>CA Course</a></li><li><a href='#courses'>CMA Course</a></li><li><a href='#courses'>CS Course</a></li>",
        "SOCIAL_FACEBOOK":    "#",
        "SOCIAL_INSTAGRAM":   "#",
        "SOCIAL_YOUTUBE":     "#",
        "CUSTOM_STYLE_OVERRIDES": "/* No custom overrides */",
    }

    for key in remaining:
        if key in defaults:
            html = html.replace("{{" + key + "}}", defaults[key])
        else:
            html = html.replace("{{" + key + "}}", "")

    return html


def parse_filler_json(response: str) -> dict:
    """Extract JSON from model response safely, falling back to robust regex parsing if needed."""

    # Strip <think>...</think> tags produced by reasoning models (e.g. qwen3)
    cleaned = re.sub(r'<think>[\s\S]*?</think>', '', response, flags=re.DOTALL).strip()

    # Direct parse on cleaned response
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Try direct parse on raw response (in case tags stripped too much)
    try:
        return json.loads(response.strip())
    except Exception:
        pass

    # Extract JSON block from cleaned response
    try:
        match = re.search(r'\{[\s\S]*\}', cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    # Extract JSON block from raw response
    try:
        match = re.search(r'\{[\s\S]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    # Regex recovery fallback for flat JSON keys
    try:
        parsed = {}
        # Find all patterns like "KEY" : "VALUE" (handling escaped quotes and newlines within values)
        matches = re.findall(r'"([A-Z_0-9]+)"\s*:\s*"((?:[^"\\]|\\.)*)"', response)
        for k, v in matches:
            # Unescape quotes/slashes
            parsed[k] = v.replace('\\"', '"').replace('\\\\', '\\')
        if len(parsed) > 10:
            print(f"[TEMPLATE MODIFIER] Successfully recovered {len(parsed)} keys using regex parser fallback!")
            return parsed
    except Exception as e:
        print(f"[TEMPLATE MODIFIER] Regex recovery failed: {e}")

    print("[TEMPLATE MODIFIER] JSON parse failed — using defaults only")
    return {}



def run_template_modifier(
    website_data: str,
    audit: str,
    previous_values: dict = None,
    feedback: str = ""
) -> tuple:
    """
    Main entry point.
    Fills the base template with AI-generated content values.
    Returns complete filled HTML and the values dict.
    """
    print("\n[TEMPLATE MODIFIER] Generating content values...")

    try:
        prompt = build_filler_prompt(website_data, audit, previous_values, feedback)
        system = (
            "You are a content specialist for Indian coaching institute websites. "
            "Output ONLY a valid JSON object. "
            "No markdown. No explanation. Just JSON."
        )

        response = call_redesign_model(prompt, system)
        import sys
        enc = sys.stdout.encoding or 'utf-8'
        print(f"[TEMPLATE MODIFIER] Model raw response (preview):\n{response[:500]}...".encode(enc, errors='replace').decode(enc))
        values   = parse_filler_json(response)

        # Merge previous values with new values so we don't lose any keys
        if previous_values:
            merged = previous_values.copy()
            merged.update(values)
            values = merged

        print(f"[TEMPLATE MODIFIER] Got {len(values)} values from model")

        # Fill template
        template = get_base_template()
        html     = fill_template_with_values(template, values)

        # Fill any remaining unfilled placeholders with defaults
        html = fill_remaining_placeholders(html)

        # Verify no placeholders remain
        remaining = re.findall(r'\{\{([A-Z_0-9]+)\}\}', html)
        if remaining:
            print(f"[TEMPLATE MODIFIER] Warning: {len(remaining)} placeholders still unfilled: {remaining[:5]}")

        print(f"[TEMPLATE MODIFIER] Done. HTML size: {len(html)} chars")
        return html, values

    except Exception as e:
        print(f"[TEMPLATE MODIFIER] ERROR: {e} — returning default-filled template")
        template = get_base_template()
        return fill_remaining_placeholders(template), {}