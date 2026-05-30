# import re
# from typing import TypedDict
# from langgraph.graph import StateGraph, END

# from backend.utils.ollama_client import call_audit_model, call_redesign_model
# from backend.utils.prompts import (
#     get_audit_prompt,
#     get_redesign_prompt,
#     get_redesign_prompt_from_generated,
#     get_evaluator_prompt,
#     get_redesign_improvement_prompt
# )
# from backend.agents.prompt_generator import run_prompt_generator


# # ── LangGraph State ─────────────────────────────────────────────────────────

# class AgentState(TypedDict):
#     # Input
#     url: str
#     website_data: str
#     screenshot_path: str

#     # Agent outputs
#     audit: str
#     generated_prompt: str      # ← NEW: prompt generator output
#     html_code: str

#     # Evaluator
#     eval_score: int
#     eval_passed: bool
#     eval_issues: str
#     eval_feedback: str

#     # Control
#     iteration: int
#     max_iterations: int
#     status: str
#     error: str


# # ── Helpers ─────────────────────────────────────────────────────────────────

# def parse_evaluator_response(response: str) -> dict:
#     result = {
#         "score": 5,
#         "passed": False,
#         "issues": "",
#         "feedback": ""
#     }
#     try:
#         score_match = re.search(r"SCORE:\s*(\d+)", response, re.IGNORECASE)
#         if score_match:
#             result["score"] = int(score_match.group(1))

#         passed_match = re.search(r"PASSED:\s*(YES|NO)", response, re.IGNORECASE)
#         if passed_match:
#             result["passed"] = passed_match.group(1).upper() == "YES"

#         issues_match = re.search(
#             r"ISSUES:(.*?)IMPROVEMENT_INSTRUCTIONS:",
#             response, re.DOTALL | re.IGNORECASE
#         )
#         if issues_match:
#             result["issues"] = issues_match.group(1).strip()

#         feedback_match = re.search(
#             r"IMPROVEMENT_INSTRUCTIONS:(.*?)$",
#             response, re.DOTALL | re.IGNORECASE
#         )
#         if feedback_match:
#             result["feedback"] = feedback_match.group(1).strip()

#     except Exception as e:
#         print(f"[EVALUATOR PARSER] Error: {e}")
#     return result


# def extract_html(response: str) -> str:
#     html_match = re.search(
#         r"```html\s*(<!DOCTYPE.*?</html>)\s*```",
#         response, re.DOTALL | re.IGNORECASE
#     )
#     if html_match:
#         return html_match.group(1).strip()

#     code_match = re.search(
#         r"```\s*(<!DOCTYPE.*?</html>)\s*```",
#         response, re.DOTALL | re.IGNORECASE
#     )
#     if code_match:
#         return code_match.group(1).strip()

#     raw_match = re.search(
#         r"(<!DOCTYPE.*?</html>)",
#         response, re.DOTALL | re.IGNORECASE
#     )
#     if raw_match:
#         return raw_match.group(1).strip()

#     return response.strip()


# # ── AGENT NODES ─────────────────────────────────────────────────────────────

# def audit_agent(state: AgentState) -> AgentState:
#     """Node 1: Generate audit using llama3.1:8b"""
#     print("\n[AUDIT AGENT] Generating audit...")
#     state["status"] = "Generating audit..."

#     try:
#         prompt = get_audit_prompt(state["website_data"])
#         system = (
#             "You are a CRO and UX expert for Indian coaching institutes. "
#             "Be direct, concise, and actionable. Follow the format exactly."
#         )
#         audit = call_audit_model(prompt, system)
#         state["audit"] = audit
#         state["status"] = "Audit complete"
#         print(f"[AUDIT AGENT] Done. Length: {len(audit)} chars")

#     except Exception as e:
#         state["error"] = f"Audit error: {str(e)}"
#         state["audit"] = "Audit generation failed."
#         state["status"] = "Audit failed"
#         print(f"[AUDIT AGENT] ERROR: {e}")

#     return state


# def prompt_generator_agent(state: AgentState) -> AgentState:
#     """
#     Node 2: Generate detailed redesign prompt
#     Uses scraped data + screenshot + audit to create
#     a highly specific prompt for the redesign agent.
#     """
#     print("\n[PROMPT GENERATOR AGENT] Generating redesign prompt...")
#     state["status"] = "Generating redesign strategy prompt..."

