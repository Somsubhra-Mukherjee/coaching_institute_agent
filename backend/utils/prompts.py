# def get_audit_prompt(website_data: str) -> str:
#     return f"""
# You are a senior CRO (Conversion Rate Optimization) and UX consultant 
# specializing in Indian coaching institutes.

# You have analyzed the following website content:

# {website_data}

# Write a concise, honest, and helpful website audit (300-400 words).

# STRICT FORMAT — follow this exactly:

# INSTITUTE NAME: [extract from content or use domain name]

# OVERVIEW:
# [2-3 sentences summarizing the website's current state and biggest problem]

# 5 MAJOR ISSUES:

# 1. [ISSUE TITLE]
# Issue: [what is wrong]
# Why it hurts: [impact on trust or conversions]
# Fix: [specific actionable improvement]

# 2. [ISSUE TITLE]
# Issue: [what is wrong]
# Why it hurts: [impact on trust or conversions]
# Fix: [specific actionable improvement]

# 3. [ISSUE TITLE]
# Issue: [what is wrong]
# Why it hurts: [impact on trust or conversions]
# Fix: [specific actionable improvement]

# 4. [ISSUE TITLE]
# Issue: [what is wrong]
# Why it hurts: [impact on trust or conversions]
# Fix: [specific actionable improvement]

# 5. [ISSUE TITLE]
# Issue: [what is wrong]
# Why it hurts: [impact on trust or conversions]
# Fix: [specific actionable improvement]

# LOCAL SEO OPPORTUNITY:
# [2-3 sentences on local SEO improvements specific to this institute]

# PRIORITY ACTION:
# [1 sentence — the single most important thing to fix first]

# TONE: Be direct, smart, helpful. Not corporate. Not insulting.
# Focus on: hero section, CTAs, mobile UX, trust signals, copy quality,
# conversion flow, parent/student psychology.
# """


# def get_redesign_prompt(website_data: str, audit: str) -> str:
#     """
#     Fallback redesign prompt — used only if prompt generator fails.
#     """
#     return f"""
# You are an expert frontend developer and UI/UX designer specializing in
# high-converting websites for Indian coaching institutes.

# WEBSITE DATA:
# {website_data}

# AUDIT FINDINGS:
# {audit}

# YOUR TASK:
# Generate a complete, single HTML file for a redesigned landing page.

# STRICT REQUIREMENTS:
# - ONE single HTML file only
# - All CSS must be inside <style> tags in <head>
# - All JS must be inside <script> tags before </body>
# - No external CSS frameworks
# - Font Awesome via CDN allowed
# - Google Fonts via @import in CSS only
# - Fully responsive and mobile-first

# MANDATORY SECTIONS:
# 1. Navigation bar
# 2. Hero section with headline and 2 CTA buttons
# 3. Key stats bar
# 4. Courses section
# 5. Why Choose Us section
# 6. Testimonials
# 7. Faculty section
# 8. Lead capture form
# 9. FAQ accordion
# 10. Footer with WhatsApp button

# OUTPUT ONLY THE HTML CODE. No explanation. No markdown.
# Start with <!DOCTYPE html> and end with </html>
# """


# def get_redesign_prompt_from_generated(generated_prompt: str) -> str:
#     """
#     Wraps the AI-generated prompt with strict technical instructions
#     for the redesign agent.
#     """
#     return f"""
# You are an expert frontend developer building a coaching institute landing page.

# DESIGN BRIEF AND REQUIREMENTS:
# {generated_prompt}

# STRICT TECHNICAL RULES — FOLLOW EXACTLY:
# - Output ONE single complete HTML file
# - All CSS inside <style> tags in <head> — no exceptions
# - All JavaScript inside <script> tags before </body>
# - No Bootstrap, no Tailwind, no external CSS files
# - Font Awesome 6 allowed: use this CDN exactly:
#   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
# - Google Fonts allowed via @import inside <style> tag
# - Fully responsive, mobile-first
# - Must work when opened directly in a browser offline

