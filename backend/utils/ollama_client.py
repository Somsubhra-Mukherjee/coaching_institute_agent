import ollama
import time


AUDIT_MODEL = "llama3.1:8b"
REDESIGN_MODEL = "qwen2.5-coder:7b"


def call_ollama(model: str, prompt: str, system: str = "", max_retries: int = 3) -> str:
    """
    Call a local Ollama model and return the response text.
    Retries up to max_retries times on failure.
    """
    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": prompt})

    for attempt in range(max_retries):
        try:
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
            print(f"[OLLAMA] Response received. Length: {len(result)} chars")
            return result

        except Exception as e:
            print(f"[OLLAMA] Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError(f"Ollama call failed after {max_retries} attempts: {e}")


def call_audit_model(prompt: str, system: str = "") -> str:
    return call_ollama(AUDIT_MODEL, prompt, system)


def call_redesign_model(prompt: str, system: str = "") -> str:
    return call_ollama(REDESIGN_MODEL, prompt, system)