#     try:
#         generated_prompt = run_prompt_generator(
#             url=state["url"],
#             website_data=state["website_data"],
#             audit=state["audit"],
#             screenshot_path=state.get("screenshot_path", "")
#         )
#         state["generated_prompt"] = generated_prompt
#         state["status"] = "Redesign prompt generated"
#         print(f"[PROMPT GENERATOR AGENT] Done. Length: {len(generated_prompt)} chars")

#     except Exception as e:
#         state["error"] = f"Prompt generator error: {str(e)}"
#         # Fallback: use basic prompt
#         state["generated_prompt"] = ""
#         state["status"] = "Prompt generation failed — using fallback"
#         print(f"[PROMPT GENERATOR AGENT] ERROR (using fallback): {e}")

#     return state


# def redesign_agent(state: AgentState) -> AgentState:
#     """
#     Node 3: Generate HTML redesign using qwen2.5-coder:7b
#     Uses generated_prompt on first iteration.
#     Uses evaluator feedback on subsequent iterations.
#     """
#     print(f"\n[REDESIGN AGENT] Iteration {state['iteration'] + 1}...")
#     state["status"] = f"Generating redesign (attempt {state['iteration'] + 1})..."

#     try:
#         if state["iteration"] == 0:
#             # First attempt — use the generated prompt
#             if state.get("generated_prompt"):
#                 print("[REDESIGN AGENT] Using AI-generated prompt")
#                 prompt = get_redesign_prompt_from_generated(state["generated_prompt"])
#             else:
#                 print("[REDESIGN AGENT] Using fallback prompt")
#                 prompt = get_redesign_prompt(state["website_data"], state["audit"])
#         else:
#             # Improvement attempt — fix based on evaluator feedback
#             print("[REDESIGN AGENT] Using improvement prompt")
#             prompt = get_redesign_improvement_prompt(
#                 state["website_data"],
#                 state["audit"],
#                 state["html_code"],
#                 state["eval_feedback"]
#             )

#         system = (
#             "You are an expert frontend developer. "
#             "Output ONLY valid HTML code. "
#             "Never add explanations or markdown outside the HTML. "
#             "Start with <!DOCTYPE html> and end with </html>."
#         )

#         response = call_redesign_model(prompt, system)
#         html_code = extract_html(response)

#         state["html_code"] = html_code
#         state["iteration"] = state["iteration"] + 1
#         state["status"] = f"Redesign attempt {state['iteration']} complete"
#         print(f"[REDESIGN AGENT] HTML generated. Length: {len(html_code)} chars")

#     except Exception as e:
#         state["error"] = f"Redesign error: {str(e)}"
#         state["status"] = "Redesign failed"
#         print(f"[REDESIGN AGENT] ERROR: {e}")

#     return state


# def evaluator_agent(state: AgentState) -> AgentState:
#     """Node 4: Evaluate HTML quality — score 1-10, pass if >= 7"""
#     print(f"\n[EVALUATOR AGENT] Evaluating iteration {state['iteration']}...")
#     state["status"] = "Evaluating redesign quality..."

#     try:
#         prompt = get_evaluator_prompt(state["html_code"], state["audit"])
#         system = (
#             "You are a strict quality evaluator. "
#             "Follow the evaluation format exactly. "
#             "Be honest and specific."
#         )
#         response = call_audit_model(prompt, system)
#         parsed = parse_evaluator_response(response)

#         state["eval_score"] = parsed["score"]
#         state["eval_passed"] = parsed["passed"]
#         state["eval_issues"] = parsed["issues"]
#         state["eval_feedback"] = parsed["feedback"]
#         state["status"] = (
#             f"Evaluation: {parsed['score']}/10 — "
#             f"{'Passed' if parsed['passed'] else 'Failed'}"
#         )
#         print(f"[EVALUATOR AGENT] Score: {parsed['score']}/10 | Passed: {parsed['passed']}")

#     except Exception as e:
#         state["eval_score"] = 7
#         state["eval_passed"] = True
#         state["eval_feedback"] = ""
#         state["error"] = f"Evaluator error (auto-passed): {str(e)}"
#         state["status"] = "Evaluator failed — auto passed"
#         print(f"[EVALUATOR AGENT] ERROR (auto-passed): {e}")

#     return state


# # ── ROUTING ──────────────────────────────────────────────────────────────────