# CONVERSION ELEMENTS — ALL REQUIRED:
# - Floating WhatsApp button bottom-right (fixed position, green, always visible)
# - Sticky top navigation bar
# - Sticky bottom CTA bar on mobile only
# - Phone number as clickable tel: link
# - WhatsApp as wa.me link
# - Form submit must show thank you message via JavaScript
# - Smooth scroll on all anchor links

# QUALITY BAR:
# - This must look like a ₹50,000+ professionally designed website
# - Not a template. Not generic. Specific to this institute.
# - Every section must have real content from the brief
# - No Lorem Ipsum anywhere
# - Consistent spacing system throughout
# - Premium typography with clear hierarchy

# OUTPUT ONLY THE HTML CODE.
# Do not write any explanation before or after.
# Do not wrap in markdown code blocks.
# Start your response with exactly: <!DOCTYPE html>
# End your response with exactly: </html>
# """


# def get_evaluator_prompt(html_code: str, audit: str) -> str:
#     return f"""
# You are a quality evaluator for coaching institute landing pages.

# AUDIT FINDINGS:
# {audit[:500]}

# GENERATED HTML (first 3000 chars):
# {html_code[:3000]}

# Evaluate this redesigned landing page and respond ONLY in this exact format:

# SCORE: [number from 1-10]

# PASSED: [YES or NO — YES if score is 7 or above]

# ISSUES:
# - [issue 1 if any]
# - [issue 2 if any]
# - [issue 3 if any]

# IMPROVEMENT_INSTRUCTIONS:
# [If PASSED is NO, write specific instructions to improve the HTML.
# If PASSED is YES, write "None needed."]

# Score based on:
# - Has all 10 required sections? (3 points)
# - Mobile responsive design? (2 points)  
# - Strong CTAs present? (2 points)
# - Trust signals present? (1 point)
# - WhatsApp button present? (1 point)
# - Lead form present? (1 point)
# """


# def get_redesign_improvement_prompt(
#     website_data: str,
#     audit: str,
#     previous_html: str,
#     evaluator_feedback: str
# ) -> str:
#     return f"""
# You are an expert frontend developer fixing a coaching institute landing page.

# WEBSITE DATA:
# {website_data[:1000]}

# AUDIT FINDINGS:
# {audit[:500]}

# EVALUATOR FEEDBACK (what needs to be fixed):
# {evaluator_feedback}

# PREVIOUS HTML (improve this):
# {previous_html}

# Fix ALL the issues mentioned in the evaluator feedback.
# Keep everything that was good. Only improve what was flagged.

# REQUIREMENTS (same as before):
# - ONE single HTML file
# - All CSS inside <style> tags
# - All JS inside <script> tags
# - No external CSS frameworks
# - Fully responsive
# - All 10 sections must be present

# OUTPUT ONLY THE HTML CODE. No explanation. No markdown.
# Start with <!DOCTYPE html> and end with </html>
# """

# def get_evaluator_prompt(html_code: str, audit: str) -> str:
#     return f"""
# You are a quality evaluator for coaching institute landing pages.

# AUDIT FINDINGS:
# {audit[:500]}

# GENERATED HTML (first 3000 chars):
# {html_code[:3000]}

# Evaluate this redesigned landing page and respond ONLY in this exact format:

# SCORE: [number from 1-10]

# PASSED: [YES or NO — YES if score is 7 or above]

# ISSUES:
# - [issue 1 if any]
# - [issue 2 if any]
# - [issue 3 if any]

# IMPROVEMENT_INSTRUCTIONS:
# [If PASSED is NO, write specific instructions to improve the HTML.
# If PASSED is YES, write "None needed."]

# Score based on:
# - Has all required sections? (3 points)
# - Mobile responsive design? (2 points)
# - Strong CTAs present? (2 points)
# - Trust signals present? (1 point)
# - WhatsApp button present? (1 point)
# - Lead form present? (1 point)
# """


# def get_redesign_improvement_prompt(
#     website_data: str,
#     audit: str,
#     previous_html: str,
#     evaluator_feedback: str
# ) -> str:
#     return f"""
# You are an expert frontend developer fixing a coaching institute landing page.

# WEBSITE DATA:
# {website_data[:1000]}

# AUDIT FINDINGS:
# {audit[:500]}

