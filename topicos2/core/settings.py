# core/settings.py
import os

# BASE_DIR points to the project root (one level up from core/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LARGURA = 1280
ALTURA = 720
TITULO = "Ecos do Passado - Protótipo"

DEFAULT_BG_PATH = os.path.join(BASE_DIR, "asets", "imagens", "fundo_menu.jpg")
if not os.path.exists(DEFAULT_BG_PATH):
    alt = os.path.join(BASE_DIR, "fundo_menu.jpg")
    DEFAULT_BG_PATH = alt if os.path.exists(alt) else None

CLICK_SOUND_PATH = os.path.join(BASE_DIR, "asets", "imagens", "click.wav")

# Colors
COR_TEXTO = (140, 140, 140, 255)
COR_BOTAO = (50, 50, 50, 255)
COR_HOVER = (100, 110, 150, 255)
COR_SOMBRA = (20, 20, 20, 180)
COR_FUNDO_JOGO = (60, 50, 40, 255)

# Dialog box layout settings
DIALOG_BOX_HEIGHT = 180  # Height of the dialog box from bottom
DIALOG_MARGIN_LEFT = 40  # Left margin for dialog text
DIALOG_MARGIN_RIGHT = 40  # Right margin for dialog text
DIALOG_MARGIN_BOTTOM = 40  # Bottom margin for dialog text (increased from 28 for better spacing)
DIALOG_MARGIN_TOP = 20  # Top margin for dialog text within the box
