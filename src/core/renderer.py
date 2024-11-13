from typing import Dict, Any, Optional, Tuple, List
from .virtual_node import VirtualNode
from ..platform.graphics import Canvas, Color
from ..styling.units import parse_unit, parse_padding
import logging
import win32gui
import win32con
import uuid

logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self._current_tree: Optional[VirtualNode] = None
        self._node_positions = {}  # Memorizza le posizioni dei nodi per gli eventi
        self._hovered_node = None
        self._active_node = None
        self._window = None  # Riferimento alla finestra per il re-rendering
        logger.debug("Renderer initialized")
    
    def set_window(self, window):
        """Imposta il riferimento alla finestra per il re-rendering"""
        self._window = window
    
    def render(self, node: VirtualNode):
        try:
            logger.debug(f"Rendering node of type: {node.component_type}")
            self._current_tree = node
            self._node_positions.clear()
            self.canvas.clear()
            self._render_node(node)
            self.canvas.update()
        except Exception as e:
            logger.error(f"Error in render: {str(e)}", exc_info=True)
            raise
    
    def handle_click(self, x: int, y: int):
        """Gestisce i click cercando il nodo cliccato"""
        for node_id, (node, pos_x, pos_y, width, height) in self._node_positions.items():
            if (pos_x <= x <= pos_x + width and 
                pos_y <= y <= pos_y + height):
                if "onClick" in node.props:
                    # Esegui il callback
                    node.props["onClick"]()
                    # Forza il re-rendering
                    if self._window and hasattr(self._window, '_current_node'):
                        self._window.render(self._window._current_node)
                    return True
        return False
    
    def handle_mouse_move(self, x: int, y: int):
        """Gestisce il movimento del mouse per gli effetti hover"""
        old_hovered = self._hovered_node
        self._hovered_node = None
        
        for node_id, (node, pos_x, pos_y, width, height) in self._node_positions.items():
            if (pos_x <= x <= pos_x + width and 
                pos_y <= y <= pos_y + height):
                self._hovered_node = node
                break
        
        if old_hovered != self._hovered_node:
            self.render(self._current_tree)  # Re-render per aggiornare lo stato hover
    
    def _render_node(self, node: VirtualNode, parent_pos: Tuple[int, int] = (0, 0)):
        try:
            style = node.props.get("style", {})
            x = parent_pos[0] + self._get_style_value(style, "left", 0)
            y = parent_pos[1] + self._get_style_value(style, "top", 0)
            width = self._get_style_value(style, "width", 100)
            height = self._get_style_value(style, "height", 30)
            
            # Memorizza la posizione del nodo per gli eventi usando un ID univoco
            if "onClick" in node.props:
                node_id = str(uuid.uuid4())
                self._node_positions[node_id] = (node, x, y, width, height)
            
            if node.component_type == "text":
                self._render_text(node, (x, y))
            elif node.component_type == "button":
                self._render_button(node, (x, y))
            elif node.component_type == "container":
                self._render_container(node, (x, y))
                
        except Exception as e:
            logger.error(f"Error rendering node {node.component_type}: {str(e)}", exc_info=True)
            raise
    
    def _render_text(self, node: VirtualNode, pos):
        style = node.props.get("style", {})
        text = str(node.props.get("text", ""))
        font_size = self._get_style_value(style, "font_size", 14)
        self.canvas.draw_text(text, pos[0], pos[1], style.get("color"), font_size)
    
    def _render_button(self, node: VirtualNode, pos):
        style = node.props.get("style", {}).copy()
        
        # Applica stili hover se il nodo è hovered
        if node == self._hovered_node:
            hover_style = style.get("hover", {})
            style.update(hover_style)
            # Modifica il colore di sfondo per l'effetto hover
            if "background" in style:
                try:
                    # Se il background è un colore del tema
                    if isinstance(style["background"], dict) and "color" in style["background"]:
                        bg_color = Color(style["background"]["color"])
                    else:
                        bg_color = Color(style["background"])
                    style["background"] = bg_color.lighten(0.1).to_hex()
                except ValueError:
                    # Se non riusciamo a parsare il colore, usiamo quello originale
                    pass
        
        # Applica stili active se il nodo è cliccato
        if node == self._active_node:
            active_style = style.get("active", {})
            style.update(active_style)
            # Aggiunge un'ombra più profonda per l'effetto pressed
            style["box_shadow"] = "inset 0 2px 4px rgba(0,0,0,0.2)"
        
        text = str(node.props.get("text", ""))
        
        width = self._get_style_value(style, "width", 60)
        height = self._get_style_value(style, "height", 60)
        margin = self._get_style_value(style, "margin", 5)
        
        # Applica il margine
        x = pos[0] + margin
        y = pos[1] + margin
        
        # Disegna lo sfondo del pulsante
        background_color = style.get("background", "#CCCCCC")
        if isinstance(background_color, dict) and "color" in background_color:
            background_color = background_color["color"]
            
        self.canvas.draw_rectangle(
            x, y, width, height,
            background_color
        )
        
        # Disegna il testo del pulsante centrato
        text_x = x + (width - len(text) * 8) // 2
        text_y = y + (height - 16) // 2
        text_color = style.get("color", "#000000")
        if isinstance(text_color, dict) and "color" in text_color:
            text_color = text_color["color"]
        self.canvas.draw_text(text, text_x, text_y, text_color)
    
    def _get_style_value(self, style: Dict[str, Any], key: str, default: int = 0) -> int:
        if key not in style:
            return default
        return parse_unit(style[key])
    
    def _render_container(self, node: VirtualNode, parent_pos: Tuple[int, int]):
        style = node.props.get("style", {})
        width = self._get_style_value(style, "width", self.canvas.width)
        height = self._get_style_value(style, "height", self.canvas.height)
        padding = self._get_style_value(style, "padding", 0)
        
        # Disegna il background se presente
        if "background" in style:
            self.canvas.draw_rectangle(
                parent_pos[0], parent_pos[1], width, height,
                style["background"]
            )
        
        if node.children:
            # Calcola le posizioni dei figli
            child_positions = []
            current_x = parent_pos[0] + padding
            current_y = parent_pos[1] + padding
            
            for child in node.children:
                child_style = child.props.get("style", {})
                child_width = self._get_style_value(child_style, "width", 60)
                child_margin = self._get_style_value(child_style, "margin", 5)
                
                # Se il figlio non entra nella riga corrente, vai a capo
                if current_x + child_width + child_margin > parent_pos[0] + width - padding:
                    current_x = parent_pos[0] + padding
                    current_y += 70  # Altezza standard + margine
                
                child_positions.append((current_x, current_y))
                current_x += child_width + child_margin * 2
            
            # Renderizza i figli nelle posizioni calcolate
            for child, pos in zip(node.children, child_positions):
                self._render_node(child, pos)