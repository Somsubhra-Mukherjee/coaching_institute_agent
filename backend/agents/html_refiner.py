# import re
# from backend.utils.ollama_client import call_redesign_model


# def build_refiner_prompt(html_code: str, ui_system: dict) -> str:

#     colors = ui_system.get("colors", {})
#     spacing = ui_system.get("spacing_system", {})
#     components = ui_system.get("components", {})

#     primary     = colors.get("primary", "#1a237e")
#     accent      = colors.get("accent", "#e53935")
#     text_body   = colors.get("text_body", "#374151")
#     bg_light    = colors.get("bg_light", "#f8fafc")
#     border_col  = colors.get("border", "#e5e7eb")

#     card_radius  = components.get("card", {}).get("border_radius", "16px")
#     card_shadow  = components.get("card", {}).get("box_shadow", "0 2px 12px rgba(0,0,0,0.06)")
#     card_hover   = components.get("card", {}).get("hover_shadow", "0 8px 32px rgba(0,0,0,0.12)")
#     card_transform = components.get("card", {}).get("hover_transform", "translateY(-4px)")

#     section_pad  = ui_system.get("layout", {}).get("section_padding_desktop", "80px 0")
#     section_mob  = ui_system.get("layout", {}).get("section_padding_mobile", "48px 0")
#     container    = ui_system.get("layout", {}).get("container_max_width", "1200px")
#     grid_gap     = ui_system.get("layout", {}).get("grid_gap", "24px")

#     return f"""
# You are an expert HTML/CSS refiner. You receive a coaching institute landing page HTML
# and must improve it WITHOUT changing the content, sections, or structure.

# ORIGINAL HTML:
# {html_code}

# YOUR TASK — APPLY THESE SPECIFIC FIXES:

# 1. SPACING FIXES:
#    - All sections must have padding: {section_pad} on desktop
#    - All sections must have padding: {section_mob} on mobile
#    - All .container elements must have max-width: {container} and margin: 0 auto
#    - Card grids must have gap: {grid_gap}
#    - No element should touch the edge of the screen on mobile (min 16px side padding)

# 2. CARD FIXES:
#    - All cards must have border-radius: {card_radius}
#    - All cards must have box-shadow: {card_shadow}
#    - All cards must have: transition: all 0.3s ease
#    - All cards on hover: box-shadow: {card_hover}, transform: {card_transform}
#    - All cards must have consistent padding (28px 24px desktop, 20px 16px mobile)

# 3. BUTTON FIXES:
#    - Primary CTA buttons: background {primary}, color white, padding 14px 32px, border-radius 8px, font-weight 600
#    - Primary buttons on hover: filter brightness(0.9), transform translateY(-2px)
#    - All buttons: cursor pointer, transition all 0.2s, border none
#    - Mobile buttons: width 100%, padding 16px

# 4. TYPOGRAPHY FIXES:
#    - H1: font-size 48px desktop / 32px mobile, font-weight 800, line-height 1.15
#    - H2: font-size 36px desktop / 26px mobile, font-weight 700
#    - H3: font-size 22px desktop / 18px mobile, font-weight 600
#    - Body text: font-size 16px, line-height 1.7, color {text_body}
#    - No paragraph should exceed 65 characters wide (use max-width on text blocks)

# 5. COLOR CONSISTENCY:
#    - Primary color throughout: {primary}
#    - Accent color: {accent}
#    - Section backgrounds must alternate: #ffffff and {bg_light}
#    - All borders: {border_col}

# 6. FORM FIXES:
#    - All form inputs: height 52px, border-radius 8px, padding 0 16px
#    - All form inputs: border 1.5px solid {border_col}, font-size 15px
#    - All form inputs on focus: border-color {primary}, outline none
#    - Form labels: font-size 13px, font-weight 600, margin-bottom 6px
#    - Submit button: full width, height 52px, background {primary}

# 7. MOBILE FIXES (max-width: 768px):
#    - All multi-column grids become 1 column
#    - All flex rows become column direction
#    - Nav hides links, shows hamburger or just logo + CTA
#    - Hero text centers on mobile
#    - Stats become 2x2 grid on mobile
#    - Remove all horizontal scroll triggers
#    - Images max-width 100%

# 8. WHATSAPP BUTTON:
#    - Must be fixed, bottom-right, z-index 9999
#    - Size: 60px x 60px, border-radius 50%
#    - Background: #25d366
#    - Box-shadow: 0 4px 20px rgba(37,211,102,0.4)
#    - On hover: transform scale(1.1)

