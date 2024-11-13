from src import Window, DraggableContainer, Button, Text, Theme, Container
from src.styling.effects import ModernEffects

def App():
    return Container({
        "children": [
            DraggableContainer({
                "draggable": True,
                "children": [
                    Text("Drag me!"),
                    Button({
                        "text": "Click Me!",
                        "variant": "glass",
                        "effect": "glow"
                    })
                ],
                "style": ModernEffects.glass()
            }),
            DraggableContainer({
                "draggable": True,
                "children": [
                    Text("Another draggable container"),
                    Button({
                        "text": "Settings",
                        "variant": "gradient"
                    })
                ],
                "style": {
                    **ModernEffects.glass(),
                    "left": "200px",
                    "top": "100px"
                }
            }),
            # Container fisso
            Container({
                "children": [
                    Text("I can't be moved"),
                    Button({
                        "text": "Static Button",
                        "variant": "filled"
                    })
                ],
                "style": {
                    "position": "absolute",
                    "right": "20px",
                    "bottom": "20px"
                }
            })
        ]
    })

window = Window("Draggable Layout", (800, 600))
window.render(App())
window.run()