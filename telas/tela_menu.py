import arcade 

class TelaMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.CORAL
        self.background_image = arcade.texture("./asets/imagens/fundo_menu.png")
        
    def on_draw(self):
       self.clear()
       
       arcade.draw_texture_rect(
           self.background_image,
           arcade.XYWH(540, 120, self.background_image.width, self.background_image.height).scale(0.2)
       )