# core/utils.py
from typing import Optional
import arcade

def safe_load_texture(path: Optional[str]) -> Optional[arcade.Texture]:
    """Tenta carregar uma textura, retorna None se falhar ou caminho for None."""
    if not path:
        return None
    try:
        return arcade.load_texture(path)
    except Exception:
        return None

def fit_font_size_measure(text: str, max_width: int, font_name: str, start_size: int = 36, min_size: int = 10) -> int:
    size = start_size
    has_measure = hasattr(arcade, "get_text_image_dimensions")
    while size >= min_size:
        try:
            if has_measure:
                w, _ = arcade.get_text_image_dimensions(text, size, font_name)
            else:
                w = len(text) * (size * 0.5)
        except Exception:
            w = len(text) * (size * 0.5)
        if w <= max_width - 16:
            return size
        size -= 1
    return min_size
