from typing import Tuple, Union
import win32gui
import win32ui
import win32con
import win32api
from .color import Color

class Canvas:
    def __init__(self, size: Tuple[int, int]):
        self.width = size[0]
        self.height = size[1]
        self.hdc = None
        
    def set_device_context(self, hdc):
        self.hdc = hdc
        win32gui.SetBkMode(self.hdc, win32con.TRANSPARENT)
        
    def clear(self):
        if self.hdc:
            win32gui.FillRect(self.hdc, (0, 0, self.width, self.height), win32gui.GetStockObject(win32con.WHITE_BRUSH))
    
    def _ensure_color(self, color: Union[str, Color]) -> Color:
        if isinstance(color, str):
            return Color(color)
        return color
    
    def draw_rectangle(self, x: int, y: int, width: int, height: int, 
                      color: Union[str, Color], border_radius: int = 0):
        if not self.hdc:
            return
            
        color = self._ensure_color(color)
        brush = win32gui.CreateSolidBrush(color.to_windows_color())
        
        # Se non ci sono bordi arrotondati, usa FillRect standard
        if border_radius == 0:
            win32gui.FillRect(self.hdc, (x, y, x + width, y + height), brush)
        else:
            # Per ora ignoriamo i bordi arrotondati e disegniamo un rettangolo normale
            # In futuro potremmo implementare i bordi arrotondati usando GDI+
            win32gui.FillRect(self.hdc, (x, y, x + width, y + height), brush)
        
        win32gui.DeleteObject(brush)
    
    def draw_text(self, text: str, x: int, y: int, color: Union[str, Color] = None, 
                 font_size: int = 14):
        if not self.hdc:
            return
            
        if color:
            color = self._ensure_color(color)
            win32gui.SetTextColor(self.hdc, color.to_windows_color())
        else:
            win32gui.SetTextColor(self.hdc, 0)  # Nero di default
        
        # Crea un oggetto LOGFONT
        lf = win32gui.LOGFONT()
        lf.lfHeight = font_size
        lf.lfWidth = 0
        lf.lfEscapement = 0
        lf.lfOrientation = 0
        lf.lfWeight = win32con.FW_NORMAL
        lf.lfItalic = False
        lf.lfUnderline = False
        lf.lfStrikeOut = False
        lf.lfCharSet = win32con.ANSI_CHARSET
        lf.lfOutPrecision = win32con.OUT_DEFAULT_PRECIS
        lf.lfClipPrecision = win32con.CLIP_DEFAULT_PRECIS
        lf.lfQuality = win32con.DEFAULT_QUALITY
        lf.lfPitchAndFamily = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE
        lf.lfFaceName = "Arial"
        
        # Crea il font usando l'oggetto LOGFONT
        font = win32gui.CreateFontIndirect(lf)
        old_font = win32gui.SelectObject(self.hdc, font)
        
        try:
            # Calcola le dimensioni del testo
            rect = win32gui.DrawText(
                self.hdc, 
                text, 
                -1, 
                (x, y, x + self.width, y + self.height),
                win32con.DT_CALCRECT | win32con.DT_LEFT | win32con.DT_TOP | 
                win32con.DT_SINGLELINE
            )
            
            # Disegna il testo
            win32gui.DrawText(
                self.hdc, 
                text, 
                -1, 
                (x, y, x + self.width, y + self.height),
                win32con.DT_LEFT | win32con.DT_TOP | win32con.DT_SINGLELINE
            )
        finally:
            win32gui.SelectObject(self.hdc, old_font)
            win32gui.DeleteObject(font)
    
    def update(self):
        pass