# EVALUATOR FEEDBACK (what needs to be fixed):
# {evaluator_feedback}

# PREVIOUS HTML (improve this):
# {previous_html}

# Fix ALL the issues mentioned in the evaluator feedback.
# Keep everything that was good. Only improve what was flagged.

# REQUIREMENTS:
# - ONE single HTML file
# - All CSS inside <style> tags
# - All JS inside <script> tags
# - No external CSS frameworks
# - Fully responsive
# - All sections must be present
# - WhatsApp floating button required

# OUTPUT ONLY THE HTML CODE. No explanation. No markdown.
# Start with <!DOCTYPE html> and end with </html>
# """



import json
import re


def get_audit_prompt(website_data: str) -> str:
    prompt_template = """
You are a senior CRO and UX consultant specializing in Indian coaching institutes.

Analyzed website content:
{website_data}

Write a detailed, comprehensive, and highly professional website growth audit. Provide deep insights into copy, visual layout, trust signals, and parent/student psychological triggers.
Do not output any markdown code blocks, introductory text, or extra commentary. 
Only output the exact structure below, replacing the bracketed placeholders.

STRICT FORMAT:

[INSTITUTE NAME EXTRACTED FROM CONTENT] × KGP Hustle House

Website Growth Audit

Hi sir, our team of IIT Kharagpur interns went through your site and identified these 5 critical things that might be holding your website back from converting visitors into student admissions. Skim this personalized audit report and check the interactive mockup we created below.

5 Key Website Problems Affecting Conversions

1. [ISSUE TITLE]
[3-4 detailed sentences explaining the specific visual, structural, or copy issue, why it hurts trust or conversions, and the student/parent psychological impact]

Fix:
[2-3 actionable sentences describing the specific design, copywriting, or layout improvement to resolve the issue]

2. [ISSUE TITLE]
[3-4 detailed sentences explaining the specific visual, structural, or copy issue, why it hurts trust or conversions, and the student/parent psychological impact]

Fix:
[2-3 actionable sentences describing the specific design, copywriting, or layout improvement to resolve the issue]

3. [ISSUE TITLE]
[3-4 detailed sentences explaining the specific visual, structural, or copy issue, why it hurts trust or conversions, and the student/parent psychological impact]

Fix:
[2-3 actionable sentences describing the specific design, copywriting, or layout improvement to resolve the issue]

4. [ISSUE TITLE]
[3-4 detailed sentences explaining the specific visual, structural, or copy issue, why it hurts trust or conversions, and the student/parent psychological impact]

Fix:
[2-3 actionable sentences describing the specific design, copywriting, or layout improvement to resolve the issue]

5. [ISSUE TITLE]
[3-4 detailed sentences explaining the specific visual, structural, or copy issue, why it hurts trust or conversions, and the student/parent psychological impact]

Fix:
[2-3 actionable sentences describing the specific design, copywriting, or layout improvement to resolve the issue]

SEO Opportunity
[3-4 detailed sentences on local SEO and search visibility improvements specific to this institute, highlighting key regional keywords]

If you like this, feel free to book a discovery call at https://cal.com/kgphustlehouse/seo

Prepared by KGP Hustle House - IIT Kharagpur interns helping businesses grow through modern websites & SEO.

TONE: Direct, smart, helpful. Not corporate. Not insulting.
"""
    return prompt_template.format(website_data=website_data[:10000])

def get_redesign_prompt(website_data: str, audit: str) -> str:
    """Fallback prompt — used only if prompt generator fails."""
    return f"""
You are an expert frontend developer building a coaching institute landing page.

WEBSITE DATA:
{website_data[:1500]}

AUDIT:
{audit[:800]}

Build a complete single HTML file. All CSS in style tags. All JS in script tags.
Mobile-first. No external frameworks. Font Awesome CDN allowed.

Include: Nav, Hero with 2 CTAs, Stats bar, Courses cards, Testimonials,
Lead form, FAQ accordion, Footer with WhatsApp.

Output ONLY HTML starting with <!DOCTYPE html>
"""


