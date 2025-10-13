import arcade 

class TelaMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.WHITE
        self.spriteList = arcade.SpriteList()


        self.background_image = arcade.Sprite("./asets/imagens/download.png",
                                             
                                              center_x=self.window.width // 2,
                                              center_y=self.window.width // 2
                                              )
        
        self.spriteList.append(self.background_image)
        #self.botao1 = arcade.Sprite(" ./asets/imagens/retangulo.png")
        #self.spriteList.append(self.botao1)

        def on_draw(self):
            self.clear()
            self.spriteList.draw()
        






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
       