# def should_regenerate(state: AgentState) -> str:
#     if state["eval_passed"]:
#         print("[ROUTER] Passed. Finishing.")
#         return "finish"
#     if state["iteration"] >= state["max_iterations"]:
#         print(f"[ROUTER] Max iterations reached. Finishing.")
#         return "finish"
#     print(f"[ROUTER] Failed. Regenerating...")
#     return "regenerate"


# # ── BUILD GRAPH ───────────────────────────────────────────────────────────────

# def build_workflow():
#     """
#     Graph:
#     audit → prompt_generator → redesign → evaluator
#                                   ↑              |
#                                   |  (fail)      |
#                                   └──────────────┘
#                                                  |
#                                           (pass or max)
#                                                  ↓
#                                                 END
#     """
#     graph = StateGraph(AgentState)

#     graph.add_node("audit_agent", audit_agent)
#     graph.add_node("prompt_generator_agent", prompt_generator_agent)
#     graph.add_node("redesign_agent", redesign_agent)
#     graph.add_node("evaluator_agent", evaluator_agent)

#     graph.set_entry_point("audit_agent")

#     graph.add_edge("audit_agent", "prompt_generator_agent")
#     graph.add_edge("prompt_generator_agent", "redesign_agent")
#     graph.add_edge("redesign_agent", "evaluator_agent")

#     graph.add_conditional_edges(
#         "evaluator_agent",
#         should_regenerate,
#         {
#             "regenerate": "redesign_agent",
#             "finish": END
#         }
#     )

#     return graph.compile()


# # ── INITIAL STATE ─────────────────────────────────────────────────────────────

# def create_initial_state(
#     url: str,
#     website_data: str,
#     screenshot_path: str = ""
# ) -> AgentState:
#     return AgentState(
#         url=url,
#         website_data=website_data,
#         screenshot_path=screenshot_path,
#         audit="",
#         generated_prompt="",
#         html_code="",
#         eval_score=0,
#         eval_passed=False,
#         eval_issues="",
#         eval_feedback="",
#         iteration=0,
#         max_iterations=3,
#         status="Starting...",
#         error=""
#     )





# import re
# import json
# from typing import TypedDict
# from langgraph.graph import StateGraph, END

# from backend.utils.ollama_client import call_audit_model, call_redesign_model
# from backend.utils.prompts import (
#     get_audit_prompt,
#     get_redesign_prompt,
#     get_redesign_prompt_from_generated,
#     get_evaluator_prompt,
#     get_redesign_improvement_prompt
# )
# from backend.agents.prompt_generator import run_prompt_generator
# from backend.agents.ui_system_agent import run_ui_system_agent
# from backend.agents.html_refiner import run_html_refiner


# # ── State ────────────────────────────────────────────────────────────────────

# class AgentState(TypedDict):
#     url: str
#     website_data: str
#     screenshot_path: str

#     audit: str
#     generated_prompt: str
#     ui_system: dict
#     html_code: str
#     refined_html: str

#     eval_score: float
#     eval_score_cta: int
#     eval_score_hierarchy: int
#     eval_score_sections: int
#     eval_score_trust: int
#     eval_score_mobile: int
#     eval_passed: bool
#     eval_hard_fail: bool
#     eval_hard_fail_reason: str
#     eval_issues: str
#     eval_feedback: str

#     iteration: int
#     max_iterations: int
#     status: str
#     error: str


# # ── Evaluator parser ─────────────────────────────────────────────────────────

# def parse_evaluator_response(response: str) -> dict:
#     result = {
#         "score": 5.0,
#         "score_cta": 5,
#         "score_hierarchy": 5,
#         "score_sections": 5,
#         "score_trust": 5,
#         "score_mobile": 5,
#         "passed": False,
#         "hard_fail": False,
#         "hard_fail_reason": "None",
#         "issues": "",
#         "feedback": ""
#     }

#     try:
#         def extract(pattern, text, default, cast=str):
#             m = re.search(pattern, text, re.IGNORECASE)
#             if m:
#                 try:
#                     return cast(m.group(1).strip())
#                 except Exception:
#                     return default
#             return default

