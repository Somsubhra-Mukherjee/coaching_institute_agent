import sys
import asyncio
import traceback
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# ── Windows event loop fix for Playwright ──────────────────────────────────
# MUST be set before any async operations or app creation
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from backend.scraper.website_scraper import scrape_website, format_scraped_data_for_prompt
from backend.agents.workflow import build_workflow, create_initial_state
from backend.utils.file_manager import (
    generate_file_slug,
    save_audit,
    save_redesign,
    save_metadata,
    list_previous_runs,
    read_file,
    save_site_text
)


# ── App setup ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Coaching Institute Audit Agent",
    description="Local AI agent for website audits and redesigns",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve outputs folder as static files (for screenshots etc)
import os
from backend.utils.file_manager import BASE_OUTPUT_DIR
outputs_dir = str(BASE_OUTPUT_DIR)
os.makedirs(outputs_dir, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=outputs_dir), name="outputs")

# Serve frontend folder
frontend_dir = str(Path(__file__).resolve().parent.parent / "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# ── Request/Response models ─────────────────────────────────────────────────
class AuditRequest(BaseModel):
    url: str


# class AuditResponse(BaseModel):
#     success: bool
#     url: str
#     slug: str
#     audit: str
#     generated_prompt: str 
#     html_code: str
#     eval_score: int
#     eval_passed: bool
#     eval_issues: str
#     iterations: int
#     audit_file_path: str
#     redesign_file_path: str
#     screenshot_path: str
#     status: str
#     error: str

class AuditResponse(BaseModel):
    success: bool
    url: str
    slug: str
    audit: str
    generated_prompt: str
    html_code: str
    eval_score: float
    eval_score_cta: int
    eval_score_hierarchy: int
    eval_score_sections: int
    eval_score_trust: int
    eval_score_mobile: int
    eval_passed: bool
    eval_hard_fail: bool
    eval_hard_fail_reason: str
    eval_issues: str
    iterations: int
    audit_file_path: str
    redesign_file_path: str
    screenshot_path: str
    status: str
    error: str


# ── Build workflow once at startup ──────────────────────────────────────────
workflow = None

@app.on_event("startup")
async def startup_event():
    global workflow
    print("[STARTUP] Building LangGraph workflow...")
    workflow = build_workflow()
    print("[STARTUP] Workflow ready.")


# ── ROUTES ──────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Serve the frontend index.html"""
    return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Coaching Audit Agent is running"}


@app.post("/audit", response_model=AuditResponse)
async def run_audit(request: AuditRequest):
    """
    Main endpoint:
    1. Scrape the website
    2. Run LangGraph workflow (audit + redesign + evaluate)
    3. Save files
    4. Return results
    """
    url = request.url.strip()

    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"\n{'='*60}")
    print(f"[API] New audit request: {url}")
    print(f"{'='*60}")

    slug = generate_file_slug(url)

    try:
        # ── STEP 1: Scrape website ──────────────────────────────────
        print("\n[API] Step 1: Scraping website...")
        scraped_data = await scrape_website(url)

        if not scraped_data["scrape_success"]:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to scrape website: {scraped_data.get('error', 'Unknown error')}"
            )

        # ── STEP 2: Format data for prompts ────────────────────────
        print("\n[API] Step 2: Formatting scraped data...")
        website_data_str = format_scraped_data_for_prompt(scraped_data)

        # ── STEP 3: Run LangGraph workflow ──────────────────────────
        print("\n[API] Step 3: Running LangGraph workflow...")
        # initial_state = create_initial_state(url, website_data_str)
        initial_state = create_initial_state(
            url=url,
            website_data=website_data_str,
            screenshot_path=scraped_data.get("screenshot_path", "")
        )

        # Run workflow in thread pool to avoid blocking async loop
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None,
            lambda: workflow.invoke(initial_state)
        )

        print(f"\n[API] Workflow complete.")
        print(f"[API] Eval score: {final_state['eval_score']}/10")
        print(f"[API] Iterations: {final_state['iteration']}")

        # ── STEP 4: Save files ──────────────────────────────────────
        print("\n[API] Step 4: Saving output files...")

        audit_path = save_audit(final_state["audit"], slug)
        redesign_path = save_redesign(final_state["html_code"], slug)
        sitetext_path = save_site_text(scraped_data, slug)

        # Save metadata for history
        metadata = {
            "slug": slug,
            "url": url,
            "domain": scraped_data["domain"],
            "timestamp": scraped_data["timestamp"],
            "eval_score": final_state["eval_score"],
            "eval_passed": final_state["eval_passed"],
            "iterations": final_state["iteration"],
            "audit_file": audit_path,
            "redesign_file": redesign_path,
            "site_text_file": sitetext_path,
            "screenshot_file": scraped_data["screenshot_path"],
            "status": final_state["status"],
            "error": final_state.get("error", "")
        }
        save_metadata(metadata, slug)

        # ── STEP 5: Return response ─────────────────────────────────
        # return AuditResponse(
        #     success=True,
        #     url=url,
        #     slug=slug,
        #     audit=final_state["audit"],
        #     generated_prompt=final_state.get("generated_prompt", ""),
        #     html_code=final_state["html_code"],
        #     eval_score=final_state["eval_score"],
        #     eval_passed=final_state["eval_passed"],
        #     eval_issues=final_state["eval_issues"],
        #     iterations=final_state["iteration"],
        #     audit_file_path=audit_path,
        #     redesign_file_path=redesign_path,
        #     screenshot_path=scraped_data["screenshot_path"],
        #     status=final_state["status"],
        #     error=final_state.get("error", "")
        # )


        return AuditResponse(
            success=True,
            url=url,
            slug=slug,
            audit=final_state["audit"],
            generated_prompt=final_state.get("generated_prompt", ""),
            html_code=final_state["html_code"],
            eval_score=final_state["eval_score"],
            eval_score_cta=final_state.get("eval_score_cta", 0),
            eval_score_hierarchy=final_state.get("eval_score_hierarchy", 0),
            eval_score_sections=final_state.get("eval_score_sections", 0),
            eval_score_trust=final_state.get("eval_score_trust", 0),
            eval_score_mobile=final_state.get("eval_score_mobile", 0),
            eval_passed=final_state["eval_passed"],
            eval_hard_fail=final_state.get("eval_hard_fail", False),
            eval_hard_fail_reason=final_state.get("eval_hard_fail_reason", "None"),
            eval_issues=final_state["eval_issues"],
            iterations=final_state["iteration"],
            audit_file_path=audit_path,
            redesign_file_path=redesign_path,
            screenshot_path=scraped_data["screenshot_path"],
            status=final_state["status"],
            error=final_state.get("error", "")
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"[API] CRITICAL ERROR:\n{error_msg}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    """Return list of all previous audit runs"""
    runs = list_previous_runs()
    return {"runs": runs, "total": len(runs)}


@app.get("/history/{slug}")
async def get_run_by_slug(slug: str):
    """Return audit and HTML for a specific previous run"""
    audit_files = list(Path("outputs/audits").glob(f"{slug}*"))

    # Derive the domain folder (strip _YYYYMMDD_HHMMSS suffix)
    parts = slug.split("_")
    domain_folder = "_".join(parts[:-2]) if len(parts) >= 3 else slug
    redesign_index = Path("outputs/redesigns") / domain_folder / "index.html"

    if not audit_files and not redesign_index.exists():
        raise HTTPException(status_code=404, detail="Run not found")

    result = {"slug": slug}

    if audit_files:
        result["audit"] = read_file(str(audit_files[0]))
        result["audit_file"] = str(audit_files[0])

    if redesign_index.exists():
        result["html_code"] = read_file(str(redesign_index))
        result["redesign_file"] = str(redesign_index)

    return result


@app.get("/download/audit/{slug}")
async def download_audit(slug: str):
    """Download audit .txt file"""
    files = list(Path("outputs/audits").glob(f"{slug}*"))
    if not files:
        raise HTTPException(status_code=404, detail="Audit file not found")
    return FileResponse(
        path=str(files[0]),
        filename=files[0].name,
        media_type="text/plain"
    )


@app.get("/download/redesign/{slug}")
async def download_redesign(slug: str):
    """Download redesign index.html from the domain folder"""
    parts = slug.split("_")
    domain_folder = "_".join(parts[:-2]) if len(parts) >= 3 else slug
    filepath = Path("outputs/redesigns") / domain_folder / "index.html"
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Redesign file not found")
    return FileResponse(
        path=str(filepath),
        filename=f"{domain_folder}_redesign.html",
        media_type="text/html"
    )