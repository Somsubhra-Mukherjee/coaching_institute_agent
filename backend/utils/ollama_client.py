import os
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"

# Models configuration
OLLAMA_AUDIT_MODEL = os.getenv("OLLAMA_AUDIT_MODEL", "llama3.1:8b")
OLLAMA_CONTENT_MODEL = os.getenv("OLLAMA_CONTENT_MODEL", "qwen2.5-coder:7b")
OLLAMA_EVALUATOR_MODEL = os.getenv("OLLAMA_EVALUATOR_MODEL", "llama3.1:8b")

GROQ_AUDIT_MODEL = os.getenv("GROQ_AUDIT_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
GROQ_CONTENT_MODEL = os.getenv("GROQ_CONTENT_MODEL", "qwen/qwen3-32b")
GROQ_EVALUATOR_MODEL = os.getenv("GROQ_EVALUATOR_MODEL", "llama-3.1-8b-instant")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Track which service we're using
USING_GROQ = False


def call_groq(prompt: str, system: str = "", model_override: str = None) -> str:
    """
    Call Groq API. Automatically tries fallback models if the primary model
    fails with rate limits (429), context limit/request too large (413), or other errors.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set in .env")

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

    primary_model = model_override or GROQ_DEFAULT_MODEL

    # List of models to try in sequence
    models_to_try = [primary_model]
    fallbacks = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for f in fallbacks:
        if f not in models_to_try:
            models_to_try.append(f)

    # Character limits for each model to avoid TPM limits and 413s
    model_caps = {
        "meta-llama/llama-4-scout-17b-16e-instruct": 12_000,
        "qwen/qwen3-32b": 12_000,
        "llama-3.3-70b-versatile": 12_000,
        "llama-3.1-8b-instant": 6_000,
    }

    last_error = None
    for model_name in models_to_try:
        # Determine prompt size for this model
        cap = model_caps.get(model_name, 15_000)
        system_chars = len(system)
        available = cap - system_chars
        
        current_prompt = prompt
        if len(prompt) > available:
            print(f"[GROQ] Prompt too long for {model_name} ({len(prompt)} chars) — truncating to {available} chars")
            current_prompt = prompt[:available] + "\n\n[... content truncated to fit model limit ...]"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": current_prompt})

        max_attempts = 2
        for attempt in range(max_attempts):
            try:
                print(f"[GROQ] Calling Groq model: {model_name} (attempt {attempt + 1})")
                current_max_tokens = 3000 if "qwen" in model_name or "scout" in model_name else 1500
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=current_max_tokens,
                    top_p=0.9,
                )
                result = response.choices[0].message.content
                print(f"[GROQ] Response received from {model_name}. {len(result)} chars (~{len(result)//4} tokens)")

                global USING_GROQ
                USING_GROQ = True
                return result

            except Exception as e:
                err_str = str(e).lower()
                last_error = e
                print(f"[GROQ] Error with model {model_name} (attempt {attempt + 1}): {e}")

                # If it's a 413 (request too large / entity too large), do NOT retry this model. Fall back immediately.
                if "413" in err_str or "too_large" in err_str or "entity too large" in err_str or "request too large" in err_str:
                    print(f"[GROQ] Request too large (413) for {model_name}. Switching to next model...")
                    break  # Break out of attempts loop to try next model

                # For 429 or rate limits, if we have attempts left, sleep and retry.
                # Otherwise, fall back to next model.
                if ("rate_limit" in err_str or "limit" in err_str or "429" in err_str) and attempt < max_attempts - 1:
                    print(f"[GROQ] Rate limit hit. Sleeping 5s before retry...")
                    time.sleep(5)
                else:
                    print(f"[GROQ] Moving to next fallback model...")
                    break

    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")


def call_ollama(model: str, prompt: str, system: str = "", max_retries: int = 1) -> str:
    """
    Call a local Ollama model and return the response text.
    If Ollama fails, falls back to Groq.
    """
    if not OLLAMA_ENABLED:
        # Determine appropriate Groq model override based on the Ollama model requested
        groq_model = None
        if model == OLLAMA_AUDIT_MODEL:
            groq_model = GROQ_AUDIT_MODEL
        elif model == OLLAMA_CONTENT_MODEL:
            groq_model = GROQ_CONTENT_MODEL
        elif model == OLLAMA_EVALUATOR_MODEL:
            groq_model = GROQ_EVALUATOR_MODEL

        print(f"[OLLAMA] Disabled. Using Groq ({groq_model or GROQ_DEFAULT_MODEL}) instead.")
        return call_groq(prompt, system, model_override=groq_model)

    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    for attempt in range(max_retries):
        try:
            import ollama
            print(f"[OLLAMA] Calling model: {model} (attempt {attempt + 1})")
            response = ollama.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "num_predict": 4096,
                    "top_p": 0.9,
                }
            )
            result = response["message"]["content"]
            estimated_tokens = len(result) // 4
            print(f"[OLLAMA] Response received. Length: {len(result)} chars (~{estimated_tokens} tokens)")
            return result

        except Exception as e:
            print(f"[OLLAMA] Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                groq_model = None
                if model == OLLAMA_AUDIT_MODEL:
                    groq_model = GROQ_AUDIT_MODEL
                elif model == OLLAMA_CONTENT_MODEL:
                    groq_model = GROQ_CONTENT_MODEL
                elif model == OLLAMA_EVALUATOR_MODEL:
                    groq_model = GROQ_EVALUATOR_MODEL
                
                print(f"[OLLAMA] Failed. Falling back to Groq ({groq_model or GROQ_DEFAULT_MODEL})...")
                return call_groq(prompt, system, model_override=groq_model)


def call_audit_model(prompt: str, system: str = "") -> str:
    return call_ollama(OLLAMA_AUDIT_MODEL, prompt, system)


def call_redesign_model(prompt: str, system: str = "") -> str:
    return call_ollama(OLLAMA_CONTENT_MODEL, prompt, system)


def call_evaluator_model(prompt: str, system: str = "") -> str:
    return call_ollama(OLLAMA_EVALUATOR_MODEL, prompt, system)