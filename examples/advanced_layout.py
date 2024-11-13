from src import Window, DraggableContainer, Button, Text, Container
from src.layout.constraints import LayoutConstraints, Bounds

def App():
    # Definisci i constraints per diversi widget
    sidebar_constraints = LayoutConstraints(
        bounds=Bounds(0, 0, 200, 600),
        snap_to_grid=True,
        prevent_collision=True,
        min_size=(150, 100),
        max_size=(200, 600)
    )
    
    content_constraints = LayoutConstraints(
        bounds=Bounds(200, 0, 800, 600),
        snap_to_grid=True,
        prevent_collision=True
    )
    
    return Container({
        "children": [
            DraggableContainer({
                "id": "sidebar",
                "draggable": True,
                "constraints": sidebar_constraints,
                "children": [
                    Text("Sidebar"),
                    Button({
                        "text": "Menu Item 1",
                        "variant": "glass"
                    })
                ]
            }),
            DraggableContainer({
                "id": "content",
                "draggable": True,
                "constraints": content_constraints,
                "children": [
                    Text("Draggable Content"),
                    Button({
                        "text": "Click Me!",
                        "variant": "gradient"
                    })
                ]
            })
        ]
    })

window = Window("Advanced Layout", (800, 600))
window.render(App())
window.run() 