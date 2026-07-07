import sys
import asyncio
import json
import traceback
from pathlib import Path

# Ensure coaching_institute_agent directory is in python path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from backend.scraper.website_scraper import scrape_website, format_scraped_data_for_prompt
from backend.agents.workflow import build_workflow, create_initial_state
from backend.utils.file_manager import generate_file_slug, save_audit, save_redesign, save_site_text, save_metadata

async def run_test():
    url = "https://example.com"
    print(f"=== Running Agent Flow Test for {url} ===")
    
    # 1. Test Scraper
    print("\n[TEST] 1. Scraping website...")
    try:
        scraped_data = await scrape_website(url)
        assert scraped_data is not None, "Scraped data is None"
        assert scraped_data.get("scrape_success") is True, f"Scrape failed: {scraped_data.get('error')}"
        print(f"[*] Scrape successful! Title: '{scraped_data['meta'].get('title')}'")
    except Exception as e:
        print(f"[FAIL] Scraper test failed: {e}")
        traceback.print_exc()
        return False

    # 2. Test Workflow
    print("\n[TEST] 2. Initializing and running LangGraph workflow...")
    try:
        website_data_str = format_scraped_data_for_prompt(scraped_data)
        initial_state = create_initial_state(
            url=url,
            website_data=website_data_str,
            screenshot_path=scraped_data.get("screenshot_path", "")
        )
        
        workflow = build_workflow()
        
        # Run workflow
        print("[*] Invoking workflow nodes (LLMs)...")
        final_state = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: workflow.invoke(initial_state)
        )
        
        # Verification
        assert final_state.get("audit"), "Audit report is empty"
        assert final_state.get("html_code"), "Redesigned HTML is empty"
        assert final_state.get("eval_score") is not None, "Eval score is missing"
        
        print("[*] Workflow completed successfully!")
        print(f"[*] Generated Audit Length: {len(final_state['audit'])} characters")
        print(f"[*] Generated HTML Length: {len(final_state['html_code'])} characters")
        print(f"[*] Evaluated Quality Score: {final_state['eval_score']}/10")
        print(f"[*] Iterations: {final_state['iteration']}")
    except Exception as e:
        print(f"[FAIL] Workflow test failed: {e}")
        traceback.print_exc()
        return False

    # 3. Test File Saving
    print("\n[TEST] 3. Verifying output saving on disk...")
    try:
        slug = generate_file_slug(url)
        audit_path = save_audit(final_state["audit"], slug)
        redesign_path = save_redesign(final_state["html_code"], slug)
        sitetext_path = save_site_text(scraped_data, slug)
        
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
        meta_path = save_metadata(metadata, slug)
        
        assert Path(audit_path).exists(), f"Audit file not found: {audit_path}"
        assert Path(redesign_path).exists(), f"Redesign file not found: {redesign_path}"
        assert Path(sitetext_path).exists(), f"Site text file not found: {sitetext_path}"
        assert Path(meta_path).exists(), f"Metadata file not found: {meta_path}"
        
        print("[*] File saving test passed successfully!")
    except Exception as e:
        print(f"[FAIL] File saving test failed: {e}")
        traceback.print_exc()
        return False

    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
    return True

if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