#         result["score_cta"]       = extract(r"SCORE_CTA:\s*(\d+)", response, 5, int)
#         result["score_hierarchy"] = extract(r"SCORE_HIERARCHY:\s*(\d+)", response, 5, int)
#         result["score_sections"]  = extract(r"SCORE_SECTIONS:\s*(\d+)", response, 5, int)
#         result["score_trust"]     = extract(r"SCORE_TRUST:\s*(\d+)", response, 5, int)
#         result["score_mobile"]    = extract(r"SCORE_MOBILE:\s*(\d+)", response, 5, int)
#         result["score"]           = extract(r"^SCORE:\s*([\d.]+)", response, 5.0, float)
#         result["passed"]          = extract(r"^PASSED:\s*(YES|NO)", response, "NO") == "YES"
#         result["hard_fail"]       = extract(r"HARD_FAIL:\s*(YES|NO)", response, "NO") == "YES"
#         result["hard_fail_reason"]= extract(r"HARD_FAIL_REASON:\s*(.+)", response, "None")

#         issues_m = re.search(
#             r"ISSUES:(.*?)IMPROVEMENT_INSTRUCTIONS:",
#             response, re.DOTALL | re.IGNORECASE
#         )
#         if issues_m:
#             result["issues"] = issues_m.group(1).strip()

#         feedback_m = re.search(
#             r"IMPROVEMENT_INSTRUCTIONS:(.*?)$",
#             response, re.DOTALL | re.IGNORECASE
#         )
#         if feedback_m:
#             result["feedback"] = feedback_m.group(1).strip()

#     except Exception as e:
#         print(f"[EVALUATOR PARSER] Error: {e}")

#     return result


# # ── HTML extractor ────────────────────────────────────────────────────────────

# def extract_html(response: str) -> str:
#     patterns = [
#         r"```html\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
#         r"```\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
#         r"(<!DOCTYPE[\s\S]*?</html>)"
#     ]
#     for pattern in patterns:
#         m = re.search(pattern, response, re.IGNORECASE)
#         if m:
#             return m.group(1).strip()
#     return response.strip()


# # ── NODES ─────────────────────────────────────────────────────────────────────

# def audit_agent(state: AgentState) -> AgentState:
#     print("\n[AUDIT AGENT] Running...")
#     state["status"] = "Generating audit..."
#     try:
#         prompt = get_audit_prompt(state["website_data"])
#         system = (
#             "You are a CRO and UX expert for Indian coaching institutes. "
#             "Be direct and actionable. Follow the format exactly."
#         )
#         state["audit"] = call_audit_model(prompt, system)
#         state["status"] = "Audit complete"
#         print(f"[AUDIT AGENT] Done. {len(state['audit'])} chars")
#     except Exception as e:
#         state["error"] = f"Audit error: {e}"
#         state["audit"] = "Audit generation failed."
#         state["status"] = "Audit failed"
#         print(f"[AUDIT AGENT] ERROR: {e}")
#     return state


# def prompt_generator_agent(state: AgentState) -> AgentState:
#     print("\n[PROMPT GENERATOR] Running...")
#     state["status"] = "Generating redesign strategy prompt..."
#     try:
#         generated = run_prompt_generator(
#             url=state["url"],
#             website_data=state["website_data"],
#             audit=state["audit"],
#             screenshot_path=state.get("screenshot_path", "")
#         )
#         state["generated_prompt"] = generated
#         state["status"] = "Strategy prompt generated"
#         print(f"[PROMPT GENERATOR] Done. {len(generated)} chars")
#     except Exception as e:
#         state["error"] = f"Prompt generator error: {e}"
#         state["generated_prompt"] = ""
#         state["status"] = "Prompt generation failed"
#         print(f"[PROMPT GENERATOR] ERROR: {e}")
#     return state


# def ui_system_agent(state: AgentState) -> AgentState:
#     print("\n[UI SYSTEM AGENT] Running...")
#     state["status"] = "Building UI system specification..."
#     try:
#         ui_system = run_ui_system_agent(
#             generated_prompt=state["generated_prompt"],
#             audit=state["audit"]
#         )
#         state["ui_system"] = ui_system
#         state["status"] = "UI system specification ready"
#         sections = len(ui_system.get("sections", []))
#         print(f"[UI SYSTEM AGENT] Done. {sections} sections defined")
#     except Exception as e:
#         state["error"] = f"UI system error: {e}"
#         state["ui_system"] = {}
#         state["status"] = "UI system failed — using defaults"
#         print(f"[UI SYSTEM AGENT] ERROR: {e}")
#     return state


# def redesign_agent(state: AgentState) -> AgentState:
#     print(f"\n[REDESIGN AGENT] Iteration {state['iteration'] + 1}...")
#     state["status"] = f"Generating redesign (attempt {state['iteration'] + 1})..."

