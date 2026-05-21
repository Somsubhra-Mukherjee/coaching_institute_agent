import json
import re
from backend.utils.ollama_client import call_audit_model


def build_ui_system_prompt(generated_prompt: str, audit: str) -> str:
    return f"""
You are a senior UI architect specializing in high-converting Indian coaching institute websites.

REDESIGN BRIEF:
{generated_prompt[:2000]}

AUDIT FINDINGS:
{audit[:800]}

YOUR TASK:
Convert this brief into a strict, structured UI system specification.
Do NOT generate any HTML or CSS.
Output ONLY a valid JSON object. Nothing else. No explanation. No markdown.

The JSON must follow this EXACT structure:

{{
  "sections": [
    {{
      "id": "hero",
      "name": "Hero Section",
      "priority": 1,
      "goal": "Capture attention and drive CTA clicks",
      "required_elements": ["headline", "subheadline", "primary_cta", "secondary_cta", "trust_stats"],
      "layout": "full-width, centered content, max-width 900px",
      "background": "#FFFFFF",
      "remove_if_present": ["slider", "carousel", "video_autoplay"]
    }}
  ],
  "layout": {{
    "container_max_width": "1200px",
    "container_padding": "0 24px",
    "section_padding_desktop": "80px 0",
    "section_padding_mobile": "48px 0",
    "grid_columns_desktop": 3,
    "grid_columns_mobile": 1,
    "grid_gap": "24px"
  }},
  "typography": {{
    "font_family_heading": "Inter, sans-serif",
    "font_family_body": "Inter, sans-serif",
    "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');",
    "scale": {{
      "h1": {{"size": "48px", "mobile": "32px", "weight": "800", "line_height": "1.15"}},
      "h2": {{"size": "36px", "mobile": "26px", "weight": "700", "line_height": "1.25"}},
      "h3": {{"size": "22px", "mobile": "18px", "weight": "600", "line_height": "1.35"}},
      "body": {{"size": "16px", "mobile": "15px", "weight": "400", "line_height": "1.7"}},
      "small": {{"size": "13px", "mobile": "12px", "weight": "400", "line_height": "1.5"}},
      "label": {{"size": "12px", "mobile": "11px", "weight": "600", "line_height": "1.4"}}
    }}
  }},
  "colors": {{
    "primary": "#1a237e",
    "primary_dark": "#0d1257",
    "primary_light": "#e8eaf6",
    "accent": "#e53935",
    "accent_light": "#ffebee",
    "text_dark": "#1a1a2e",
    "text_body": "#374151",
    "text_muted": "#6b7280",
    "text_light": "#9ca3af",
    "bg_white": "#ffffff",
    "bg_light": "#f8fafc",
    "bg_section": "#f1f5f9",
    "border": "#e5e7eb",
    "success": "#16a34a",
    "whatsapp": "#25d366"
  }},
  "components": {{
    "button_primary": {{
      "background": "primary color",
      "color": "#ffffff",
      "padding": "14px 32px",
      "border_radius": "8px",
      "font_size": "16px",
      "font_weight": "600",
      "border": "none",
      "hover": "darken background by 10%, lift with box-shadow",
      "mobile_padding": "14px 24px",
      "mobile_width": "100%"
    }},
    "button_secondary": {{
      "background": "transparent",
      "color": "primary color",
      "padding": "13px 30px",
      "border_radius": "8px",
      "font_size": "16px",
      "font_weight": "600",
      "border": "2px solid primary color",
      "hover": "fill with primary color, text white",
      "mobile_width": "100%"
    }},
    "card": {{
      "background": "#ffffff",
      "border_radius": "16px",
      "padding": "28px 24px",
      "border": "1px solid #e5e7eb",
      "box_shadow": "0 2px 12px rgba(0,0,0,0.06)",
      "hover_shadow": "0 8px 32px rgba(0,0,0,0.12)",
      "hover_transform": "translateY(-4px)",
      "transition": "all 0.3s ease"
    }},
    "stat_card": {{
      "background": "primary_light or white",
      "border_radius": "12px",
      "padding": "24px 20px",
      "text_align": "center",
      "number_size": "40px",
      "number_weight": "800",
      "number_color": "primary",
      "label_size": "13px",
      "label_color": "text_muted"
    }},
    "testimonial_card": {{
      "background": "#ffffff",
      "border_radius": "16px",
      "padding": "28px",
      "border_left": "4px solid accent color",
      "box_shadow": "0 4px 20px rgba(0,0,0,0.08)",
      "quote_size": "15px",
      "name_size": "14px",
      "name_weight": "700",
      "role_size": "12px",
      "role_color": "text_muted"
    }},
    "form": {{
      "background": "#ffffff",
      "border_radius": "20px",
      "padding": "40px 36px",
      "box_shadow": "0 8px 40px rgba(0,0,0,0.12)",
      "input_height": "52px",
      "input_border_radius": "8px",
      "input_border": "1.5px solid #e5e7eb",
      "input_focus_border": "primary color",
      "input_padding": "0 16px",
      "input_font_size": "15px",
      "label_size": "13px",
      "label_weight": "600",
      "label_color": "text_body",
      "gap_between_fields": "20px"
    }},
    "nav": {{
      "position": "sticky",
      "top": "0",
      "background": "#ffffff",
      "box_shadow": "0 2px 20px rgba(0,0,0,0.08)",
      "height": "70px",
      "z_index": "1000",
      "logo_size": "22px",
      "logo_weight": "800",
      "link_size": "14px",
      "link_weight": "500",
      "link_color": "text_body",
      "cta_button": "button_primary style, smaller padding 10px 20px"
    }},
    "whatsapp_button": {{
      "position": "fixed",
      "bottom": "28px",
      "right": "28px",
      "size": "60px",
      "background": "#25d366",
      "border_radius": "50%",
      "icon_size": "28px",
      "z_index": "9999",
      "box_shadow": "0 4px 20px rgba(37,211,102,0.4)",
      "hover_scale": "1.1"
    }},
    "mobile_cta_bar": {{
      "display": "none on desktop, flex on mobile",
      "position": "fixed",
      "bottom": "0",
      "width": "100%",
      "background": "#ffffff",
      "border_top": "1px solid #e5e7eb",
      "padding": "12px 16px",
      "gap": "8px",
      "z_index": "999",
      "buttons": ["Call Now", "WhatsApp", "Apply Now"]
    }},
    "faq_accordion": {{
      "border_radius": "12px",
      "border": "1px solid #e5e7eb",
      "question_padding": "20px 24px",
      "answer_padding": "0 24px 20px",
      "question_font_size": "16px",
      "question_font_weight": "600",
      "answer_font_size": "15px",
      "answer_color": "text_body",
      "icon": "plus/minus toggle",
      "animation": "smooth height transition"
    }}
  }},
  "spacing_system": {{
    "base": "8px",
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px",
    "section_gap": "80px",
    "card_gap": "24px",
    "element_gap": "16px",
    "text_gap": "12px"
  }},
  "mobile_rules": {{
    "breakpoint": "768px",
    "nav": "hamburger menu, logo left, CTA right",
    "hero": "stack vertically, headline 32px, CTAs full width stacked",
    "stats": "2x2 grid",
    "cards": "single column, full width",
    "form": "full width, reduced padding 24px",
    "font_scale": "reduce all sizes by 25-30%",
    "touch_targets": "minimum 44px height for all buttons",
    "sticky_bar": "show mobile CTA bar fixed at bottom",
    "hide_on_mobile": ["faculty photos large", "decorative elements"]
  }}
}}

IMPORTANT RULES:
1. Replace all color values with actual hex codes matching the institute branding
2. Include only 5-6 sections maximum in the sections array
3. Keep all section goals conversion-focused
4. Every value must be a concrete CSS value, not a vague description
5. The sections array must include these IDs in order:
   nav, hero, trust_signals, courses, testimonials, lead_form, faq_footer
   (pick max 6 of these)
6. Output ONLY the JSON. Zero other text.
"""