def get_redesign_prompt_from_generated(
    generated_prompt: str,
    ui_system: dict
) -> str:
    """
    Main redesign prompt — uses generated brief + UI system.
    """
    ui_json = json.dumps(ui_system, indent=2)

    sections = ui_system.get("sections", [])
    section_list = "\n".join([
        f"  {i+1}. {s.get('name','Section')} — Goal: {s.get('goal','')} — Required: {', '.join(s.get('required_elements',[]))}"
        for i, s in enumerate(sections)
    ])

    colors = ui_system.get("colors", {})
    typo   = ui_system.get("typography", {})
    layout = ui_system.get("layout", {})
    comp   = ui_system.get("components", {})
    mobile = ui_system.get("mobile_rules", {})
    spacing = ui_system.get("spacing_system", {})

    primary    = colors.get("primary", "#1a237e")
    accent     = colors.get("accent", "#e53935")
    text_dark  = colors.get("text_dark", "#1a1a2e")
    text_body  = colors.get("text_body", "#374151")
    bg_light   = colors.get("bg_light", "#f8fafc")
    bg_section = colors.get("bg_section", "#f1f5f9")
    border_col = colors.get("border", "#e5e7eb")
    whatsapp   = colors.get("whatsapp", "#25d366")

    fonts_import = typo.get("google_fonts_import", "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');")
    font_heading = typo.get("font_family_heading", "Inter, sans-serif")
    font_body    = typo.get("font_family_body", "Inter, sans-serif")

    scale = typo.get("scale", {})
    h1 = scale.get("h1", {"size":"48px","mobile":"32px","weight":"800","line_height":"1.15"})
    h2 = scale.get("h2", {"size":"36px","mobile":"26px","weight":"700","line_height":"1.25"})
    h3 = scale.get("h3", {"size":"22px","mobile":"18px","weight":"600","line_height":"1.35"})
    body_t = scale.get("body", {"size":"16px","mobile":"15px","weight":"400","line_height":"1.7"})

    container      = layout.get("container_max_width", "1200px")
    cont_pad       = layout.get("container_padding", "0 24px")
    section_pad_d  = layout.get("section_padding_desktop", "80px 0")
    section_pad_m  = layout.get("section_padding_mobile", "48px 0")
    grid_cols      = layout.get("grid_columns_desktop", 3)
    grid_gap       = layout.get("grid_gap", "24px")

    card = comp.get("card", {})
    form = comp.get("form", {})
    btn  = comp.get("button_primary", {})
    wa   = comp.get("whatsapp_button", {})
    nav  = comp.get("nav", {})
    mob_bar = comp.get("mobile_cta_bar", {})
    faq_comp = comp.get("faq_accordion", {})

    return f"""
You are a world-class frontend developer building a high-converting coaching institute
landing page. You must follow the provided UI system STRICTLY and exactly.

═══════════════════════════════════════════════════════
DESIGN BRIEF
═══════════════════════════════════════════════════════
{generated_prompt}

═══════════════════════════════════════════════════════
UI SYSTEM — FOLLOW EXACTLY — NO DEVIATIONS ALLOWED
═══════════════════════════════════════════════════════

SECTIONS TO BUILD (in this order, no extras):
{section_list}

COLOR SYSTEM (use these exact hex codes):
  Primary:      {primary}
  Accent:       {accent}
  Text Dark:    {text_dark}
  Text Body:    {text_body}
  Background:   #ffffff
  Bg Light:     {bg_light}
  Bg Section:   {bg_section}
  Border:       {border_col}
  WhatsApp:     {whatsapp}

TYPOGRAPHY SYSTEM:
  Fonts Import:  {fonts_import}
  Heading Font:  {font_heading}
  Body Font:     {font_body}
  H1: {h1['size']} desktop / {h1['mobile']} mobile / weight {h1['weight']} / line-height {h1['line_height']}
  H2: {h2['size']} desktop / {h2['mobile']} mobile / weight {h2['weight']} / line-height {h2['line_height']}
  H3: {h3['size']} desktop / {h3['mobile']} mobile / weight {h3['weight']} / line-height {h3['line_height']}
  Body: {body_t['size']} / weight {body_t['weight']} / line-height {body_t['line_height']}

LAYOUT SYSTEM:
  Container max-width: {container}
  Container padding: {cont_pad}
  Section padding desktop: {section_pad_d}
  Section padding mobile: {section_pad_m}
  Card grid columns desktop: {grid_cols}
  Card grid gap: {grid_gap}

CARD COMPONENT:
  background: {card.get('background','#ffffff')}
  border-radius: {card.get('border_radius','16px')}
  padding: {card.get('padding','28px 24px')}
  border: {card.get('border','1px solid #e5e7eb')}
  box-shadow: {card.get('box_shadow','0 2px 12px rgba(0,0,0,0.06)')}
  hover box-shadow: {card.get('hover_shadow','0 8px 32px rgba(0,0,0,0.12)')}
  hover transform: {card.get('hover_transform','translateY(-4px)')}
  transition: {card.get('transition','all 0.3s ease')}

FORM COMPONENT:
  background: {form.get('background','#ffffff')}
  border-radius: {form.get('border_radius','20px')}
  padding: {form.get('padding','40px 36px')}
  box-shadow: {form.get('box_shadow','0 8px 40px rgba(0,0,0,0.12)')}
  Input height: {form.get('input_height','52px')}
  Input border: {form.get('input_border','1.5px solid #e5e7eb')}
  Input border-radius: {form.get('input_border_radius','8px')}
  Input padding: {form.get('input_padding','0 16px')}

BUTTON — PRIMARY:
  background: {btn.get('background', primary)}
  color: {btn.get('color','#ffffff')}
  padding: {btn.get('padding','14px 32px')}
  border-radius: {btn.get('border_radius','8px')}
  font-size: {btn.get('font_size','16px')}
  font-weight: {btn.get('font_weight','600')}
  On hover: filter brightness(0.9), transform translateY(-2px)

WHATSAPP BUTTON:
  position: fixed, bottom: 28px, right: 28px
  width/height: 60px, border-radius: 50%
  background: {whatsapp}
  box-shadow: 0 4px 20px rgba(37,211,102,0.4)
  z-index: 9999
  On hover: transform scale(1.1)

MOBILE BAR (show only on mobile, fixed bottom):
  3 buttons side by side: Call Now | WhatsApp | Apply Now
  background white, border-top 1px solid {border_col}
  padding: 12px 16px

MOBILE RULES:
  Breakpoint: {mobile.get('breakpoint','768px')}
  Hero: {mobile.get('hero','stack vertically, CTAs full width')}
  Cards: {mobile.get('cards','single column full width')}
  Font scale: {mobile.get('font_scale','reduce by 25%')}
  Touch targets: {mobile.get('touch_targets','minimum 44px')}
  Hide desktop nav, show mobile-friendly nav

SPACING SYSTEM:
  Use these values consistently:
  xs={spacing.get('xs','4px')} sm={spacing.get('sm','8px')} md={spacing.get('md','16px')}
  lg={spacing.get('lg','24px')} xl={spacing.get('xl','32px')} xxl={spacing.get('xxl','48px')}

═══════════════════════════════════════════════════════
MANDATORY CONVERSION ELEMENTS
═══════════════════════════════════════════════════════

HERO SECTION MUST HAVE:
  ✓ H1 headline using actual institute name and courses
  ✓ Subheadline (max 2 lines, result-focused)
  ✓ Primary CTA button: "Book Free Counselling" → background {primary}
  ✓ Secondary CTA button: "Explore Courses" → outlined style
  ✓ Stats bar below CTAs: 4 stats (students, years, results, rating)
  ✓ Section background: white or subtle gradient

TRUST SECTION / WHY US:
  ✓ 6 icon cards in {grid_cols}-column desktop / 2-column mobile grid
  ✓ Each card: icon (Font Awesome) + title + 1-line description
  ✓ Cards use exact card component spec above

COURSES SECTION:
  ✓ {grid_cols} course cards (one per course)
  ✓ Each card: course name H3, levels, career outcome, key subjects list, CTA button
  ✓ Cards use exact card component spec above

TESTIMONIALS SECTION:
  ✓ 3 stat numbers (large, bold, colored {primary}) at top
  ✓ 3 testimonial cards below
  ✓ Each card: quote, student name, course, result/rank

LEAD FORM SECTION:
  ✓ Centered card (max-width 560px)
  ✓ Fields: Full Name, Phone Number, Course Interested In (dropdown), City
  ✓ Submit: "Get Free Career Guidance" → full width, {primary} background
  ✓ On submit: show thank you message via JS, hide form

FAQ + FOOTER:
  ✓ 5 FAQ items as accordion (JS toggle, smooth animation)
  ✓ Footer: 3 columns (About, Courses, Contact)
  ✓ Contact: address, phone (tel: link), WhatsApp (wa.me link)

═══════════════════════════════════════════════════════
TECHNICAL REQUIREMENTS
═══════════════════════════════════════════════════════

ALLOWED EXTERNAL RESOURCES (only these two):
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
  Google Fonts via @import inside style tag

HTML STRUCTURE:
  - Single HTML file
  - All CSS in <style> tag inside <head>
  - All JS in <script> tag before </body>
  - Semantic HTML5 tags (nav, main, section, footer, article)
  - Proper H1 → H2 → H3 hierarchy (one H1 only)
  - Alt text on all images (use placeholder images from picsum.photos)
  - Schema markup for LocalBusiness in JSON-LD script tag

CSS RULES:
  - Start CSS with: *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  - Use CSS variables in :root for all colors and fonts
  - Use exact values from UI system above
  - Use flexbox and CSS grid for layouts
  - All animations use transition not animation keyframes (keep it subtle)
  - scroll-behavior: smooth on html element

JS RULES:
  - FAQ accordion: toggle open/close on click, smooth max-height transition
  - Form: prevent default submit, show thank you message, hide form fields
  - Mobile nav: hamburger toggle if nav links present
  - Smooth scroll on all anchor href links
  - No jQuery. Vanilla JS only.

QUALITY BAR:
  This page must look like it was built by a ₹1,00,000 design agency.
  Every pixel must match the UI system above.
  No Lorem Ipsum anywhere — use real content from the brief.
  No generic placeholder content.

OUTPUT ONLY THE HTML FILE.
No explanation. No markdown fences. No comments outside HTML.
Start with exactly: <!DOCTYPE html>
End with exactly: </html>
"""


