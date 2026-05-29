import sys
import asyncio
import uvicorn

# ── Windows event loop fix for Playwright ──────────────────────────────────
# On Windows, asyncio needs ProactorEventLoop for subprocess (which Playwright uses)
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

if __name__ == "__main__":
    # Disable reload=True on Windows to prevent event loop policy issues
    # The policy needs to be consistent across all processes
    reload = not (sys.platform == "win32")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        log_level="info"
    )