#     try:
#         if state["iteration"] == 0:
#             if state.get("generated_prompt"):
#                 print("[REDESIGN AGENT] Using generated prompt + UI system")
#                 prompt = get_redesign_prompt_from_generated(
#                     state["generated_prompt"],
#                     state.get("ui_system", {})
#                 )
#             else:
#                 print("[REDESIGN AGENT] Using fallback prompt")
#                 prompt = get_redesign_prompt(state["website_data"], state["audit"])
#         else:
#             print("[REDESIGN AGENT] Using improvement prompt")
#             prompt = get_redesign_improvement_prompt(
#                 state["website_data"],
#                 state["audit"],
#                 state["html_code"],
#                 state["eval_feedback"],
#                 state.get("ui_system", {})
#             )

#         system = (
#             "You are an expert frontend developer. "
#             "You must strictly follow the UI system provided. "
#             "Output ONLY valid HTML. No markdown. No explanations. "
#             "Start with <!DOCTYPE html>. End with </html>."
#         )

#         response = call_redesign_model(prompt, system)
#         html = extract_html(response)

#         state["html_code"] = html
#         state["iteration"] = state["iteration"] + 1
#         state["status"] = f"Redesign attempt {state['iteration']} complete"
#         print(f"[REDESIGN AGENT] Done. {len(html)} chars")

#     except Exception as e:
#         state["error"] = f"Redesign error: {e}"
#         state["status"] = "Redesign failed"
#         print(f"[REDESIGN AGENT] ERROR: {e}")

#     return state


# def html_refiner_agent(state: AgentState) -> AgentState:
#     print(f"\n[HTML REFINER] Running on iteration {state['iteration']}...")
#     state["status"] = "Refining and polishing HTML..."

#     try:
#         refined = run_html_refiner(
#             html_code=state["html_code"],
#             ui_system=state.get("ui_system", {})
#         )
#         state["refined_html"] = refined
#         state["html_code"] = refined
#         state["status"] = "HTML refinement complete"
#     except Exception as e:
#         state["error"] = f"Refiner error: {e}"
#         state["refined_html"] = state["html_code"]
#         state["status"] = "HTML refinement failed — using original"
#         print(f"[HTML REFINER] ERROR: {e}")

#     return state


# def evaluator_agent(state: AgentState) -> AgentState:
#     print(f"\n[EVALUATOR] Evaluating iteration {state['iteration']}...")
#     state["status"] = "Evaluating redesign quality..."

#     try:
#         prompt = get_evaluator_prompt(
#             state["html_code"],
#             state["audit"],
#             state.get("ui_system", {})
#         )
#         system = (
#             "You are a strict quality evaluator. "
#             "Follow the evaluation format exactly. "
#             "Output only the specified fields."
#         )
#         response = call_audit_model(prompt, system)
#         parsed = parse_evaluator_response(response)

#         state["eval_score"]           = parsed["score"]
#         state["eval_score_cta"]       = parsed["score_cta"]
#         state["eval_score_hierarchy"] = parsed["score_hierarchy"]
#         state["eval_score_sections"]  = parsed["score_sections"]
#         state["eval_score_trust"]     = parsed["score_trust"]
#         state["eval_score_mobile"]    = parsed["score_mobile"]
#         state["eval_passed"]          = parsed["passed"]
#         state["eval_hard_fail"]       = parsed["hard_fail"]
#         state["eval_hard_fail_reason"]= parsed["hard_fail_reason"]
#         state["eval_issues"]          = parsed["issues"]
#         state["eval_feedback"]        = parsed["feedback"]
#         state["status"] = (
#             f"Eval: {parsed['score']}/10 — "
#             f"CTA:{parsed['score_cta']} "
#             f"Hier:{parsed['score_hierarchy']} "
#             f"Sec:{parsed['score_sections']} "
#             f"Trust:{parsed['score_trust']} "
#             f"Mob:{parsed['score_mobile']} — "
#             f"{'PASSED' if parsed['passed'] else 'FAILED'}"
#         )
#         print(f"[EVALUATOR] {state['status']}")
#         if parsed["hard_fail"]:
#             print(f"[EVALUATOR] HARD FAIL: {parsed['hard_fail_reason']}")

