import arcade 
from telas.tela_menu import TelaMenu


class Janela(arcade.Window):
    def __init__(self):
        super().__init__(400, 400, "Meu joguinho", False)
        tela = TelaMenu()
        self.show_view(tela)
        
        
def main():
    Janela()
    arcade.run()
if __name__ == "__main__":
    main()