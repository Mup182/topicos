# Ecos do Passado - Visual Novel

Protótipo de Visual Novel desenvolvido com Python Arcade.

## Estrutura do Projeto

```
topicos2/
├── core/           # Configurações e utilitários centralizados
├── views/          # Telas do jogo (menu, jogo, diálogos)
├── ui/             # Componentes de interface (botões, etc.)
├── asets/          # Recursos (imagens, sons)
└── main.py         # Ponto de entrada da aplicação
```

## Configuração e Execução

### Requisitos
- Python 3.8+
- Arcade library

### Instalação
```bash
pip install -r requirements.txt
```

### Executar o jogo
```bash
python main.py
```

## Boas Práticas de Layout

### Uso de Constantes Centralizadas

Todas as configurações de layout devem ser definidas em `core/settings.py` para facilitar manutenção e garantir consistência:

```python
# Exemplo: Configurações de caixa de diálogo
DIALOG_BOX_HEIGHT = 180        # Altura da caixa de diálogo
DIALOG_MARGIN_LEFT = 40        # Margem esquerda do texto
DIALOG_MARGIN_RIGHT = 40       # Margem direita do texto
DIALOG_MARGIN_BOTTOM = 40      # Margem inferior do texto
DIALOG_MARGIN_TOP = 20         # Margem superior do texto
```

### Cálculo de Largura Disponível

Sempre calcule a largura disponível para texto subtraindo as margens esquerda e direita:

```python
window_width = self.window.width
largura_disponivel = window_width - DIALOG_MARGIN_LEFT - DIALOG_MARGIN_RIGHT
```

### Posicionamento de Texto

Use as constantes de margem para posicionar elementos:

```python
x = DIALOG_MARGIN_LEFT
y = DIALOG_MARGIN_BOTTOM
```

### Responsividade

O jogo suporta redimensionamento de janela. Implemente o método `on_resize()` nas views para recalcular layouts:

```python
def on_resize(self, width: int, height: int) -> None:
    self.largura = width
    self.altura = height
    self._criar_text_objs()  # Recria objetos de texto com nova largura
```

### Objetos arcade.Text

Use objetos `arcade.Text` pré-criados com parâmetro `width` para quebra automática de linha:

```python
self.text_obj = arcade.Text(
    text,
    x, y,
    color,
    font_size=18,
    width=largura_disponivel,  # Ativa quebra de linha
    anchor_x="left",
    anchor_y="bottom",
    font_name=self.font_name,
)
```

## Convenções de Código

- Use type hints em todas as funções
- Docstrings em português para métodos importantes
- Nomes de variáveis em português (padrão do projeto)
- Prefixo `_` para métodos privados/auxiliares

## Estrutura de Telas

Todas as telas (`View`) devem:
1. Herdar de `arcade.View`
2. Implementar `on_show()`, `on_draw()` e handlers de eventos necessários
3. Armazenar referências para navegação (ex: `self.window.menu_view`)
4. Implementar `on_resize()` para suportar redimensionamento

## Troubleshooting

### Margens não respeitadas
- Verifique se está usando as constantes de `core/settings.py`
- Confirme que o cálculo de largura subtrai ambas as margens
- Certifique-se de que `on_resize()` recria os objetos de texto

### Texto cortado
- Verifique se a largura disponível está sendo calculada corretamente
- Confirme que o objeto `arcade.Text` tem o parâmetro `width` definido
- Aumente as margens se necessário em `settings.py`