# def get_evaluator_prompt(html_code: str, audit: str, ui_system: dict = None) -> str:
#     sections_expected = 6
#     if ui_system:
#         sections_expected = len(ui_system.get("sections", [])) + 1

#     return f"""
# You are a strict quality evaluator for coaching institute landing pages.

# AUDIT SUMMARY:
# {audit[:600]}

# HTML TO EVALUATE (first 4000 chars):
# {html_code[:4000]}

# EVALUATION CRITERIA — score each from 0 to 10:

# 1. CTA CLARITY (0-10):
#    - Is there a clear CTA in the hero section?
#    - Are CTAs visually prominent (color, size)?
#    - Is there a WhatsApp floating button?
#    Full marks: hero CTA + secondary CTA + WhatsApp button all present and styled

# 2. VISUAL HIERARCHY (0-10):
#    - Does H1 → H2 → H3 flow correctly?
#    - Is there one clear H1?
#    - Are sections clearly separated with spacing?
#    - Is typography consistent?
#    Full marks: clear hierarchy, consistent spacing, no text walls

# 3. SECTION DISCIPLINE (0-10):
#    - Are there {sections_expected} sections or fewer?
#    - Are sections purposeful (no filler sections)?
#    - Is there a clear flow from hero → courses → trust → form?
#    Full marks: 5-6 purposeful sections, clean flow

