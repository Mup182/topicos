import arcade


class TelaGameplay(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.background_color = arcade.color.WHITE
        
    def on_draw(self):
        self.clear()
        self.spriteList.draw()
        
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if(self.botao1.collides_with_point({x, y})):
            self.window.show_view()