#     except Exception as e:
#         state["eval_score"]    = 7.0
#         state["eval_passed"]   = True
#         state["eval_hard_fail"]= False
#         state["eval_feedback"] = ""
#         state["error"]         = f"Evaluator error (auto-passed): {e}"
#         state["status"]        = "Evaluator failed — auto passed"
#         print(f"[EVALUATOR] ERROR (auto-passed): {e}")

#     return state


# # ── Routing ───────────────────────────────────────────────────────────────────

# def should_regenerate(state: AgentState) -> str:
#     if state["eval_passed"] and not state["eval_hard_fail"]:
#         print("[ROUTER] Passed all checks. Finishing.")
#         return "finish"

#     if state["iteration"] >= state["max_iterations"]:
#         print(f"[ROUTER] Max iterations ({state['max_iterations']}) reached. Finishing.")
#         return "finish"

#     reason = "score too low"
#     if state["eval_hard_fail"]:
#         reason = f"hard fail: {state['eval_hard_fail_reason']}"
#     print(f"[ROUTER] Failed ({reason}). Regenerating — iteration {state['iteration']}")
#     return "regenerate"


# # ── Build graph ───────────────────────────────────────────────────────────────

# def build_workflow():
#     """
#     Full pipeline:
#     audit → prompt_generator → ui_system → redesign → html_refiner → evaluator
#                                                 ↑                          |
#                                                 |     (fail/hard fail)     |
#                                                 └──────────────────────────┘
#                                                                            |
#                                                               (pass or max iter)
#                                                                            ↓
#                                                                           END
#     """
#     graph = StateGraph(AgentState)

#     graph.add_node("audit_agent",            audit_agent)
#     graph.add_node("prompt_generator_agent", prompt_generator_agent)
#     graph.add_node("ui_system_agent",        ui_system_agent)
#     graph.add_node("redesign_agent",         redesign_agent)
#     graph.add_node("html_refiner_agent",     html_refiner_agent)
#     graph.add_node("evaluator_agent",        evaluator_agent)

#     graph.set_entry_point("audit_agent")

#     graph.add_edge("audit_agent",            "prompt_generator_agent")
#     graph.add_edge("prompt_generator_agent", "ui_system_agent")
#     graph.add_edge("ui_system_agent",        "redesign_agent")
#     graph.add_edge("redesign_agent",         "html_refiner_agent")
#     graph.add_edge("html_refiner_agent",     "evaluator_agent")

#     graph.add_conditional_edges(
#         "evaluator_agent",
#         should_regenerate,
#         {
#             "regenerate": "redesign_agent",
#             "finish":     END
#         }
#     )

#     return graph.compile()


# # ── Initial state ─────────────────────────────────────────────────────────────

# def create_initial_state(
#     url: str,
#     website_data: str,
#     screenshot_path: str = ""
# ) -> AgentState:
#     return AgentState(
#         url=url,
#         website_data=website_data,
#         screenshot_path=screenshot_path,
#         audit="",
#         generated_prompt="",
#         ui_system={},
#         html_code="",
#         refined_html="",
#         eval_score=0.0,
#         eval_score_cta=0,
#         eval_score_hierarchy=0,
#         eval_score_sections=0,
#         eval_score_trust=0,
#         eval_score_mobile=0,
#         eval_passed=False,
#         eval_hard_fail=False,
#         eval_hard_fail_reason="None",
#         eval_issues="",
#         eval_feedback="",
#         iteration=0,
#         max_iterations=3,
#         status="Starting...",
#         error=""
#     )


import re
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END

from backend.utils.ollama_client  import call_audit_model, call_evaluator_model
from backend.utils.prompts        import (
    get_audit_prompt,
    get_evaluator_prompt,
    get_redesign_improvement_prompt
)
from backend.agents.template_modifier import run_template_modifier


# ── State ─────────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    url:               str
    website_data:      str
    screenshot_path:   str

    audit:             str
    generated_prompt:  str  # Storing content mapping JSON string here for display
    html_code:         str

    eval_score:           float
    eval_score_cta:       int
    eval_score_hierarchy: int
    eval_score_sections:  int
    eval_score_trust:     int
    eval_score_mobile:    int
    eval_passed:          bool
    eval_hard_fail:       bool
    eval_hard_fail_reason:str
    eval_issues:          str
    eval_feedback:        str

    iteration:         int
    max_iterations:    int
    status:            str
    error:             str


# ── Evaluator parser ──────────────────────────────────────────────────────────

