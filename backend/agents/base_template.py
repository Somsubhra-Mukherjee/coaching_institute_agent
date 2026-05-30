BASE_TEMPLATE_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{{META_TITLE}}</title>
<meta name="description" content="{{META_DESCRIPTION}}"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<style>
{{GOOGLE_FONTS_IMPORT}}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}

:root{
  --primary:       {{COLOR_PRIMARY}};
  --primary-dark:  {{COLOR_PRIMARY_DARK}};
  --primary-light: {{COLOR_PRIMARY_LIGHT}};
  --accent:        {{COLOR_ACCENT}};
  --accent-light:  {{COLOR_ACCENT_LIGHT}};
  --text-dark:     {{COLOR_TEXT_DARK}};
  --text-body:     {{COLOR_TEXT_BODY}};
  --text-muted:    {{COLOR_TEXT_MUTED}};
  --bg-white:      #ffffff;
  --bg-light:      {{COLOR_BG_LIGHT}};
  --bg-section:    {{COLOR_BG_SECTION}};
  --border:        {{COLOR_BORDER}};
  --success:       #16a34a;
  --whatsapp:      #25d366;
  --radius-sm:     8px;
  --radius-md:     12px;
  --radius-lg:     16px;
  --radius-xl:     20px;
  --shadow-sm:     0 2px 8px rgba(0,0,0,0.06);
  --shadow-md:     0 4px 20px rgba(0,0,0,0.10);
  --shadow-lg:     0 8px 40px rgba(0,0,0,0.14);
  --shadow-hover:  0 12px 48px rgba(0,0,0,0.18);
  --transition:    all 0.3s ease;
  --font-heading:  {{FONT_HEADING}};
  --font-body:     {{FONT_BODY}};
  --container:     1200px;
}

body{
  font-family: var(--font-body);
  color: var(--text-body);
  background: var(--bg-white);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}

img{max-width:100%;height:auto;display:block}
a{text-decoration:none;color:inherit}
ul{list-style:none}
button{cursor:pointer;border:none;outline:none;font-family:inherit}
input,select,textarea{font-family:inherit;outline:none}

/* ── UTILITIES ─────────────────────────────────────── */
.container{max-width:var(--container);margin:0 auto;padding:0 24px}
.section{padding:80px 0}
.section-alt{background:var(--bg-light)}
.section-dark{background:var(--primary);color:#fff}

.section-header{text-align:center;margin-bottom:56px}
.section-header h2{
  font-family:var(--font-heading);
  font-size:36px;font-weight:700;
  color:var(--text-dark);line-height:1.25;
  margin-bottom:14px
}
.section-header p{
  font-size:17px;color:var(--text-muted);
  max-width:560px;margin:0 auto;line-height:1.7
}
.section-dark .section-header h2{color:#fff}
.section-dark .section-header p{color:rgba(255,255,255,0.75)}

.tag{
  display:inline-flex;align-items:center;gap:6px;
  font-size:13px;font-weight:600;letter-spacing:0.4px;
  color:var(--primary);background:var(--primary-light);
  padding:6px 14px;border-radius:99px;margin-bottom:16px
}

/* ── BUTTONS ────────────────────────────────────────── */
.btn{
  display:inline-flex;align-items:center;justify-content:center;
  gap:8px;font-size:16px;font-weight:600;
  padding:14px 32px;border-radius:var(--radius-sm);
  transition:var(--transition);cursor:pointer;border:none;
  font-family:var(--font-body)
}
.btn-primary{
  background:var(--primary);color:#fff;
  box-shadow:0 4px 16px rgba(0,0,0,0.15)
}
.btn-primary:hover{
  background:var(--primary-dark);
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(0,0,0,0.2)
}
.btn-outline{
  background:transparent;color:var(--primary);
  border:2px solid var(--primary)
}
.btn-outline:hover{
  background:var(--primary);color:#fff;
  transform:translateY(-2px)
}
.btn-accent{
  background:var(--accent);color:#fff;
  box-shadow:0 4px 16px rgba(0,0,0,0.15)
}
.btn-accent:hover{
  filter:brightness(0.9);transform:translateY(-2px)
}
.btn-lg{padding:17px 40px;font-size:17px}
.btn-sm{padding:10px 22px;font-size:14px}
.btn-full{width:100%}

/* ── CARDS ──────────────────────────────────────────── */
.card{
  background:var(--bg-white);
  border-radius:var(--radius-lg);
  padding:28px 24px;
  border:1px solid var(--border);
  box-shadow:var(--shadow-sm);
  transition:var(--transition)
}
.card:hover{
  box-shadow:var(--shadow-hover);
  transform:translateY(-4px)
}

/* ── GRID ───────────────────────────────────────────── */
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}

/* ══════════════════════════════════════════════════════
   SECTION 1 — NAVIGATION
═══════════════════════════════════════════════════════ */
#nav{
  position:sticky;top:0;z-index:1000;
  background:#fff;
  box-shadow:0 2px 20px rgba(0,0,0,0.08);
  height:70px;
}
.nav-inner{
  display:flex;align-items:center;
  justify-content:space-between;
  height:70px
}
.nav-logo{
  display:flex;align-items:center;gap:10px
}
.nav-logo-icon{
  width:38px;height:38px;
  background:var(--primary);
  border-radius:var(--radius-sm);
  display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:18px;font-weight:800
}
.nav-logo-text{
  font-family:var(--font-heading);
  font-size:20px;font-weight:800;color:var(--text-dark)
}
.nav-logo-text span{color:var(--primary)}
.nav-links{display:flex;align-items:center;gap:8px}
.nav-links a{
  font-size:14px;font-weight:500;color:var(--text-body);
  padding:8px 14px;border-radius:var(--radius-sm);
  transition:var(--transition)
}
.nav-links a:hover{color:var(--primary);background:var(--primary-light)}
.nav-right{display:flex;align-items:center;gap:12px}
.nav-phone{
  display:flex;align-items:center;gap:6px;
  font-size:14px;font-weight:600;color:var(--text-dark)
}
.nav-phone i{color:var(--primary)}
.nav-hamburger{
  display:none;flex-direction:column;gap:5px;
  background:none;border:none;cursor:pointer;padding:4px
}
.nav-hamburger span{
  display:block;width:24px;height:2px;
  background:var(--text-dark);border-radius:2px;
  transition:var(--transition)
}
.mobile-menu{
  display:none;position:fixed;top:70px;left:0;right:0;
  background:#fff;border-top:1px solid var(--border);
  padding:20px 24px;z-index:999;
  box-shadow:var(--shadow-md)
}
.mobile-menu.open{display:block}
.mobile-menu a{
  display:block;padding:12px 0;
  font-size:15px;font-weight:500;
  color:var(--text-body);
  border-bottom:1px solid var(--border)
}
.mobile-menu a:hover{color:var(--primary)}
.mobile-menu .btn{margin-top:16px;width:100%}