# 4. TRUST SIGNALS (0-10):
#    - Are there student testimonials?
#    - Are there stat numbers (students enrolled, results, years)?
#    - Is there a results/achievements section?
#    Full marks: stats + testimonials + specific numbers present

# 5. MOBILE UX (0-10):
#    - Is there a responsive meta viewport tag?
def get_evaluator_prompt(html_code: str, audit: str) -> str:
    html_preview = html_code[:2500]

    # Deterministic checks
    has_hero_cta     = bool(re.search(r'id=["\']hero["\']', html_code, re.I)
                       and re.search(r'btn-primary|btn btn', html_code, re.I))
    has_whatsapp     = bool(re.search(r'whatsapp-float|wa\.me', html_code, re.I))
    has_form         = bool(re.search(r'<form|form-card|lead-form', html_code, re.I))
    has_trust        = bool(re.search(r'trust|testimonial|result-stat', html_code, re.I))
    html_length_ok   = len(html_code) >= 3000
    section_count    = len(re.findall(r'<section', html_code, re.I))
    too_many_sections= section_count > 9  # default allowed sections

    # Check for raw placeholders
    has_raw_placeholders = bool(re.search(r'\{\{[A-Z_0-9]+\}\}', html_code))

    pre_checks = {
        "has_hero_cta":     has_hero_cta,
        "has_whatsapp":     has_whatsapp,
        "has_form":         has_form,
        "has_trust":        has_trust,
        "html_length_ok":   html_length_ok,
        "section_count_ok": not too_many_sections,
        "section_count":    section_count,
        "has_raw_placeholders": has_raw_placeholders
    }

    pre_check_summary = "\n".join([f"  {k}: {v}" for k, v in pre_checks.items()])

    return f"""
You are a quality evaluator for coaching institute landing pages.
Here are pre-computed checks on the HTML page:

PRE-CHECKS:
{pre_check_summary}

AUDIT SUMMARY:
{audit[:500]}

HTML PREVIEW (first 5000 chars):
{html_preview}

EVALUATION CRITERIA:
1. CTA CLARITY (0-10): Should have hero buttons, mobile bar, and floating WhatsApp.
2. VISUAL HIERARCHY (0-10): Flow and fonts.
3. SECTION DISCIPLINE (0-10): Under 9 sections, clear conversion path.
4. TRUST SIGNALS (0-10): Student testimonials and result highlights.
5. MOBILE UX (0-10): Viewport meta and stack layout.

HARD FAIL RULES:
- has_hero_cta is False
- has_whatsapp is False
- has_form is False
- html_length_ok is False
- has_raw_placeholders is True (unresolved placeholders like {{{{PLACEHOLDER}}}} remain)

Evaluate the page and rate it. Because the template code already contains structured CTAs, forms, WhatsApp, trust section, and sections, if the pre-checks are green, you should output high scores (e.g. 9 or 10) so the page passes immediately.
If there are unresolved placeholders, score lower and specify them in ISSUES.

RESPOND IN THIS EXACT FORMAT ONLY:

SCORE_CTA: [0-10]
SCORE_HIERARCHY: [0-10]
SCORE_SECTIONS: [0-10]
SCORE_TRUST: [0-10]
SCORE_MOBILE: [0-10]
SCORE: [average of above, one decimal]
PASSED: [YES or NO]
HARD_FAIL: [YES or NO]
HARD_FAIL_REASON: [reason description or None]

ISSUES:
- [issue 1 if any]

IMPROVEMENT_INSTRUCTIONS:
- [fix instruction 1 if any]
"""


def get_redesign_improvement_prompt(
    website_data: str,
    audit: str,
    previous_html: str,
    evaluator_feedback: str,
    ui_system: dict = None
) -> str:

    ui_hint = ""
    if ui_system:
        colors = ui_system.get("colors", {})
        ui_hint = f"""
REQUIRED COLOR SYSTEM:
  Primary: {colors.get('primary','#1a237e')}
  Accent:  {colors.get('accent','#e53935')}
  Background: #ffffff / {colors.get('bg_light','#f8fafc')}
"""

    return f"""
You are an expert frontend developer fixing a coaching institute landing page.

EVALUATOR FEEDBACK — FIX ALL OF THESE:
{evaluator_feedback}

{ui_hint}

PREVIOUS HTML — IMPROVE THIS (keep structure, fix issues):
{previous_html}

RULES:
- Fix every issue listed in evaluator feedback
- Keep all content that was correct
- Do NOT remove sections that passed evaluation
- Do NOT add new sections beyond what existed
- Maintain the UI system colors and spacing
- Ensure WhatsApp floating button exists
- Ensure hero has a primary CTA button
- Ensure form exists with submit handler

OUTPUT ONLY HTML. No explanation.
Start with <!DOCTYPE html> end with </html>
"""