def parse_evaluator_response(response: str) -> dict:
    result = {
        "score": 5.0, "score_cta": 5, "score_hierarchy": 5,
        "score_sections": 5, "score_trust": 5, "score_mobile": 5,
        "passed": False, "hard_fail": False,
        "hard_fail_reason": "None", "issues": "", "feedback": ""
    }

    def extract(pattern, text, default, cast=str):
        m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if m:
            try: return cast(m.group(1).strip())
            except: return default
        return default

    try:
        result["score_cta"]       = extract(r"^SCORE_CTA:\s*(\d+)",       response, 5, int)
        result["score_hierarchy"] = extract(r"^SCORE_HIERARCHY:\s*(\d+)", response, 5, int)
        result["score_sections"]  = extract(r"^SCORE_SECTIONS:\s*(\d+)",  response, 5, int)
        result["score_trust"]     = extract(r"^SCORE_TRUST:\s*(\d+)",     response, 5, int)
        result["score_mobile"]    = extract(r"^SCORE_MOBILE:\s*(\d+)",    response, 5, int)
        result["score"]           = extract(r"^SCORE:\s*([\d.]+)",         response, 5.0, float)
        result["passed"]          = extract(r"^PASSED:\s*(YES|NO)",        response, "NO") == "YES"
        result["hard_fail"]       = extract(r"^HARD_FAIL:\s*(YES|NO)",     response, "NO") == "YES"
        result["hard_fail_reason"]= extract(r"^HARD_FAIL_REASON:\s*(.+)", response, "None")

        issues_m = re.search(
            r"ISSUES:(.*?)IMPROVEMENT_INSTRUCTIONS:", response, re.DOTALL | re.IGNORECASE)
        if issues_m: result["issues"] = issues_m.group(1).strip()

        feedback_m = re.search(
            r"IMPROVEMENT_INSTRUCTIONS:(.*?)$", response, re.DOTALL | re.IGNORECASE)
        if feedback_m: result["feedback"] = feedback_m.group(1).strip()

    except Exception as e:
        print(f"[EVALUATOR PARSER] Error: {e}")

    return result


# ── HTML extractor ────────────────────────────────────────────────────────────

def extract_html(response: str) -> str:
    for pattern in [
        r"```html\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
        r"```\s*(<!DOCTYPE[\s\S]*?</html>)\s*```",
        r"(<!DOCTYPE[\s\S]*?</html>)"
    ]:
        m = re.search(pattern, response, re.IGNORECASE)
        if m: return m.group(1).strip()
    return response.strip()


# ── NODES ─────────────────────────────────────────────────────────────────────

def audit_agent(state: AgentState) -> AgentState:
    print("\n[AUDIT AGENT] Running...")
    state["status"] = "Generating audit..."
    try:
        prompt = get_audit_prompt(state["website_data"])
        system = "You are a CRO expert for Indian coaching institutes. Be direct. Follow the format exactly."
        state["audit"]  = call_audit_model(prompt, system)
        state["status"] = "Audit complete"
        print(f"[AUDIT AGENT] Done. {len(state['audit'])} chars")
    except Exception as e:
        state["error"]  = f"Audit error: {e}"
        state["audit"]  = "Audit generation failed."
        state["status"] = "Audit failed"
        print(f"[AUDIT AGENT] ERROR: {e}")
    return state


def template_modifier_agent(state: AgentState) -> AgentState:
    print(f"\n[TEMPLATE MODIFIER] Iteration {state['iteration'] + 1}...")
    state["status"] = f"Filling template with content (attempt {state['iteration'] + 1})..."

    try:
        previous_values = None
        if state["iteration"] > 0 and state.get("generated_prompt"):
            try:
                previous_values = json.loads(state["generated_prompt"])
            except Exception as e:
                print(f"[TEMPLATE MODIFIER] Error parsing previous values: {e}")

        # Run template modifier (either initial or with feedback refinement)
        html, values_dict = run_template_modifier(
            website_data=state["website_data"],
            audit=state["audit"],
            previous_values=previous_values,
            feedback=state.get("eval_feedback", "")
        )

        state["generated_prompt"] = json.dumps(values_dict, indent=2)
        state["html_code"]  = html
        state["iteration"]  = state["iteration"] + 1
        state["status"]     = f"Template filled (attempt {state['iteration']})"
        print(f"[TEMPLATE MODIFIER] Done. {len(html)} chars")

    except Exception as e:
        state["error"]  = f"Template modifier error: {e}"
        state["status"] = "Template modifier failed"
        print(f"[TEMPLATE MODIFIER] ERROR: {e}")

    return state


