import arcade

class TelaJogo2(arcade.View):

    def __init__(self):
        super().__init__()
        
        self.spritelist = arcade.SpriteList()

        fundo = arcade.Sprite("./asets/imagens/fundo_menu.jpg",
                              scale=0.8,
                              center_x=self.window.width // 2,
                              center_y=self.window.height // 2)
        self.spritelist.append(fundo)

        
        self.ordem_itens = [self.item1]
        self.ordem_index = 0
        
        self.dialogo_index = 0
        self.dialogo_ativo = True
        
        #ordem_index = 0
        self.dialogo_texto = [["Ache o filhote"]] 
        #ordem_index = 1
        self.dialogo_texto.append(["Enquanto explorava cautelosamente o terreno, o filhote percebeu algo se mexendo perto...",
                                   "de um rio lamacento que caminhava pelo lixão."])
        #ordem_index = 2
        self.dialogo_texto.append(["Era uma barata, deslizando lentamente entre os detritos e refletindo à luz cinzenta do dia.", 
                                   "O gato, curioso e faminto, aproximou-se devagar.",
                                   "Cada passo seu afundava um pouco na lama, mas o instinto de sobrevivência era mais forte...",
                                   "que o medo.",
                                   "Mais adiante, o cheiro forte chamou sua atenção perto do rio."])
        #ordem_index = 3
        self.dialogo_texto.append(["Entre o despejo do esgoto e restos de pneus, um peixe morto jazia à beira da água.",
                                   "Ele estava coberto de lama e moscas, mas para o filhote era uma refeição preciosa.",
                                   "Hesitante no começo, o gato se aproximou, cheirou e deu pequenas mordidas",
                                    "recuperando forças aos poucos."])
        


      

    def on_draw(self):
        self.clear()
        self.spritelist.draw()

        if self.dialogo_ativo:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                top=70,
                bottom=0,
                color=(0, 0, 0, 170)
            )

            arcade.draw_text(
                self.dialogo_texto[self.ordem_index][self.dialogo_index],
                20,
                20,
                arcade.color.WHITE,
                font_size=14,
                width=self.window.width - 40
            )
            if self.dialogo_index >= len(self.dialogo_texto[self.ordem_index])-1:
                arcade.draw_text(
                    "Procure...",
                    5,
                    5,
                    arcade.color.WHITE,
                    font_size=10,
                    width=self.window.width - 40,
                    align="right",
                    anchor_x="right"
                )
            else:
                self.icones.draw()

        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.ordem_itens[self.ordem_index].collides_with_point((x, y)) and self.dialogo_index>=len(self.dialogo_texto[self.ordem_index])-1: # só pode clicar se terminou o diálogo
            self.click.play(volume=0.5, loop=False)
            if self.ordem_index < len(self.ordem_itens)-1:
                self.ordem_index+=1
                self.dialogo_index=0

        elif self.dialogo_index < len(self.dialogo_texto[self.ordem_index])-1:
            self.dialogo_index+=1
        
        