/* ══════════════════════════════════════════════════════
   SECTION 2 — HERO
═══════════════════════════════════════════════════════ */
#hero{
  padding:100px 0 80px;
  background:linear-gradient(135deg, var(--bg-white) 0%, var(--bg-light) 100%);
  position:relative;overflow:hidden
}
#hero::before{
  content:'';position:absolute;
  top:-100px;right:-100px;
  width:500px;height:500px;
  background:var(--primary-light);
  border-radius:50%;opacity:0.4;
  pointer-events:none
}
.hero-inner{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:60px;align-items:center
}
.hero-content{position:relative;z-index:1}
.hero-content .tag{margin-bottom:20px}
.hero-content h1{
  font-family:var(--font-heading);
  font-size:48px;font-weight:800;
  color:var(--text-dark);line-height:1.15;
  margin-bottom:20px
}
.hero-content h1 span{color:var(--primary)}
.hero-content p{
  font-size:18px;color:var(--text-muted);
  line-height:1.7;margin-bottom:32px;
  max-width:520px
}
.hero-cta{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:40px}
.hero-stats{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:16px;margin-top:8px
}
.hero-stat{
  text-align:center;
  background:#fff;
  border-radius:var(--radius-md);
  padding:16px 12px;
  border:1px solid var(--border);
  box-shadow:var(--shadow-sm)
}
.hero-stat-num{
  font-family:var(--font-heading);
  font-size:28px;font-weight:800;
  color:var(--primary);line-height:1
}
.hero-stat-label{
  font-size:12px;color:var(--text-muted);
  margin-top:6px;font-weight:500
}
.hero-image{
  position:relative;z-index:1
}
.hero-image-main{
  width:100%;border-radius:var(--radius-xl);
  box-shadow:var(--shadow-lg);
  aspect-ratio:4/3;object-fit:cover;
  background:var(--bg-section)
}
.hero-image-badge{
  position:absolute;bottom:-20px;left:-20px;
  background:#fff;border-radius:var(--radius-md);
  padding:16px 20px;
  box-shadow:var(--shadow-md);
  display:flex;align-items:center;gap:12px
}
.hero-image-badge i{font-size:24px;color:var(--primary)}
.hero-image-badge strong{
  display:block;font-size:16px;
  font-weight:700;color:var(--text-dark)
}
.hero-image-badge span{font-size:12px;color:var(--text-muted)}

/* ══════════════════════════════════════════════════════
   SECTION 3 — WHY US / TRUST
═══════════════════════════════════════════════════════ */
#trust{padding:80px 0;background:var(--bg-white)}
.trust-cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:24px
}
.trust-card{
  background:var(--bg-white);
  border-radius:var(--radius-lg);
  padding:28px 24px;
  border:1px solid var(--border);
  box-shadow:var(--shadow-sm);
  transition:var(--transition)
}
.trust-card:hover{
  box-shadow:var(--shadow-hover);
  transform:translateY(-4px);
  border-color:var(--primary)
}
.trust-icon{
  width:56px;height:56px;
  background:var(--primary-light);
  border-radius:var(--radius-md);
  display:flex;align-items:center;justify-content:center;
  margin-bottom:20px
}
.trust-icon i{font-size:24px;color:var(--primary)}
.trust-card h3{
  font-size:17px;font-weight:700;
  color:var(--text-dark);margin-bottom:10px
}
.trust-card p{
  font-size:14px;color:var(--text-muted);line-height:1.65
}

/* ══════════════════════════════════════════════════════
   SECTION 4 — COURSES
═══════════════════════════════════════════════════════ */
#courses{padding:80px 0;background:var(--bg-light)}
.course-cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:28px
}
.course-card{
  background:var(--bg-white);
  border-radius:var(--radius-xl);
  overflow:hidden;
  border:1px solid var(--border);
  box-shadow:var(--shadow-sm);
  transition:var(--transition);
  display:flex;flex-direction:column
}
.course-card:hover{
  box-shadow:var(--shadow-hover);
  transform:translateY(-4px)
}
.course-card-header{
  background:var(--primary);
  padding:28px 24px
}
.course-card-header h3{
  font-size:24px;font-weight:800;
  color:#fff;margin-bottom:6px
}
.course-card-header p{
  font-size:13px;color:rgba(255,255,255,0.8)
}
.course-card-body{padding:24px;flex:1;display:flex;flex-direction:column}
.course-levels{margin-bottom:16px}
.course-levels-label{
  font-size:12px;font-weight:700;
  color:var(--text-muted);
  text-transform:uppercase;letter-spacing:0.5px;
  margin-bottom:8px
}
.course-level-tags{display:flex;flex-wrap:wrap;gap:6px}
.course-level-tag{
  font-size:12px;font-weight:600;
  color:var(--primary);
  background:var(--primary-light);
  padding:4px 10px;border-radius:99px
}
.course-subjects{margin-bottom:20px}
.course-subjects-label{
  font-size:12px;font-weight:700;
  color:var(--text-muted);
  text-transform:uppercase;letter-spacing:0.5px;
  margin-bottom:8px
}
.course-subjects ul{display:flex;flex-direction:column;gap:6px}
.course-subjects ul li{
  display:flex;align-items:center;gap:8px;
  font-size:14px;color:var(--text-body)
}
.course-subjects ul li::before{
  content:'';width:6px;height:6px;
  background:var(--accent);border-radius:50%;flex-shrink:0
}
.course-outcome{
  font-size:13px;color:var(--text-muted);
  padding:12px;background:var(--bg-light);
  border-radius:var(--radius-sm);margin-bottom:20px;
  line-height:1.55
}
.course-outcome strong{color:var(--success)}
.course-card .btn{margin-top:auto}

