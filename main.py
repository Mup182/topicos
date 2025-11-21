# main.py
import arcade
from core.settings import LARGURA, ALTURA, TITULO, DEFAULT_BG_PATH
from views.menu import TelaMenu

def main():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    menu = TelaMenu(LARGURA, ALTURA, bg_path=DEFAULT_BG_PATH)
    janela.menu_view = menu
    janela.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
