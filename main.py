# main.py — FULLSCREEN FIX + VIEWPORT AUTO-SCALE (Arcade 2.6.17)
import faulthandler
import logging
import sys

faulthandler.enable()

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

    # 1 — criamos a janela em FULLSCREEN
    janela = arcade.Window(
        LARGURA,
        ALTURA,
        TITULO,
        fullscreen=True,
        resizable=True
    )

    # 2 — pegamos o tamanho REAL da tela
    largura_real, altura_real = janela.get_size()

    # 3 — configuramos escala do viewport para ocupar a tela inteira
    janela.set_viewport(0, largura_real, 0, altura_real)

    # 4 — criamos o menu usando o tamanho real do monitor
    menu = TelaMenu(
        largura=largura_real,
        altura=altura_real,
        bg_path=DEFAULT_BG_PATH
    )

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