/* ══════════════════════════════════════════════════════
   SECTION 5 — RESULTS / TESTIMONIALS
═══════════════════════════════════════════════════════ */
#results{padding:80px 0;background:var(--bg-white)}
.results-stats{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:20px;margin-bottom:56px
}
.result-stat{
  text-align:center;
  background:var(--bg-white);
  border-radius:var(--radius-lg);
  padding:28px 20px;
  border:1px solid var(--border);
  box-shadow:var(--shadow-sm)
}
.result-stat-num{
  font-family:var(--font-heading);
  font-size:44px;font-weight:800;
  color:var(--primary);line-height:1;
  margin-bottom:8px
}
.result-stat-label{
  font-size:14px;color:var(--text-muted);font-weight:500
}
.testimonial-cards{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:24px
}
.testimonial-card{
  background:var(--bg-white);
  border-radius:var(--radius-lg);
  padding:28px;
  border:1px solid var(--border);
  border-left:4px solid var(--accent);
  box-shadow:var(--shadow-sm);
  transition:var(--transition)
}
.testimonial-card:hover{box-shadow:var(--shadow-md)}
.testimonial-stars{
  display:flex;gap:4px;margin-bottom:14px
}
.testimonial-stars i{font-size:14px;color:#f59e0b}
.testimonial-text{
  font-size:15px;color:var(--text-body);
  line-height:1.7;margin-bottom:20px;
  font-style:italic
}
.testimonial-author{display:flex;align-items:center;gap:12px}
.testimonial-avatar{
  width:44px;height:44px;border-radius:50%;
  background:var(--primary-light);
  display:flex;align-items:center;justify-content:center;
  font-size:18px;font-weight:700;color:var(--primary);
  flex-shrink:0
}
.testimonial-name{
  font-size:15px;font-weight:700;
  color:var(--text-dark)
}
.testimonial-meta{font-size:12px;color:var(--text-muted);margin-top:2px}

/* ══════════════════════════════════════════════════════
   SECTION 6 — LEAD FORM
═══════════════════════════════════════════════════════ */
#lead-form{padding:80px 0;background:var(--bg-light)}
.lead-form-inner{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:60px;align-items:center
}
.lead-form-content h2{
  font-family:var(--font-heading);
  font-size:36px;font-weight:700;
  color:var(--text-dark);
  line-height:1.25;margin-bottom:16px
}
.lead-form-content p{
  font-size:16px;color:var(--text-muted);
  line-height:1.7;margin-bottom:28px
}
.lead-form-bullets{display:flex;flex-direction:column;gap:14px}
.lead-form-bullet{
  display:flex;align-items:center;gap:12px;
  font-size:15px;color:var(--text-body);font-weight:500
}
.lead-form-bullet i{
  width:32px;height:32px;
  background:var(--primary-light);
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:14px;color:var(--primary);flex-shrink:0
}
.form-card{
  background:#fff;
  border-radius:var(--radius-xl);
  padding:40px 36px;
  box-shadow:var(--shadow-lg);
  border:1px solid var(--border)
}
.form-card h3{
  font-size:22px;font-weight:700;
  color:var(--text-dark);
  margin-bottom:28px;text-align:center
}
.form-group{margin-bottom:20px}
.form-label{
  display:block;font-size:13px;
  font-weight:600;color:var(--text-body);
  margin-bottom:7px
}
.form-input{
  width:100%;height:52px;
  border:1.5px solid var(--border);
  border-radius:var(--radius-sm);
  padding:0 16px;font-size:15px;
  color:var(--text-dark);
  background:#fff;
  transition:var(--transition)
}
.form-input:focus{border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-light)}
.form-select{
  width:100%;height:52px;
  border:1.5px solid var(--border);
  border-radius:var(--radius-sm);
  padding:0 16px;font-size:15px;
  color:var(--text-dark);
  background:#fff;
  cursor:pointer;
  transition:var(--transition);
  appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat:no-repeat;
  background-position:right 16px center
}
.form-select:focus{border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-light)}
.form-submit{margin-top:8px}
.form-note{
  text-align:center;font-size:12px;
  color:var(--text-muted);margin-top:12px
}
.form-note i{color:var(--success);margin-right:4px}
.form-success{
  display:none;text-align:center;padding:20px
}
.form-success i{
  font-size:48px;color:var(--success);
  display:block;margin-bottom:16px
}
.form-success h3{
  font-size:22px;font-weight:700;
  color:var(--text-dark);margin-bottom:10px
}
.form-success p{font-size:15px;color:var(--text-muted)}