# 9. SECTION HEADINGS:
#    - Every section must have a centered H2 with margin-bottom 48px
#    - Optional subtitle below H2: font-size 16px, color {text_body}, max-width 560px, margin auto

# 10. FAQ ACCORDION:
#     - Questions must have cursor pointer, padding 20px 24px
#     - Smooth max-height transition on open/close
#     - Plus/minus icon that rotates on open
#     - Border-bottom between items

# 11. MISSING HOVER STATES — ADD IF MISSING:
#     - Nav links: color {primary} on hover
#     - Cards: shadow + lift on hover
#     - Buttons: brightness shift on hover
#     - Footer links: color {primary} on hover

# 12. GENERAL POLISH:
#     - Add scroll-behavior: smooth to html
#     - Add box-sizing: border-box to * selector
#     - Ensure no content overflows horizontally
#     - Add proper meta viewport tag if missing
#     - Ensure WhatsApp floating button is always visible

# OUTPUT ONLY THE COMPLETE IMPROVED HTML FILE.
# Do not explain changes.
# Do not add comments outside the HTML.
# Start with <!DOCTYPE html> and end with </html>
# """


# def extract_html(response: str) -> str:
#     """Extract clean HTML from model response."""
#     patterns = [
#         r"```html\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
#         r"```\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
#         r"(<!DOCTYPE[\s\S]*?</html>)"
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, response, re.IGNORECASE)
#         if match:
#             return match.group(1).strip()
#     return response.strip()


# def run_html_refiner(html_code: str, ui_system: dict) -> str:
#     """
#     Main entry point.
#     Takes generated HTML + UI system spec.
#     Returns polished HTML.
#     """
#     print("\n[HTML REFINER] Starting HTML refinement...")

#     if not html_code or len(html_code) < 500:
#         print("[HTML REFINER] HTML too short — skipping refinement")
#         return html_code

#     try:
#         prompt = build_refiner_prompt(html_code, ui_system)
#         system = (
#             "You are an expert HTML/CSS developer. "
#             "Apply all specified fixes precisely. "
#             "Output ONLY complete valid HTML. "
#             "Start with <!DOCTYPE html>. End with </html>."
#         )

#         response = call_redesign_model(prompt, system)
#         refined_html = extract_html(response)

#         if len(refined_html) < 1000:
#             print("[HTML REFINER] Refined HTML too short — returning original")
#             return html_code

#         print(f"[HTML REFINER] Done. Original: {len(html_code)} chars → Refined: {len(refined_html)} chars")
#         return refined_html

#     except Exception as e:
#         print(f"[HTML REFINER] ERROR: {e} — returning original HTML")
#         return html_code


import re
from backend.utils.ollama_client import call_redesign_model


