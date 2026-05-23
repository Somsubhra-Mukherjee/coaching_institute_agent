import json
import re
from backend.utils.ollama_client import call_audit_model
from backend.agents.base_template import (
    get_base_template,
    get_all_placeholders,
    TEMPLATE_PLACEHOLDERS
)


def build_filler_prompt(
    website_data: str,
    audit: str,
    generated_prompt: str,
    ui_system: dict
) -> str:

    colors  = ui_system.get("colors", {})
    typo    = ui_system.get("typography", {})
    sections = ui_system.get("sections", [])

    primary       = colors.get("primary",       "#1a237e")
    primary_dark  = colors.get("primary_dark",  "#0d1257")
    primary_light = colors.get("primary_light", "#e8eaf6")
    accent        = colors.get("accent",        "#e53935")
    accent_light  = colors.get("accent_light",  "#ffebee")
    text_dark     = colors.get("text_dark",     "#1a1a2e")
    text_body     = colors.get("text_body",     "#374151")
    text_muted    = colors.get("text_muted",    "#6b7280")
    bg_light      = colors.get("bg_light",      "#f8fafc")
    bg_section    = colors.get("bg_section",    "#f1f5f9")
    border        = colors.get("border",        "#e5e7eb")

    fonts_import  = typo.get("google_fonts_import",
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');")
    font_heading  = typo.get("font_family_heading", "Inter, sans-serif")
    font_body     = typo.get("font_family_body",    "Inter, sans-serif")

    placeholders_list = "\n".join([f"  - {{{{{p}}}}}" for p in TEMPLATE_PLACEHOLDERS])

    return f"""
You are filling in a premium HTML template for an Indian coaching institute website.

WEBSITE DATA (scraped content — use this as your primary source):
{website_data}

AUDIT FINDINGS:
{audit[:600]}

DESIGN BRIEF:
{generated_prompt[:800]}

UI SYSTEM COLORS:
  Primary:       {primary}
  Primary Dark:  {primary_dark}
  Primary Light: {primary_light}
  Accent:        {accent}
  Accent Light:  {accent_light}
  Text Dark:     {text_dark}
  Text Body:     {text_body}
  Text Muted:    {text_muted}
  Bg Light:      {bg_light}
  Bg Section:    {bg_section}
  Border:        {border}

FONTS:
  Google Fonts Import: {fonts_import}
  Heading Font: {font_heading}
  Body Font:    {font_body}

YOUR TASK:
Output a single JSON object that maps every placeholder key to its replacement value.
Extract real values from the website data wherever possible.
Use realistic, specific content — never generic filler.

PLACEHOLDER KEYS TO FILL:
{placeholders_list}

RULES:
1. Extract REAL institute name, courses, phone, address from website data
2. For courses: only include courses actually mentioned in website data
   - If only 1-2 courses exist, still fill all 3 course slots but make course 2/3 variants
   - COURSE_X_LEVELS: output as HTML like:
     <span class="course-level-tag">Foundation</span><span class="course-level-tag">Intermediate</span>
   - COURSE_X_SUBJECTS: output as HTML like:
     <li>Accounting</li><li>Economics</li><li>Law</li>
3. FORM_COURSE_OPTIONS: output as HTML like:
   <option value="ca">CA Course</option><option value="cma">CMA Course</option>
4. FOOTER_COURSE_LINKS: output as HTML like:
   <li><a href="#courses">CA Course</a></li><li><a href="#courses">CMA Course</a></li>
5. NAV_LOGO_LETTER: first letter of institute name only
6. PHONE_NUMBER: extract from website data, use "+91 98765 43210" if not found
7. WHATSAPP_LINK: format as https://wa.me/91XXXXXXXXXX
8. EMAIL_ADDRESS: extract from website or use info@institutename.com
9. WEBSITE_URL: use the actual URL from website data
10. TESTIMONIALS: write realistic, specific testimonials for this institute's courses
11. STATS: use real numbers if available, otherwise realistic ones (e.g. "5000+", "15+", "98%")
12. FAQs: write questions specifically relevant to this institute's courses and location
13. All color values: use the exact hex codes from UI SYSTEM COLORS above
14. GOOGLE_FONTS_IMPORT: use exactly: {fonts_import}
15. FONT_HEADING and FONT_BODY: use exactly: {font_heading} and {font_body}

CONVERSION COPY RULES:
- HERO_TITLE: strong, benefit-focused, mentions course names
- HERO_TITLE_HIGHLIGHT: the most important word or phrase (will be colored)
- HERO_SUBTITLE: 1-2 lines, result-focused, mention location if available
- CTA_PRIMARY: action phrase like "Book Free Counselling" or "Start Your Journey"
- CTA_SECONDARY: "Explore Courses" or "View Programs"
- FORM_CTA: "Get Free Career Guidance" or "Book My Free Session"
- FORM_NOTE: "Your information is 100% private. No spam."
- FORM_SUCCESS_TITLE: "We'll Call You Soon!"
- FORM_SUCCESS_MSG: "Our counsellor will contact you within 24 hours."

OUTPUT ONLY A VALID JSON OBJECT.
No explanation. No markdown fences. No extra text.
Start with {{ and end with }}
Every key must be a string from the placeholder list above.
Every value must be a non-empty string.
"""


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
        "STAT_1_NUM":         "5000+",
        "STAT_1_LABEL":       "Students Trained",
        "STAT_2_NUM":         "15+",
        "STAT_2_LABEL":       "Years Experience",
        "STAT_3_NUM":         "98%",
        "STAT_3_LABEL":       "Pass Rate",
        "STAT_4_NUM":         "4.8★",
        "STAT_4_LABEL":       "Google Rating",
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
        "RESULT_1_NUM":       "5000+",
        "RESULT_1_LABEL":     "Students Trained",
        "RESULT_2_NUM":       "500+",
        "RESULT_2_LABEL":     "Rank Holders",
        "RESULT_3_NUM":       "98%",
        "RESULT_3_LABEL":     "Pass Rate",
        "RESULT_4_NUM":       "15+",
        "RESULT_4_LABEL":     "Years of Excellence",
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
    }

    for key in remaining:
        if key in defaults:
            html = html.replace("{{" + key + "}}", defaults[key])
        else:
            html = html.replace("{{" + key + "}}", "")

    return html


def parse_filler_json(response: str) -> dict:
    """Extract JSON from model response safely."""
    # Direct parse
    try:
        return json.loads(response.strip())
    except Exception:
        pass

    # Extract JSON block
    try:
        match = re.search(r'\{[\s\S]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    print("[TEMPLATE MODIFIER] JSON parse failed — using defaults only")
    return {}


def run_template_modifier(
    website_data: str,
    audit: str,
    generated_prompt: str,
    ui_system: dict
) -> str:
    """
    Main entry point.
    Fills the base template with AI-generated content values.
    Returns complete filled HTML.
    """
    print("\n[TEMPLATE MODIFIER] Generating content values...")

    try:
        prompt = build_filler_prompt(website_data, audit, generated_prompt, ui_system)
        system = (
            "You are a content specialist for Indian coaching institute websites. "
            "Output ONLY a valid JSON object. "
            "No markdown. No explanation. Just JSON."
        )

        response = call_audit_model(prompt, system)
        values   = parse_filler_json(response)

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
        return html

    except Exception as e:
        print(f"[TEMPLATE MODIFIER] ERROR: {e} — returning default-filled template")
        template = get_base_template()
        return fill_remaining_placeholders(template)