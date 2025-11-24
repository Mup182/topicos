# main.py — versão limpa e sem travamentos
import faulthandler
import logging
import sys

# Habilita faulthandler básico
faulthandler.enable()

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("game")

import arcade
from core.settings import LARGURA, ALTURA, TITULO, DEFAULT_BG_PATH
from views.menu import TelaMenu

def main():
    logger.info("Criando janela")

    janela = arcade.Window(LARGURA, ALTURA, TITULO)

    menu = TelaMenu(
        largura=LARGURA,
        altura=ALTURA,
        bg_path=DEFAULT_BG_PATH
    )

    # Guardamos a referência ao menu para retornar ao final do diálogo
    janela.menu_view = menu

    janela.show_view(menu)

    logger.info("Entrando no loop arcade.run()")

    try:
        arcade.run()
    except Exception:
        logger.exception("Erro em arcade.run():")
    finally:
        logger.info("Saindo...")

if __name__ == "__main__":
    main()
