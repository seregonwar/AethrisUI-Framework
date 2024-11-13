import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).parent.parent))

from src import Window, Container, Button, Text, Theme
from src.core.state import State
from src.animation.easing import Easing
from src.feedback.visual_feedback import VisualFeedback, FeedbackEffect
from src.animation.animation import Animation
from src.platform.graphics import Color
from src.styling.theme import Theme

# Configura il tema personalizzato per la calcolatrice
calculator_theme = Theme({
    "primary": "#0D6EFD",
    "secondary": "#6C757D",
    "success": "#198754",
    "error": "#DC3545",
    "warning": "#FFC107"
})

Theme.set_current(calculator_theme)

class CalculatorState:
    def __init__(self):
        self.display = "0"
        self.first_number = None
        self.operation = None
        self.new_number = True
        self._window = None
        
    def set_window(self, window):
        self._window = window
        
    def update_display(self, value):
        self.display = value
        if self._window:
            self._window.render(Calculator(self))
    
    def handle_number(self, num: str):
        def handler():
            logger.debug(f"Clicked number: {num}")
            feedback = VisualFeedback.apply_effect(FeedbackEffect(
                type="highlight",
                color=Color("#4287f5"),
                duration=200,
                intensity=0.8
            ))
            if self.new_number:
                self.update_display(num)
                self.new_number = False
            else:
                if self.display == "0":
                    self.update_display(num)
                else:
                    self.update_display(self.display + num)
        return handler
    
    def handle_operation(self, op: str):
        def handler():
            logger.debug(f"Clicked operation: {op}")
            try:
                self.first_number = float(self.display)
                self.operation = op
                self.new_number = True
            except ValueError:
                self.update_display("Error")
        return handler
    
    def handle_equals(self):
        logger.debug("Clicked equals")
        if self.operation is None or self.first_number is None:
            return
            
        try:
            second_number = float(self.display)
            result = 0
            
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "×":
                result = self.first_number * second_number
            elif self.operation == "÷":
                if second_number != 0:
                    result = self.first_number / second_number
                else:
                    self.update_display("Error")
                    return
            
            # Formatta il risultato
            if result.is_integer():
                self.update_display(str(int(result)))
            else:
                self.update_display(f"{result:.8f}".rstrip('0').rstrip('.'))
            
            self.operation = None
            self.first_number = None
            self.new_number = True
            
        except ValueError:
            self.update_display("Error")
    
    def handle_decimal(self):
        logger.debug("Clicked decimal")
        if "." not in self.display:
            self.update_display(self.display + ".")
            self.new_number = False
    
    def handle_clear(self):
        logger.debug("Clicked clear")
        self.update_display("0")
        self.first_number = None
        self.operation = None
        self.new_number = True

def Calculator(state=None):
    if state is None:
        state = CalculatorState()
    
    # Stili base per i bottoni (solo proprietà supportate)
    button_base_style = {
        "width": "65px", 
        "height": "65px",
        "margin": "4px",
        "border_radius": "12px",
        "font_size": "22px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
    }
    
    number_button_style = {
        **button_base_style,
        "background": "#F8F9FA",
        "color": "#212529"
    }
    
    operator_button_style = {
        **button_base_style,
        "background": Theme.current.colors["primary"],
        "color": "#FFFFFF"
    }
    
    # Display semplificato con stili supportati
    display_style = {
        "width": "300px",
        "height": "90px", 
        "background": "#F8F9FA",
        "border": "2px solid #E9ECEF",
        "border_radius": "16px",
        "margin": "15px",
        "padding": "20px",
        "display": "flex",
        "justify_content": "flex_end",
        "align_items": "center",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.05)"
    }
    
    # Layout della calcolatrice
    calculator = Container({
        "children": [
            # Display
            Container({
                "children": [
                    Text(state.display, {
                        "font_size": "40px",
                        "font_family": "Consolas",
                        "color": "#212529"
                    })
                ],
                "style": display_style
            }),
            
            # Pulsante Clear
            Container({
                "children": [
                    Button({
                        "text": "C",
                        "onClick": state.handle_clear,
                        "style": {
                            **button_base_style,
                            "background": Theme.current.colors["error"],
                            "color": "#FFFFFF",
                            "width": "300px",
                            "height": "60px"
                        }
                    })
                ],
                "style": {
                    "display": "flex",
                    "flex_direction": "row",
                    "justify_content": "space_between",
                    "width": "300px"
                }
            }),
            
            # Prima riga: C
            Container({
                "children": [
                    Button({
                        "text": "7",
                        "onClick": state.handle_number("7"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "8",
                        "onClick": state.handle_number("8"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "9",
                        "onClick": state.handle_number("9"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "÷",
                        "onClick": state.handle_operation("÷"),
                        "style": operator_button_style
                    })
                ],
                "style": {
                    "display": "flex",
                    "flex_direction": "row",
                    "justify_content": "space_between",
                    "width": "300px"
                }
            }),
            
            # Seconda riga: 4 5 6 ×
            Container({
                "children": [
                    Button({
                        "text": "4",
                        "onClick": state.handle_number("4"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "5",
                        "onClick": state.handle_number("5"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "6",
                        "onClick": state.handle_number("6"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "×",
                        "onClick": state.handle_operation("×"),
                        "style": operator_button_style
                    })
                ],
                "style": {
                    "display": "flex",
                    "flex_direction": "row",
                    "justify_content": "space_between",
                    "width": "300px"
                }
            }),
            
            # Terza riga: 1 2 3 -
            Container({
                "children": [
                    Button({
                        "text": "1",
                        "onClick": state.handle_number("1"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "2",
                        "onClick": state.handle_number("2"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "3",
                        "onClick": state.handle_number("3"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": "-",
                        "onClick": state.handle_operation("-"),
                        "style": operator_button_style
                    })
                ],
                "style": {
                    "display": "flex",
                    "flex_direction": "row",
                    "justify_content": "space_between",
                    "width": "300px"
                }
            }),
            
            # Quarta riga: 0 . = +
            Container({
                "children": [
                    Button({
                        "text": "0",
                        "onClick": state.handle_number("0"),
                        "style": number_button_style
                    }),
                    Button({
                        "text": ".",
                        "onClick": state.handle_decimal,
                        "style": number_button_style
                    }),
                    Button({
                        "text": "=",
                        "onClick": state.handle_equals,
                        "style": {
                            **button_base_style,
                            "background": Theme.current.colors["success"],
                            "color": "#FFFFFF"
                        }
                    }),
                    Button({
                        "text": "+",
                        "onClick": state.handle_operation("+"),
                        "style": operator_button_style
                    })
                ],
                "style": {
                    "display": "flex",
                    "flex_direction": "row",
                    "justify_content": "space_between",
                    "width": "300px"
                }
            })
        ],
        "style": {
            "width": "330px",
            "background": "#FFFFFF", 
            "border": "2px solid #E9ECEF",
            "border_radius": "24px",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.1)",
            "margin": "20px auto",
            "padding": "15px"
        }
    })
    
    return calculator

def main():
    try:
        logger.debug("Creating window...")
        window = Window("AethrisUI Calculator", (360, 600))
        
        # Crea lo stato e passa il riferimento alla finestra
        calculator_state = CalculatorState()
        calculator_state.set_window(window)
        
        logger.debug("Rendering application...")
        window.render(Calculator(calculator_state))
        
        logger.debug("Starting main loop...")
        window.run()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 