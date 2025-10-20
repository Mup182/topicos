import arcade 
from telas.tela_gameplay import TelaGameplay
class TelaMenu(arcade.View): 
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.WHITE
        self.spriteList = arcade.SpriteList()


        self.background_image = arcade.Sprite("./asets/imagens/space.jpg",
                                             
                                              center_x=self.window.width // 2
                                              ,
                                              center_y=self.window.width // 2,
                                              scale=2
                                              )
        
        self.spriteList.append(self.background_image)
        self.botao1 = arcade.Sprite(" ./asets/imagens/botao.png",
                                            center_x=self.window.width // 2,
                                              center_y=self.window.width // 4-100,
                                              scale=0.20
                                              )
        self.spriteList.append(self.botao1)
        
        
        self.botao2 = arcade.Sprite(" ./asets/imagens/botao.png",
                                            center_x=self.window.width // 2,
                                              center_y=self.window.width // 4-200,
                                              scale=0.20
                                              )
        self.spriteList.append(self.botao2)
        
        self.botao3 = arcade.Sprite(" ./asets/imagens/botao.png",
                                            center_x=self.window.width // 2,
                                              center_y=self.window.width // 4-300,
                                              scale=0.20
                                              )
        self.spriteList.append(self.botao3)

    def on_draw(self):
        self.clear()
        self.spriteList.draw()
        
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if(self.botao1.collides_with_point({x, y})):
          proxTela = TelaGameplay()
          self.window.show_view(proxTela)
          print("Botão clicado")
          
          
        return super().on_mouse_press(x, y, button, modifiers)
        
        
        






'''class TelaMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.CORAL
        self.background_image = arcade.texture("./asets/imagens/fundo_menu.png")
        
    def on_draw(self):
       self.clear()
       
       arcade.draw_texture_rect(
           self.background_image,
           arcade.XYWH(540, 120, self.background_image.width, self.background_image.height).scale(0.2)
       )'''
       