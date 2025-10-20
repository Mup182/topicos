import arcade 
from telas.tela_menu import TelaMenu


class Janela(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, "Meu joguinho", False)
        self.tela = TelaMenu()
        self.show_view(self.tela)
        
        
def main():
    Janela()
    arcade.run()
if __name__ == "__main__":
    main()