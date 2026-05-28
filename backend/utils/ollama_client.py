import os
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"

AUDIT_MODEL = "llama3.1:8b"
REDESIGN_MODEL = "qwen2.5-coder:7b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Track which service we're using
USING_OPENAI = False
USING_GROQ = False


def call_openai(prompt: str, system: str = "") -> str:
    """
    Call OpenAI's API using gpt-4o-mini.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in .env file")

    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    try:
        print(f"[GPT] Calling OpenAI model: {OPENAI_MODEL}")
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
            top_p=0.9,
        )
        result = response.choices[0].message.content
        estimated_tokens = len(result) // 4
        print(f"[GPT] Response received. Length: {len(result)} chars (~{estimated_tokens} tokens)")
        return result

    except Exception as e:
        print(f"[GPT] Error: {e}")
        raise RuntimeError(f"OpenAI call failed: {e}")


def call_groq(prompt: str, system: str = "") -> str:
    """
    Call Groq API. Truncates input to stay within free-tier TPM limits.
    gemma2-9b-it has 15k TPM; we reserve ~4k for output → cap input at ~11k tokens (~44k chars).
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set in .env")

    # Rough truncation: 1 token ≈ 4 chars. Cap total input at ~44k chars (~11k tokens).
    MAX_INPUT_CHARS = 44_000
    system_chars = len(system)
    available = MAX_INPUT_CHARS - system_chars
    if len(prompt) > available:
        print(f"[GROQ] Prompt too long ({len(prompt)} chars) — truncating to {available} chars")
        prompt = prompt[:available] + "\n\n[... content truncated to fit model limit ...]"

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        print(f"[GROQ] Calling Groq model: {GROQ_MODEL}")
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
            top_p=0.9,
        )
        result = response.choices[0].message.content
        print(f"[GROQ] Response received. {len(result)} chars (~{len(result)//4} tokens)")

        global USING_GROQ, USING_OPENAI
        USING_GROQ = True
        USING_OPENAI = False
        return result

    except Exception as e:
        print(f"[GROQ] Error: {e}")
        raise RuntimeError(f"Groq call failed: {e}")


def call_ollama(model: str, prompt: str, system: str = "", max_retries: int = 1) -> str:
    """
    Call a local Ollama model and return the response text.
    If Ollama fails, falls back to OpenAI.
    """
    if not OLLAMA_ENABLED:
        print("[OLLAMA] Disabled. Using Groq instead.")
        return call_groq(prompt, system)

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
            global USING_OPENAI
            USING_OPENAI = False
            return result

        except Exception as e:
            print(f"[OLLAMA] Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print("[OLLAMA] Failed. Falling back to Groq...")
                return call_groq(prompt, system)


def call_audit_model(prompt: str, system: str = "") -> str:
    return call_ollama(AUDIT_MODEL, prompt, system)


def call_redesign_model(prompt: str, system: str = "") -> str:
    return call_ollama(REDESIGN_MODEL, prompt, system)