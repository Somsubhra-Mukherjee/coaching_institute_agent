import base64
from pathlib import Path


def screenshot_to_base64(screenshot_path: str) -> str:
    """
    Convert a screenshot PNG file to base64 string.
    Returns empty string if file not found.
    """
    path = Path(screenshot_path)

    if not path.exists():
        print(f"[IMAGE UTILS] Screenshot not found: {screenshot_path}")
        return ""

    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        print(f"[IMAGE UTILS] Screenshot encoded. Size: {len(encoded)} chars")
        return encoded
    except Exception as e:
        print(f"[IMAGE UTILS] Error encoding screenshot: {e}")
        return ""


def get_image_size_kb(screenshot_path: str) -> float:
    """Return file size in KB."""
    path = Path(screenshot_path)
    if not path.exists():
        return 0.0
    return path.stat().st_size / 1024