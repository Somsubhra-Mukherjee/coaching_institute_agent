# Project Overview: Coaching Institute Agent

## Table of Contents
- [High‑Level Architecture](#high-level-architecture)
- [Frontend (Static Site)](#frontend-static-site)
- [Backend (FastAPI + LangGraph)](#backend-fastapi--langgraph)
- [Data Flow & Interaction](#data-flow--interaction)
- [Key Files & Types](#key-files--types)
- [LangGraph Workflow Details](#langgraph-workflow-details)
- [Running the Application Locally](#running-the-application-locally)
- [Glossary (Layman Terms)](#glossary-layman-terms)

---

## High‑Level Architecture

```mermaid
flowchart LR
    subgraph Frontend[Frontend (Static Files)]
        index["index.html"]
        css["styles.css"]
        js["scripts/*.js"]
    end
    subgraph Backend[Backend (FastAPI)]
        main["backend/main.py"]
        agents["backend/agents/*.py"]
        utils["backend/utils/*.py"]
        scraper["backend/scraper/*.py"]
        workflow["backend/agents/workflow.py"]
    end
    Frontend -->|HTTP GET/POST| Backend
    Backend -->|uses| LangGraph["LangGraph (State Graph)" ]
    Backend -->|stores| outputs["outputs/ (audit, redesign, screenshots)" ]
    Backend -->|serves| static["/static (frontend files)" ]
```

The system consists of a **static front‑end** (plain HTML/CSS/JS) and a **Python FastAPI back‑end** that runs an autonomous workflow powered by **LangGraph**. The front‑end talks to the back‑end via HTTP endpoints.

---

## Frontend (Static Site)

- **Location:** `frontend/` (served by FastAPI at `/static`).
- **Main entry point:** `frontend/index.html` – contains the landing page layout and UI components (hero, sections, POCs, etc.).
- **Styling:** `styles.css` (custom CSS with dark mode, glass‑morphism, animations). No UI framework – pure vanilla HTML & CSS.
- **Interactivity:** Small inline scripts or separate JS files in `js/` that:
  - Capture the URL entered by a user.
  - Call the back‑end `POST /audit` endpoint using `fetch`.
  - Display the audit / redesign results, and allow downloading files.

### What the Frontend Does
1. **Collects input** – the website URL the user wants audited.
2. **Calls the API** – sends a JSON payload (`{"url": "https://example.com"}`) to the back‑end.
3. **Shows loading / results** – updates the UI with progress messages and finally renders the audit text, redesign preview, and evaluation scores.

---

## Backend (FastAPI + LangGraph)

- **Entry point:** `backend/main.py` – creates a FastAPI app, registers CORS, mounts static folders, and defines API routes.
- **Key Routes:**
  - `GET /` – serves the front‑end `index.html`.
  - `GET /health` – health check.
  - `POST /audit` – main endpoint that drives the whole process.
  - `GET /history`, `GET /history/{slug}`, `GET /download/*` – retrieve past runs.
- **Data models (Pydantic):**
  - `AuditRequest` – input schema (`url: str`).
  - `AuditResponse` – extensive output including audit text, redesign HTML, evaluation scores, file paths, status, and error messages.
- **Utility modules:**
  - `backend/utils/file_manager.py` – helpers to generate slugs, save files, read history.
  - `backend/scraper/website_scraper.py` – uses Playwright to scrape the target website and take a screenshot.
- **Agents & Workflow:**
  - `backend/agents/workflow.py` builds a **LangGraph** `StateGraph` that orchestrates three agents: **AuditAgent**, **RedesignAgent**, **EvalAgent** (names may differ, but conceptually they perform those steps).
  - The graph defines states, transitions, and a final `END` node.
- **LangGraph usage:**
  - Imported via `from langgraph.graph import StateGraph, END`.
  - The graph is created once at startup (`startup_event`) and stored in the global `workflow` variable.
  - When a request arrives, `workflow.invoke(initial_state)` is called in a thread‑pool to avoid blocking the async event loop.

---

## Data Flow & Interaction

1. **User clicks “Audit”** → Browser `fetch` → `POST /audit` (JSON `{url}`).
2. **FastAPI handler (`run_audit`)** receives request.
3. **Scrape step** – `scrape_website` loads the page, extracts text, captures a screenshot, returns a dict with `scrape_success`, `website_text`, `screenshot_path`, etc.
4. **Formatting step** – `format_scraped_data_for_prompt` converts the scraped dict into a single string suitable for LLM prompts.
5. **LangGraph execution** – `initial_state` is built (contains URL, website data, screenshot path). The graph runs:
   - **Audit node:** generates a critique of the current site.
   - **Redesign node:** produces a revised HTML layout.
   - **Evaluation node:** scores the redesign on criteria (CTA, hierarchy, sections, trust, mobile, etc.).
6. **Result handling** – The final state dictionary includes all outputs and meta‑info.
7. **Persistence** – `save_audit`, `save_redesign`, and `save_metadata` write files under `outputs/` (`audits/`, `redesigns/`).
8. **Response** – `AuditResponse` JSON is sent back; the front‑end displays it and offers download links.
9. **History endpoints** – read the saved JSON files to list previous runs.

---

## Key Files & Types

| Path | Purpose | Important Types |
|------|---------|----------------|
| `backend/main.py` | FastAPI server, route definitions | `FastAPI`, `AuditRequest`, `AuditResponse` |
| `backend/agents/workflow.py` | Constructs LangGraph state machine | `StateGraph`, `END`, custom state dict |
| `backend/utils/file_manager.py` | File‑system helpers (slug, save, read) | Functions returning `str` paths |
| `backend/scraper/website_scraper.py` | Playwright‑based scraper | Returns `Dict[str, Any]` with `scrape_success`, `screenshot_path` |
| `frontend/index.html` | UI markup | — |
| `styles.css` | Visual design, gradients, glass‑morphism | — |
| `js/*.js` | Front‑end fetch logic | Uses `fetch` and `async/await` |
| `requirements.txt` | Python dependencies (includes `langgraph==1.2.0`, `fastapi`, `playwright`, etc.) | — |

### Pydantic Models (Technical)
```python
class AuditRequest(BaseModel):
    url: str

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
```
These models give both **type safety** (FastAPI validates incoming JSON) and clear **OpenAPI documentation**.

---

## LangGraph Workflow Details

- **State Graph Construction (`build_workflow`)**:
  1. Create a `StateGraph` instance.
  2. Add **nodes** for each agent (`audit`, `redesign`, `evaluate`).
  3. Define **edges** that pass the evolving state dict from one node to the next.
  4. Set the `END` node when evaluation is complete.
- **State Shape** (what travels through the graph):
  ```python
  state = {
      "url": str,
      "website_data": str,          # formatted scraped content
      "screenshot_path": str,
      "audit": str,
      "html_code": str,
      "eval_score": float,
      "eval_passed": bool,
      "iteration": int,
      "status": str,
      "error": str,
      # additional score fields …
  }
  ```
- **Why LangGraph?** It provides a **deterministic orchestration** layer for LLM‑driven agents, letting us define a clear sequence and fallback logic without writing ad‑hoc async code.
- **Checkpointing** (via `langgraph-checkpoint` and `langgraph-sdk`) enables persisting intermediate states, useful for debugging or resuming long runs.

---

## Running the Application Locally

1. **Install dependencies** (inside the `coaching_institute_agent` folder):
   ```bash
   pip install -r requirements.txt
   python -m playwright install  # required for the scraper
   ```
2. **Start the server**:
   ```bash
   uvicorn backend.main:app --reload
   ```
   - The server will be reachable at `http://127.0.0.1:8000`.
3. **Open the front‑end** in a browser: `http://127.0.0.1:8000/`.
4. **Use the UI** to enter a site URL and watch the audit/redesign flow.
5. **Inspect saved files** under the `outputs/` directory (audits, redesigns, screenshots).

---

## Glossary (Layman Terms)

- **Frontend** – The part of the website you see and click on (HTML pages, colors, buttons).
- **Backend** – The hidden brain that does the heavy work: talking to the web, running AI, and storing results.
- **FastAPI** – A fast web server written in Python; it lets the front‑end ask the back‑end questions.
- **LangGraph** – Think of it as a flow‑chart for AI agents. It tells the system *first do this, then that*, and keeps track of information as it moves around.
- **Agent** – A small AI program that knows how to do one specific job (e.g., write an audit, redesign a page, grade the result).
- **State** – A suitcase of data that travels from step to step (the URL, the scraped text, the scores, etc.).
- **Scraper** – A robot that visits a website, reads its content, and takes a picture.
- **Slug** – A short, URL‑friendly name derived from the website address, used to name the saved files.
- **Evaluation scores** – Numbers that rate how good the redesign is on things like calls‑to‑action, mobile friendliness, and trust.
- **Checkpointing** – Saving the AI’s progress so if something crashes you don’t have to start over.

---

*This document lives in the project’s artifact folder as `project_overview.md`. It provides both a technical roadmap for developers and a plain‑English walkthrough for anyone curious about how the system works.*