def build_refiner_prompt(html_code: str, ui_system: dict) -> str:
    colors  = ui_system.get("colors",   {})
    spacing = ui_system.get("spacing_system", {})
    layout  = ui_system.get("layout",   {})

    primary    = colors.get("primary",    "#1a237e")
    accent     = colors.get("accent",     "#e53935")
    text_body  = colors.get("text_body",  "#374151")
    bg_light   = colors.get("bg_light",   "#f8fafc")
    border_col = colors.get("border",     "#e5e7eb")
    whatsapp   = colors.get("whatsapp",   "#25d366")

    container  = layout.get("container_max_width",   "1200px")
    sec_pad_d  = layout.get("section_padding_desktop","80px 0")
    sec_pad_m  = layout.get("section_padding_mobile", "48px 0")
    grid_gap   = layout.get("grid_gap",               "24px")

    return f"""
You are a CSS specialist refining a coaching institute landing page.
The HTML structure and content are correct. Your job is ONLY to fix CSS and polish.

ORIGINAL HTML:
{html_code}

APPLY THESE FIXES — DO NOT CHANGE CONTENT OR STRUCTURE:

CSS VARIABLE CHECK:
Ensure :root contains ALL of these exact values:
  --primary:       {primary};
  --primary-dark:  {colors.get('primary_dark','#0d1257')};
  --primary-light: {colors.get('primary_light','#e8eaf6')};
  --accent:        {accent};
  --text-dark:     {colors.get('text_dark','#1a1a2e')};
  --text-body:     {text_body};
  --text-muted:    {colors.get('text_muted','#6b7280')};
  --bg-light:      {bg_light};
  --border:        {border_col};
  --whatsapp:      {whatsapp};

SPACING FIXES:
  All .section elements: padding {sec_pad_d}
  All .container elements: max-width {container}; margin 0 auto; padding 0 24px
  Card grids (.trust-cards,.course-cards,.testimonial-cards): gap {grid_gap}
  No element touches screen edge on mobile (min padding-left/right 16px)

CARD HOVER POLISH:
  .trust-card:hover,.course-card:hover,.testimonial-card:hover {{
    box-shadow: 0 12px 48px rgba(0,0,0,0.14);
    transform: translateY(-4px);
    transition: all 0.3s ease
  }}

BUTTON POLISH:
  .btn-primary:hover {{
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2)
  }}
  .btn-outline:hover {{ background: var(--primary); color: #fff; transform: translateY(-2px) }}
  All buttons: cursor pointer; transition all 0.2s; font-family inherit

INPUT FOCUS:
  .form-input:focus, .form-select:focus {{
    border-color: {primary};
    box-shadow: 0 0 0 3px {colors.get('primary_light','#e8eaf6')};
    outline: none
  }}

MOBILE (@media max-width:768px):
  .section {{ padding: {sec_pad_m} }}
  .hero-inner {{ grid-template-columns: 1fr }}
  .hero-content h1 {{ font-size: 30px }}
  .hero-cta .btn {{ width: 100% }}
  .trust-cards {{ grid-template-columns: repeat(2,1fr) }}
  .course-cards {{ grid-template-columns: 1fr }}
  .testimonial-cards {{ grid-template-columns: 1fr }}
  .results-stats {{ grid-template-columns: repeat(2,1fr) }}
  .lead-form-inner {{ grid-template-columns: 1fr }}
  .footer-grid {{ grid-template-columns: 1fr }}
  .nav-links,.nav-phone {{ display: none }}
  .nav-hamburger {{ display: flex }}
  .mobile-cta-bar {{ display: flex }}
  body {{ padding-bottom: 60px }}
  .whatsapp-float {{ bottom: 76px; right: 16px }}

WHATSAPP BUTTON VERIFY:
  .whatsapp-float must be: position fixed; bottom 28px (76px on mobile);
  right 28px (16px on mobile); width 60px; height 60px; border-radius 50%;
  background #25d366; z-index 9999; transition all 0.3s

SECTION ALTERNATING BACKGROUNDS:
  #hero: background linear-gradient(135deg, #fff 0%, {bg_light} 100%)
  #trust: background #fff
  #courses: background {bg_light}
  #results: background #fff
  #lead-form: background {bg_light}
  #faq: background #fff
  #footer: background {colors.get('text_dark','#1a1a2e')}

TYPOGRAPHY VERIFY:
  h1: line-height 1.15; font-weight 800
  h2: line-height 1.25; font-weight 700
  body: line-height 1.7; color {text_body}
  Max paragraph width: 65ch

OUTPUT THE COMPLETE HTML FILE WITH FIXES APPLIED.
Do not change any text content. Do not remove any sections.
Do not add new sections. Only fix CSS.
Start with <!DOCTYPE html>. End with </html>.
"""


def extract_html(response: str) -> str:
    for pattern in [
        r"```html\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
        r"```\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
        r"(<!DOCTYPE[\s\S]*?</html>)"
    ]:
        m = re.search(pattern, response, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return response.strip()


def run_html_refiner(html_code: str, ui_system: dict) -> str:
    print("\n[HTML REFINER] Starting refinement...")

    if not html_code or len(html_code) < 500:
        print("[HTML REFINER] HTML too short — skipping")
        return html_code

    try:
        prompt = build_refiner_prompt(html_code, ui_system)
        system = (
            "You are a CSS specialist. "
            "Fix CSS issues only. Never change text content. "
            "Output complete valid HTML starting with <!DOCTYPE html>."
        )

        response    = call_redesign_model(prompt, system)
        refined     = extract_html(response)

        if len(refined) < len(html_code) * 0.7:
            print("[HTML REFINER] Output too short — returning original")
            return html_code

        print(f"[HTML REFINER] Done. {len(html_code)} → {len(refined)} chars")
        return refined

    except Exception as e:
        print(f"[HTML REFINER] ERROR: {e} — returning original")
        return html_code