def parse_ui_system(response: str) -> dict:
    """
    Extract and parse JSON from model response.
    Returns parsed dict or fallback default system.
    """
    # Try direct parse first
    try:
        return json.loads(response.strip())
    except Exception:
        pass

    # Try extracting JSON block from response
    try:
        match = re.search(r'\{[\s\S]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    print("[UI SYSTEM AGENT] JSON parse failed — using default system")
    return get_default_ui_system()


def get_default_ui_system() -> dict:
    """
    Hardcoded fallback UI system used when model fails to return valid JSON.
    This ensures the redesign agent always has a design system to follow.
    """
    return {
        "sections": [
            {
                "id": "nav",
                "name": "Navigation",
                "priority": 1,
                "goal": "Quick access and trust",
                "required_elements": ["logo", "nav_links", "phone_number", "cta_button"],
                "layout": "sticky, space-between, height 70px"
            },
            {
                "id": "hero",
                "name": "Hero Section",
                "priority": 2,
                "goal": "Capture attention and drive enquiries",
                "required_elements": ["h1_headline", "subheadline", "primary_cta", "secondary_cta", "stat_bar"],
                "layout": "centered, max-width 860px, padding 100px 0"
            },
            {
                "id": "courses",
                "name": "Courses Section",
                "priority": 3,
                "goal": "Show offerings clearly",
                "required_elements": ["course_cards", "levels", "career_outcome", "get_syllabus_cta"],
                "layout": "3 column grid desktop, 1 column mobile"
            },
            {
                "id": "testimonials",
                "name": "Results and Testimonials",
                "priority": 4,
                "goal": "Build trust with social proof",
                "required_elements": ["stat_numbers", "student_cards", "parent_quotes"],
                "layout": "stats row + 3 column card grid"
            },
            {
                "id": "lead_form",
                "name": "Lead Capture Form",
                "priority": 5,
                "goal": "Generate enquiries",
                "required_elements": ["name_field", "phone_field", "course_dropdown", "city_field", "submit_cta"],
                "layout": "centered card, max-width 560px"
            },
            {
                "id": "faq_footer",
                "name": "FAQ and Footer",
                "priority": 6,
                "goal": "Answer objections and provide contact",
                "required_elements": ["faq_accordion", "address", "phone", "whatsapp_link", "social_links"],
                "layout": "accordion + 3 column footer grid"
            }
        ],
        "layout": {
            "container_max_width": "1200px",
            "container_padding": "0 24px",
            "section_padding_desktop": "80px 0",
            "section_padding_mobile": "48px 0",
            "grid_columns_desktop": 3,
            "grid_columns_mobile": 1,
            "grid_gap": "24px"
        },
        "typography": {
            "font_family_heading": "Inter, sans-serif",
            "font_family_body": "Inter, sans-serif",
            "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');",
            "scale": {
                "h1": {"size": "48px", "mobile": "32px", "weight": "800", "line_height": "1.15"},
                "h2": {"size": "36px", "mobile": "26px", "weight": "700", "line_height": "1.25"},
                "h3": {"size": "22px", "mobile": "18px", "weight": "600", "line_height": "1.35"},
                "body": {"size": "16px", "mobile": "15px", "weight": "400", "line_height": "1.7"},
                "small": {"size": "13px", "mobile": "12px", "weight": "400", "line_height": "1.5"},
                "label": {"size": "12px", "mobile": "11px", "weight": "600", "line_height": "1.4"}
            }
        },
        "colors": {
            "primary": "#1a237e",
            "primary_dark": "#0d1257",
            "primary_light": "#e8eaf6",
            "accent": "#e53935",
            "accent_light": "#ffebee",
            "text_dark": "#1a1a2e",
            "text_body": "#374151",
            "text_muted": "#6b7280",
            "bg_white": "#ffffff",
            "bg_light": "#f8fafc",
            "bg_section": "#f1f5f9",
            "border": "#e5e7eb",
            "success": "#16a34a",
            "whatsapp": "#25d366"
        },
        "components": {
            "button_primary": {
                "background": "#1a237e",
                "color": "#ffffff",
                "padding": "14px 32px",
                "border_radius": "8px",
                "font_size": "16px",
                "font_weight": "600"
            },
            "card": {
                "background": "#ffffff",
                "border_radius": "16px",
                "padding": "28px 24px",
                "border": "1px solid #e5e7eb",
                "box_shadow": "0 2px 12px rgba(0,0,0,0.06)",
                "hover_shadow": "0 8px 32px rgba(0,0,0,0.12)",
                "hover_transform": "translateY(-4px)",
                "transition": "all 0.3s ease"
            },
            "form": {
                "background": "#ffffff",
                "border_radius": "20px",
                "padding": "40px 36px",
                "box_shadow": "0 8px 40px rgba(0,0,0,0.12)",
                "input_height": "52px",
                "input_border_radius": "8px",
                "input_border": "1.5px solid #e5e7eb"
            },
            "whatsapp_button": {
                "position": "fixed",
                "bottom": "28px",
                "right": "28px",
                "size": "60px",
                "background": "#25d366",
                "border_radius": "50%"
            }
        },
        "spacing_system": {
            "base": "8px",
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "xxl": "48px",
            "section_gap": "80px",
            "card_gap": "24px",
            "element_gap": "16px",
            "text_gap": "12px"
        },
        "mobile_rules": {
            "breakpoint": "768px",
            "hero": "stack vertically, CTAs full width",
            "cards": "single column full width",
            "font_scale": "reduce all sizes by 25%",
            "touch_targets": "minimum 44px height",
            "sticky_bar": "show mobile CTA bar fixed at bottom"
        }
    }


def run_ui_system_agent(generated_prompt: str, audit: str) -> dict:
    """
    Main entry point for ui_system_agent.
    Returns a parsed UI system dict.
    """
    print("\n[UI SYSTEM AGENT] Generating UI system specification...")

    try:
        prompt = build_ui_system_prompt(generated_prompt, audit)
        system = (
            "You are a UI system architect. "
            "You output ONLY valid JSON. "
            "No explanations. No markdown. "
            "Just the raw JSON object."
        )
        response = call_audit_model(prompt, system)
        ui_system = parse_ui_system(response)
        print(f"[UI SYSTEM AGENT] UI system generated with {len(ui_system.get('sections', []))} sections")
        return ui_system

    except Exception as e:
        print(f"[UI SYSTEM AGENT] ERROR: {e} — using default system")
        return get_default_ui_system()