/* ══════════════════════════════════════════════════════
   SECTION 7 — FAQ
═══════════════════════════════════════════════════════ */
#faq{padding:80px 0;background:var(--bg-white)}
.faq-list{max-width:780px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
.faq-item{
  border:1px solid var(--border);
  border-radius:var(--radius-md);
  overflow:hidden;
  transition:var(--transition)
}
.faq-item.open{border-color:var(--primary)}
.faq-question{
  width:100%;display:flex;
  align-items:center;justify-content:space-between;
  padding:20px 24px;
  background:#fff;cursor:pointer;
  font-size:16px;font-weight:600;
  color:var(--text-dark);text-align:left;
  transition:var(--transition);gap:12px
}
.faq-question:hover{background:var(--bg-light);color:var(--primary)}
.faq-item.open .faq-question{
  background:var(--primary-light);color:var(--primary)
}
.faq-icon{
  width:28px;height:28px;
  border-radius:50%;
  background:var(--bg-light);
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;font-size:14px;
  color:var(--primary);
  transition:var(--transition)
}
.faq-item.open .faq-icon{
  background:var(--primary);color:#fff;transform:rotate(45deg)
}
.faq-answer{
  max-height:0;overflow:hidden;
  transition:max-height 0.35s ease,padding 0.35s ease
}
.faq-answer-inner{
  padding:0 24px 20px;
  font-size:15px;color:var(--text-muted);line-height:1.7
}
.faq-item.open .faq-answer{max-height:300px}

/* ══════════════════════════════════════════════════════
   SECTION 8 — FOOTER
═══════════════════════════════════════════════════════ */
#footer{background:var(--text-dark);color:#fff;padding:64px 0 0}
.footer-grid{
  display:grid;
  grid-template-columns:2fr 1fr 1fr 1.5fr;
  gap:40px;margin-bottom:40px
}
.footer-brand h3{
  font-family:var(--font-heading);
  font-size:20px;font-weight:800;
  margin-bottom:14px
}
.footer-brand h3 span{color:var(--accent)}
.footer-brand p{
  font-size:14px;color:rgba(255,255,255,0.6);
  line-height:1.7;margin-bottom:20px;max-width:280px
}
.footer-socials{display:flex;gap:10px}
.footer-social{
  width:36px;height:36px;
  background:rgba(255,255,255,0.1);
  border-radius:var(--radius-sm);
  display:flex;align-items:center;justify-content:center;
  font-size:15px;color:#fff;
  transition:var(--transition)
}
.footer-social:hover{background:var(--primary)}
.footer-col h4{
  font-size:14px;font-weight:700;
  margin-bottom:16px;color:#fff;
  text-transform:uppercase;letter-spacing:0.5px
}
.footer-col ul{display:flex;flex-direction:column;gap:10px}
.footer-col ul li a{
  font-size:14px;color:rgba(255,255,255,0.6);
  transition:var(--transition)
}
.footer-col ul li a:hover{color:#fff}
.footer-contact{display:flex;flex-direction:column;gap:14px}
.footer-contact-item{
  display:flex;align-items:flex-start;gap:10px;
  font-size:14px;color:rgba(255,255,255,0.7)
}
.footer-contact-item i{
  margin-top:2px;color:var(--accent);flex-shrink:0
}
.footer-contact-item a{color:rgba(255,255,255,0.7)}
.footer-contact-item a:hover{color:#fff}
.footer-bottom{
  border-top:1px solid rgba(255,255,255,0.1);
  padding:20px 0;margin-top:0;
  display:flex;align-items:center;
  justify-content:space-between;flex-wrap:wrap;gap:10px
}
.footer-bottom p{font-size:13px;color:rgba(255,255,255,0.45)}
.footer-bottom-links{display:flex;gap:20px}
.footer-bottom-links a{
  font-size:13px;color:rgba(255,255,255,0.45);
  transition:var(--transition)
}
.footer-bottom-links a:hover{color:#fff}

/* ══════════════════════════════════════════════════════
   FLOATING ELEMENTS
═══════════════════════════════════════════════════════ */
.whatsapp-float{
  position:fixed;bottom:28px;right:28px;
  width:60px;height:60px;
  background:#25d366;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:28px;color:#fff;
  box-shadow:0 4px 20px rgba(37,211,102,0.45);
  z-index:9999;transition:var(--transition);
  text-decoration:none
}
.whatsapp-float:hover{transform:scale(1.12);box-shadow:0 8px 32px rgba(37,211,102,0.55)}

.mobile-cta-bar{
  display:none;position:fixed;bottom:0;left:0;right:0;
  background:#fff;border-top:1px solid var(--border);
  padding:10px 16px;gap:8px;z-index:998;
  box-shadow:0 -4px 20px rgba(0,0,0,0.08)
}
.mobile-cta-bar a{
  flex:1;display:flex;align-items:center;
  justify-content:center;gap:6px;
  padding:12px 8px;border-radius:var(--radius-sm);
  font-size:13px;font-weight:600;
  transition:var(--transition)
}
.mobile-cta-call{
  background:var(--primary-light);color:var(--primary)
}
.mobile-cta-wa{background:#25d366;color:#fff}
.mobile-cta-apply{background:var(--primary);color:#fff}

/* ══════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════ */
@media(max-width:1024px){
  .grid-4{grid-template-columns:repeat(2,1fr)}
  .hero-stats{grid-template-columns:repeat(2,1fr)}
  .results-stats{grid-template-columns:repeat(2,1fr)}
  .footer-grid{grid-template-columns:1fr 1fr}
}

@media(max-width:768px){
  .section{padding:56px 0}
  .section-header{margin-bottom:36px}
  .section-header h2{font-size:26px}
  .section-header p{font-size:15px}

  .nav-links,.nav-phone,.nav-right .btn{display:none}
  .nav-hamburger{display:flex}

  .hero-inner{grid-template-columns:1fr;gap:36px}
  .hero-content h1{font-size:32px}
  .hero-content p{font-size:16px}
  .hero-cta{flex-direction:column}
  .hero-cta .btn{width:100%}
  .hero-stats{grid-template-columns:repeat(2,1fr);gap:10px}
  .hero-image{display:none}

  .trust-cards{grid-template-columns:repeat(2,1fr);gap:16px}
  .trust-card{padding:20px 16px}

  .course-cards{grid-template-columns:1fr;max-width:480px;margin:0 auto}

  .results-stats{grid-template-columns:repeat(2,1fr)}
  .testimonial-cards{grid-template-columns:1fr}

  .lead-form-inner{grid-template-columns:1fr;gap:32px}
  .lead-form-content{display:none}
  .form-card{padding:28px 20px}

  .footer-grid{grid-template-columns:1fr}
  .footer-brand{margin-bottom:0}

  .whatsapp-float{width:52px;height:52px;font-size:24px;bottom:76px;right:16px}
  .mobile-cta-bar{display:flex}
  body{padding-bottom:60px}

  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
  .faq-question{font-size:15px;padding:16px 18px}
  .faq-answer-inner{padding:0 18px 16px}
}

@media(max-width:480px){
  .container{padding:0 16px}
  .hero-content h1{font-size:28px}
  .hero-stat-num{font-size:22px}
  .form-card{padding:24px 16px}
}

/* Custom Style Overrides from LLM */
{{CUSTOM_STYLE_OVERRIDES}}
</style>
</head>
<body>

<!-- ══ NAV ══════════════════════════════════════════════════ -->
<nav id="nav">
<div class="container">
<div class="nav-inner">
  <div class="nav-logo">
    <div class="nav-logo-icon">{{NAV_LOGO_LETTER}}</div>
    <div class="nav-logo-text">{{NAV_INSTITUTE_NAME}}</div>
  </div>
  <div class="nav-links">
    <a href="#trust">Why Us</a>
    <a href="#courses">Courses</a>
    <a href="#results">Results</a>
    <a href="#faq">FAQ</a>
  </div>
  <div class="nav-right">
    <a href="tel:{{PHONE_NUMBER}}" class="nav-phone">
      <i class="fa fa-phone"></i> {{PHONE_NUMBER}}
    </a>
    <a href="#lead-form" class="btn btn-primary btn-sm">{{NAV_CTA}}</a>
  </div>
  <button class="nav-hamburger" id="hamburger" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</div>
</div>
<div class="mobile-menu" id="mobileMenu">
  <a href="#trust">Why Us</a>
  <a href="#courses">Courses</a>
  <a href="#results">Results</a>
  <a href="#faq">FAQ</a>
  <a href="tel:{{PHONE_NUMBER}}">📞 {{PHONE_NUMBER}}</a>
  <a href="#lead-form" class="btn btn-primary">{{NAV_CTA}}</a>
</div>
</nav>

<!-- ══ HERO ══════════════════════════════════════════════════ -->
<section id="hero">
<div class="container">
<div class="hero-inner">
  <div class="hero-content">
    <div class="tag"><i class="fa fa-star"></i> {{HERO_TAG}}</div>
    <h1>{{HERO_TITLE}} <span>{{HERO_TITLE_HIGHLIGHT}}</span></h1>
    <p>{{HERO_SUBTITLE}}</p>
    <div class="hero-cta">
      <a href="#lead-form" class="btn btn-primary btn-lg">
        <i class="fa fa-calendar-check"></i> {{CTA_PRIMARY}}
      </a>
      <a href="#courses" class="btn btn-outline btn-lg">
        <i class="fa fa-book-open"></i> {{CTA_SECONDARY}}
      </a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-num">{{STAT_1_NUM}}</div>
        <div class="hero-stat-label">{{STAT_1_LABEL}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{{STAT_2_NUM}}</div>
        <div class="hero-stat-label">{{STAT_2_LABEL}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{{STAT_3_NUM}}</div>
        <div class="hero-stat-label">{{STAT_3_LABEL}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{{STAT_4_NUM}}</div>
        <div class="hero-stat-label">{{STAT_4_LABEL}}</div>
      </div>
    </div>
  </div>
  <div class="hero-image">
    <img src="https://picsum.photos/600/450?random=1"
         alt="{{INSTITUTE_NAME}} Students" class="hero-image-main"/>
    <div class="hero-image-badge">
      <i class="fa fa-trophy"></i>
      <div>
        <strong>{{BADGE_TITLE}}</strong>
        <span>{{BADGE_SUBTITLE}}</span>
      </div>
    </div>
  </div>
</div>
</div>
</section>

<!-- ══ TRUST ══════════════════════════════════════════════════ -->
<section id="trust" class="section">
<div class="container">
  <div class="section-header">
    <h2>{{TRUST_HEADING}}</h2>
    <p>{{TRUST_SUBHEADING}}</p>
  </div>
  <div class="trust-cards">
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-chalkboard-teacher"></i></div>
      <h3>{{TRUST_1_TITLE}}</h3>
      <p>{{TRUST_1_DESC}}</p>
    </div>
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-clipboard-list"></i></div>
      <h3>{{TRUST_2_TITLE}}</h3>
      <p>{{TRUST_2_DESC}}</p>
    </div>
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-user-check"></i></div>
      <h3>{{TRUST_3_TITLE}}</h3>
      <p>{{TRUST_3_DESC}}</p>
    </div>
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-laptop"></i></div>
      <h3>{{TRUST_4_TITLE}}</h3>
      <p>{{TRUST_4_DESC}}</p>
    </div>
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-chart-line"></i></div>
      <h3>{{TRUST_5_TITLE}}</h3>
      <p>{{TRUST_5_DESC}}</p>
    </div>
    <div class="trust-card">
      <div class="trust-icon"><i class="fa fa-compass"></i></div>
      <h3>{{TRUST_6_TITLE}}</h3>
      <p>{{TRUST_6_DESC}}</p>
    </div>
  </div>
</div>
</section>

<!-- ══ COURSES ════════════════════════════════════════════════ -->
<section id="courses" class="section section-alt">
<div class="container">
  <div class="section-header">
    <h2>{{COURSES_HEADING}}</h2>
    <p>{{COURSES_SUBHEADING}}</p>
  </div>
  <div class="course-cards">
    <div class="course-card">
      <div class="course-card-header">
        <h3>{{COURSE_1_NAME}}</h3>
        <p>{{COURSE_1_TAGLINE}}</p>
      </div>
      <div class="course-card-body">
        <div class="course-levels">
          <div class="course-levels-label">Levels Offered</div>
          <div class="course-level-tags">
            {{COURSE_1_LEVELS}}
          </div>
        </div>
        <div class="course-subjects">
          <div class="course-subjects-label">Key Subjects</div>
          <ul>{{COURSE_1_SUBJECTS}}</ul>
        </div>
        <div class="course-outcome">
          <strong>Career Outcome:</strong> {{COURSE_1_OUTCOME}}
        </div>
        <a href="#lead-form" class="btn btn-primary btn-full">
          <i class="fa fa-file-alt"></i> Get Syllabus
        </a>
      </div>
    </div>
    <div class="course-card">
      <div class="course-card-header" style="background:var(--accent)">
        <h3>{{COURSE_2_NAME}}</h3>
        <p>{{COURSE_2_TAGLINE}}</p>
      </div>
      <div class="course-card-body">
        <div class="course-levels">
          <div class="course-levels-label">Levels Offered</div>
          <div class="course-level-tags">
            {{COURSE_2_LEVELS}}
          </div>
        </div>
        <div class="course-subjects">
          <div class="course-subjects-label">Key Subjects</div>
          <ul>{{COURSE_2_SUBJECTS}}</ul>
        </div>
        <div class="course-outcome">
          <strong>Career Outcome:</strong> {{COURSE_2_OUTCOME}}
        </div>
        <a href="#lead-form" class="btn btn-accent btn-full">
          <i class="fa fa-file-alt"></i> Get Syllabus
        </a>
      </div>
    </div>
    <div class="course-card">
      <div class="course-card-header" style="background:#1e3a5f">
        <h3>{{COURSE_3_NAME}}</h3>
        <p>{{COURSE_3_TAGLINE}}</p>
      </div>
      <div class="course-card-body">
        <div class="course-levels">
          <div class="course-levels-label">Levels Offered</div>
          <div class="course-level-tags">
            {{COURSE_3_LEVELS}}
          </div>
        </div>
        <div class="course-subjects">
          <div class="course-subjects-label">Key Subjects</div>
          <ul>{{COURSE_3_SUBJECTS}}</ul>
        </div>
        <div class="course-outcome">
          <strong>Career Outcome:</strong> {{COURSE_3_OUTCOME}}
        </div>
        <a href="#lead-form" class="btn btn-full" style="background:#1e3a5f;color:#fff">
          <i class="fa fa-file-alt"></i> Get Syllabus
        </a>
      </div>
    </div>
  </div>
</div>
</section>

<!-- ══ RESULTS ════════════════════════════════════════════════ -->
<section id="results" class="section">
<div class="container">
  <div class="section-header">
    <h2>{{RESULTS_HEADING}}</h2>
    <p>{{RESULTS_SUBHEADING}}</p>
  </div>
  <div class="results-stats">
    <div class="result-stat">
      <div class="result-stat-num">{{RESULT_1_NUM}}</div>
      <div class="result-stat-label">{{RESULT_1_LABEL}}</div>
    </div>
    <div class="result-stat">
      <div class="result-stat-num">{{RESULT_2_NUM}}</div>
      <div class="result-stat-label">{{RESULT_2_LABEL}}</div>
    </div>
    <div class="result-stat">
      <div class="result-stat-num">{{RESULT_3_NUM}}</div>
      <div class="result-stat-label">{{RESULT_3_LABEL}}</div>
    </div>
    <div class="result-stat">
      <div class="result-stat-num">{{RESULT_4_NUM}}</div>
      <div class="result-stat-label">{{RESULT_4_LABEL}}</div>
    </div>
  </div>
  <div class="testimonial-cards">
    <div class="testimonial-card">
      <div class="testimonial-stars">
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i>
      </div>
      <p class="testimonial-text">{{TESTIMONIAL_1_TEXT}}</p>
      <div class="testimonial-author">
        <div class="testimonial-avatar">{{TESTIMONIAL_1_INITIAL}}</div>
        <div>
          <div class="testimonial-name">{{TESTIMONIAL_1_NAME}}</div>
          <div class="testimonial-meta">{{TESTIMONIAL_1_META}}</div>
        </div>
      </div>
    </div>
    <div class="testimonial-card">
      <div class="testimonial-stars">
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i>
      </div>
      <p class="testimonial-text">{{TESTIMONIAL_2_TEXT}}</p>
      <div class="testimonial-author">
        <div class="testimonial-avatar">{{TESTIMONIAL_2_INITIAL}}</div>
        <div>
          <div class="testimonial-name">{{TESTIMONIAL_2_NAME}}</div>
          <div class="testimonial-meta">{{TESTIMONIAL_2_META}}</div>
        </div>
      </div>
    </div>
    <div class="testimonial-card">
      <div class="testimonial-stars">
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i><i class="fas fa-star"></i>
        <i class="fas fa-star"></i>
      </div>
      <p class="testimonial-text">{{TESTIMONIAL_3_TEXT}}</p>
      <div class="testimonial-author">
        <div class="testimonial-avatar">{{TESTIMONIAL_3_INITIAL}}</div>
        <div>
          <div class="testimonial-name">{{TESTIMONIAL_3_NAME}}</div>
          <div class="testimonial-meta">{{TESTIMONIAL_3_META}}</div>
        </div>
      </div>
    </div>
  </div>
</div>
</section>

<!-- ══ LEAD FORM ══════════════════════════════════════════════ -->
<section id="lead-form" class="section section-alt">
<div class="container">
<div class="lead-form-inner">
  <div class="lead-form-content">
    <div class="tag"><i class="fa fa-comments"></i> Free Counselling</div>
    <h2>{{FORM_HEADING}}</h2>
    <p>{{FORM_SUBHEADING}}</p>
    <div class="lead-form-bullets">
      <div class="lead-form-bullet">
        <i class="fa fa-check"></i> {{FORM_BULLET_1}}
      </div>
      <div class="lead-form-bullet">
        <i class="fa fa-check"></i> {{FORM_BULLET_2}}
      </div>
      <div class="lead-form-bullet">
        <i class="fa fa-check"></i> {{FORM_BULLET_3}}
      </div>
    </div>
  </div>
  <div class="form-card">
    <h3>{{FORM_CARD_TITLE}}</h3>
    <div id="formFields">
      <div class="form-group">
        <label class="form-label">Full Name *</label>
        <input type="text" class="form-input" id="fname" placeholder="Your full name"/>
      </div>
      <div class="form-group">
        <label class="form-label">Phone Number *</label>
        <input type="tel" class="form-input" id="fphone" placeholder="+91 98765 43210"/>
      </div>
      <div class="form-group">
        <label class="form-label">Course Interested In</label>
        <select class="form-select" id="fcourse">
          <option value="">Select a course</option>
          {{FORM_COURSE_OPTIONS}}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Your City</label>
        <input type="text" class="form-input" id="fcity" placeholder="Your city"/>
      </div>
      <div class="form-submit">
        <button class="btn btn-primary btn-full btn-lg" id="formSubmitBtn">
          <i class="fa fa-paper-plane"></i> {{FORM_CTA}}
        </button>
      </div>
      <p class="form-note">
        <i class="fa fa-lock"></i> {{FORM_NOTE}}
      </p>
    </div>
    <div class="form-success" id="formSuccess">
      <i class="fa fa-check-circle"></i>
      <h3>{{FORM_SUCCESS_TITLE}}</h3>
      <p>{{FORM_SUCCESS_MSG}}</p>
    </div>
  </div>
</div>
</div>
</section>

<!-- ══ FAQ ════════════════════════════════════════════════════ -->
<section id="faq" class="section">
<div class="container">
  <div class="section-header">
    <h2>{{FAQ_HEADING}}</h2>
    <p>{{FAQ_SUBHEADING}}</p>
  </div>
  <div class="faq-list">
    <div class="faq-item">
      <button class="faq-question">
        {{FAQ_1_Q}}<span class="faq-icon"><i class="fa fa-plus"></i></span>
      </button>
      <div class="faq-answer"><div class="faq-answer-inner">{{FAQ_1_A}}</div></div>
    </div>
    <div class="faq-item">
      <button class="faq-question">
        {{FAQ_2_Q}}<span class="faq-icon"><i class="fa fa-plus"></i></span>
      </button>
      <div class="faq-answer"><div class="faq-answer-inner">{{FAQ_2_A}}</div></div>
    </div>
    <div class="faq-item">
      <button class="faq-question">
        {{FAQ_3_Q}}<span class="faq-icon"><i class="fa fa-plus"></i></span>
      </button>
      <div class="faq-answer"><div class="faq-answer-inner">{{FAQ_3_A}}</div></div>
    </div>
    <div class="faq-item">
      <button class="faq-question">
        {{FAQ_4_Q}}<span class="faq-icon"><i class="fa fa-plus"></i></span>
      </button>
      <div class="faq-answer"><div class="faq-answer-inner">{{FAQ_4_A}}</div></div>
    </div>
    <div class="faq-item">
      <button class="faq-question">
        {{FAQ_5_Q}}<span class="faq-icon"><i class="fa fa-plus"></i></span>
      </button>
      <div class="faq-answer"><div class="faq-answer-inner">{{FAQ_5_A}}</div></div>
    </div>
  </div>
</div>
</section>

<!-- ══ FOOTER ═════════════════════════════════════════════════ -->
<footer id="footer">
<div class="container">
  <div class="footer-grid">
    <div class="footer-brand">
      <h3>{{NAV_INSTITUTE_NAME}} <span>.</span></h3>
      <p>{{FOOTER_ABOUT}}</p>
      <div class="footer-socials">
        <a href="{{SOCIAL_FACEBOOK}}" class="footer-social"><i class="fab fa-facebook-f"></i></a>
        <a href="{{SOCIAL_INSTAGRAM}}" class="footer-social"><i class="fab fa-instagram"></i></a>
        <a href="{{SOCIAL_YOUTUBE}}" class="footer-social"><i class="fab fa-youtube"></i></a>
        <a href="{{WHATSAPP_LINK}}" class="footer-social"><i class="fab fa-whatsapp"></i></a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Courses</h4>
      <ul>{{FOOTER_COURSE_LINKS}}</ul>
    </div>
    <div class="footer-col">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="#trust">Why Choose Us</a></li>
        <li><a href="#results">Results</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#lead-form">Free Counselling</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact Us</h4>
      <div class="footer-contact">
        <div class="footer-contact-item">
          <i class="fa fa-map-marker-alt"></i>
          <span>{{FOOTER_ADDRESS}}</span>
        </div>
        <div class="footer-contact-item">
          <i class="fa fa-phone"></i>
          <a href="tel:{{PHONE_NUMBER}}">{{PHONE_NUMBER}}</a>
        </div>
        <div class="footer-contact-item">
          <i class="fab fa-whatsapp"></i>
          <a href="{{WHATSAPP_LINK}}">WhatsApp Us</a>
        </div>
        <div class="footer-contact-item">
          <i class="fa fa-envelope"></i>
          <a href="mailto:{{EMAIL_ADDRESS}}">{{EMAIL_ADDRESS}}</a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <p>{{FOOTER_COPYRIGHT}}</p>
    <div class="footer-bottom-links">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms of Use</a>
    </div>
  </div>
</div>
</footer>

<!-- ══ FLOATING ELEMENTS ══════════════════════════════════════ -->
<a href="{{WHATSAPP_LINK}}" class="whatsapp-float" target="_blank" aria-label="WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>

<div class="mobile-cta-bar">
  <a href="tel:{{PHONE_NUMBER}}" class="mobile-cta-call">
    <i class="fa fa-phone"></i> Call Now
  </a>
  <a href="{{WHATSAPP_LINK}}" class="mobile-cta-wa">
    <i class="fab fa-whatsapp"></i> WhatsApp
  </a>
  <a href="#lead-form" class="mobile-cta-apply">
    <i class="fa fa-edit"></i> Apply Now
  </a>
</div>

<!-- ══ SCHEMA ═════════════════════════════════════════════════ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "{{INSTITUTE_NAME}}",
  "url": "{{WEBSITE_URL}}",
  "telephone": "{{PHONE_NUMBER}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{FOOTER_ADDRESS}}",
    "addressLocality": "{{CITY_NAME}}",
    "addressCountry": "IN"
  },
  "description": "{{META_DESCRIPTION}}"
}
</script>

<script>
// ── FAQ Accordion ─────────────────────────────────────────
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

// ── Mobile Nav ────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
  mobileMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });
}

// ── Form Submit ───────────────────────────────────────────
const formBtn = document.getElementById('formSubmitBtn');
if (formBtn) {
  formBtn.addEventListener('click', () => {
    const name  = document.getElementById('fname')?.value?.trim();
    const phone = document.getElementById('fphone')?.value?.trim();
    if (!name || !phone) {
      alert('Please enter your name and phone number.');
      return;
    }
    document.getElementById('formFields').style.display = 'none';
    document.getElementById('formSuccess').style.display = 'block';
  });
}

// ── Smooth scroll ─────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });
});
</script>
</body>
</html>'''


# ── All placeholder keys in the template ─────────────────────────────────────
TEMPLATE_PLACEHOLDERS = [
    "META_TITLE", "META_DESCRIPTION", "GOOGLE_FONTS_IMPORT",
    "COLOR_PRIMARY", "COLOR_PRIMARY_DARK", "COLOR_PRIMARY_LIGHT",
    "COLOR_ACCENT", "COLOR_ACCENT_LIGHT",
    "COLOR_TEXT_DARK", "COLOR_TEXT_BODY", "COLOR_TEXT_MUTED",
    "COLOR_BG_LIGHT", "COLOR_BG_SECTION", "COLOR_BORDER",
    "FONT_HEADING", "FONT_BODY",
    "NAV_LOGO_LETTER", "NAV_INSTITUTE_NAME", "NAV_CTA",
    "PHONE_NUMBER", "WHATSAPP_LINK", "EMAIL_ADDRESS",
    "WEBSITE_URL", "INSTITUTE_NAME", "CITY_NAME",
    "HERO_TAG", "HERO_TITLE", "HERO_TITLE_HIGHLIGHT", "HERO_SUBTITLE",
    "CTA_PRIMARY", "CTA_SECONDARY",
    "STAT_1_NUM", "STAT_1_LABEL", "STAT_2_NUM", "STAT_2_LABEL",
    "STAT_3_NUM", "STAT_3_LABEL", "STAT_4_NUM", "STAT_4_LABEL",
    "BADGE_TITLE", "BADGE_SUBTITLE",
    "TRUST_HEADING", "TRUST_SUBHEADING",
    "TRUST_1_TITLE", "TRUST_1_DESC",
    "TRUST_2_TITLE", "TRUST_2_DESC",
    "TRUST_3_TITLE", "TRUST_3_DESC",
    "TRUST_4_TITLE", "TRUST_4_DESC",
    "TRUST_5_TITLE", "TRUST_5_DESC",
    "TRUST_6_TITLE", "TRUST_6_DESC",
    "COURSES_HEADING", "COURSES_SUBHEADING",
    "COURSE_1_NAME", "COURSE_1_TAGLINE", "COURSE_1_LEVELS",
    "COURSE_1_SUBJECTS", "COURSE_1_OUTCOME",
    "COURSE_2_NAME", "COURSE_2_TAGLINE", "COURSE_2_LEVELS",
    "COURSE_2_SUBJECTS", "COURSE_2_OUTCOME",
    "COURSE_3_NAME", "COURSE_3_TAGLINE", "COURSE_3_LEVELS",
    "COURSE_3_SUBJECTS", "COURSE_3_OUTCOME",
    "RESULTS_HEADING", "RESULTS_SUBHEADING",
    "RESULT_1_NUM", "RESULT_1_LABEL",
    "RESULT_2_NUM", "RESULT_2_LABEL",
    "RESULT_3_NUM", "RESULT_3_LABEL",
    "RESULT_4_NUM", "RESULT_4_LABEL",
    "TESTIMONIAL_1_TEXT", "TESTIMONIAL_1_INITIAL",
    "TESTIMONIAL_1_NAME", "TESTIMONIAL_1_META",
    "TESTIMONIAL_2_TEXT", "TESTIMONIAL_2_INITIAL",
    "TESTIMONIAL_2_NAME", "TESTIMONIAL_2_META",
    "TESTIMONIAL_3_TEXT", "TESTIMONIAL_3_INITIAL",
    "TESTIMONIAL_3_NAME", "TESTIMONIAL_3_META",
    "FORM_HEADING", "FORM_SUBHEADING",
    "FORM_BULLET_1", "FORM_BULLET_2", "FORM_BULLET_3",
    "FORM_CARD_TITLE", "FORM_COURSE_OPTIONS",
    "FORM_CTA", "FORM_NOTE",
    "FORM_SUCCESS_TITLE", "FORM_SUCCESS_MSG",
    "FAQ_HEADING", "FAQ_SUBHEADING",
    "FAQ_1_Q", "FAQ_1_A",
    "FAQ_2_Q", "FAQ_2_A",
    "FAQ_3_Q", "FAQ_3_A",
    "FAQ_4_Q", "FAQ_4_A",
    "FAQ_5_Q", "FAQ_5_A",
    "FOOTER_ABOUT", "FOOTER_ADDRESS", "FOOTER_COPYRIGHT",
    "FOOTER_COURSE_LINKS",
    "SOCIAL_FACEBOOK", "SOCIAL_INSTAGRAM", "SOCIAL_YOUTUBE",
    "CUSTOM_STYLE_OVERRIDES"
]


def get_base_template() -> str:
    return BASE_TEMPLATE_HTML


def get_all_placeholders() -> list:
    return TEMPLATE_PLACEHOLDERS