# No longer using apply_evaluator_patches with an LLM on the entire HTML code.
# The template is filled deterministically via Python placeholder replacement using refined JSON values.



def evaluator_agent(state: AgentState) -> AgentState:
    print(f"\n[EVALUATOR] Evaluating iteration {state['iteration']}...")
    state["status"] = "Evaluating quality..."
    try:
        prompt   = get_evaluator_prompt(state["html_code"], state["audit"])
        system   = "Strict quality evaluator. Follow the format exactly."
        response = call_evaluator_model(prompt, system)
        parsed   = parse_evaluator_response(response)

        state["eval_score"]            = parsed["score"]
        state["eval_score_cta"]        = parsed["score_cta"]
        state["eval_score_hierarchy"]  = parsed["score_hierarchy"]
        state["eval_score_sections"]   = parsed["score_sections"]
        state["eval_score_trust"]      = parsed["score_trust"]
        state["eval_score_mobile"]     = parsed["score_mobile"]
        state["eval_passed"]           = parsed["passed"]
        state["eval_hard_fail"]        = parsed["hard_fail"]
        state["eval_hard_fail_reason"] = parsed["hard_fail_reason"]
        state["eval_issues"]           = parsed["issues"]
        state["eval_feedback"]         = parsed["feedback"]
        state["status"] = (
            f"Score: {parsed['score']}/10 — "
            f"CTA:{parsed['score_cta']} "
            f"Hier:{parsed['score_hierarchy']} "
            f"Sec:{parsed['score_sections']} "
            f"Trust:{parsed['score_trust']} "
            f"Mob:{parsed['score_mobile']} — "
            f"{'PASSED' if parsed['passed'] else 'FAILED'}"
            + (f" — HARD FAIL: {parsed['hard_fail_reason']}" if parsed["hard_fail"] else "")
        )
        print(f"[EVALUATOR] {state['status']}")

    except Exception as e:
        state["eval_score"]    = 7.0
        state["eval_passed"]   = True
        state["eval_hard_fail"]= False
        state["eval_feedback"] = ""
        state["error"]         = f"Evaluator error (auto-passed): {e}"
        state["status"]        = "Evaluator failed — auto passed"
        print(f"[EVALUATOR] ERROR (auto-passed): {e}")

    return state


# ── Routing ───────────────────────────────────────────────────────────────────

def should_regenerate(state: AgentState) -> str:
    if state["eval_passed"] and not state["eval_hard_fail"]:
        print("[ROUTER] Passed. Finishing.")
        return "finish"
    if state["iteration"] >= state["max_iterations"]:
        print(f"[ROUTER] Max iterations reached. Finishing.")
        return "finish"
    reason = state["eval_hard_fail_reason"] if state["eval_hard_fail"] else "score too low"
    print(f"[ROUTER] Failed ({reason}). Patching — iteration {state['iteration']}")
    return "regenerate"


# ── Build graph ───────────────────────────────────────────────────────────────

def build_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("audit_agent",             audit_agent)
    graph.add_node("template_modifier_agent", template_modifier_agent)
    graph.add_node("evaluator_agent",         evaluator_agent)

    graph.set_entry_point("audit_agent")
    graph.add_edge("audit_agent",             "template_modifier_agent")
    graph.add_edge("template_modifier_agent", "evaluator_agent")

    graph.add_conditional_edges(
        "evaluator_agent",
        should_regenerate,
        {"regenerate": "template_modifier_agent", "finish": END}
    )

    return graph.compile()


# ── Initial state ─────────────────────────────────────────────────────────────

def create_initial_state(
    url: str,
    website_data: str,
    screenshot_path: str = ""
) -> AgentState:
    return AgentState(
        url=url,
        website_data=website_data,
        screenshot_path=screenshot_path,
        audit="",
        generated_prompt="",
        html_code="",
        eval_score=0.0,
        eval_score_cta=0,
        eval_score_hierarchy=0,
        eval_score_sections=0,
        eval_score_trust=0,
        eval_score_mobile=0,
        eval_passed=False,
        eval_hard_fail=False,
        eval_hard_fail_reason="None",
        eval_issues="",
        eval_feedback="",
        iteration=0,
        max_iterations=3,
        status="Starting...",
        error=""
    )