"""
PyQt6 Comic Book Theme - Style Examples
This shows how the CSS translates to Qt Style Sheets (QSS)
"""

# Color Palette
COMIC_COLORS = {
    # Primary banner
    'banner_red': '#E63946',
    'banner_red_dark': '#C81F2A',
    'banner_yellow': '#FFD60A',

    # Character portrait frames
    'portrait_teal': '#2A9D8F',
    'portrait_teal_dark': '#1A7A6E',
    'portrait_border': '#264653',

    # Panels and backgrounds
    'panel_cream': '#F4E8D8',
    'panel_pink': '#F4ACB7',
    'panel_orange': '#F4A261',
    'panel_mustard': '#E9C46A',

    # Text and outlines
    'comic_black': '#1A1A1A',
    'text_dark': '#264653',
    'speech_bubble_white': '#FFFFFF',
    'speech_outline': '#1A1A1A',

    # Shadows
    'shadow': 'rgba(0, 0, 0, 0.3)',
}


# ============================================================================
# BANNER STYLING (Top red banner with yellow text)
# ============================================================================

BANNER_STYLE = f"""
QWidget#banner {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {COMIC_COLORS['banner_red']},
        stop:1 {COMIC_COLORS['banner_red_dark']}
    );
    border: 4px solid {COMIC_COLORS['comic_black']};
    border-radius: 8px 8px 0px 0px;
    padding: 20px;
}}

QLabel#banner_title {{
    font-family: "Bangers", "Impact", sans-serif;
    font-size: 40px;
    font-weight: bold;
    color: {COMIC_COLORS['banner_yellow']};
    letter-spacing: 3px;
    padding: 10px;
}}

QLabel#banner_subtitle {{
    font-family: "Courier New", monospace;
    font-style: italic;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.95);
    padding: 4px;
}}
"""


# ============================================================================
# PORTRAIT COLUMN STYLING (Left sidebar with AI avatars)
# ============================================================================

PORTRAIT_COLUMN_STYLE = f"""
QWidget#portrait_column {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {COMIC_COLORS['portrait_teal']},
        stop:1 {COMIC_COLORS['portrait_teal_dark']}
    );
    border-right: 4px solid {COMIC_COLORS['comic_black']};
    min-width: 140px;
    max-width: 140px;
    padding: 20px 10px;
}}

/* Portrait frame (circular) */
QLabel#portrait {{
    border: 4px solid {COMIC_COLORS['portrait_border']};
    border-radius: 50px;  /* Half of width/height for circle */
    background: {COMIC_COLORS['panel_pink']};
    min-width: 100px;
    max-width: 100px;
    min-height: 100px;
    max-height: 100px;
}}

/* Portrait label below avatar */
QLabel#portrait_label {{
    background: {COMIC_COLORS['portrait_border']};
    color: white;
    font-weight: bold;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 8px;
    border: 2px solid {COMIC_COLORS['comic_black']};
    border-radius: 3px;
    qproperty-alignment: AlignCenter;
}}
"""


# ============================================================================
# MESSAGE WIDGET STYLING (Speech bubbles)
# ============================================================================

MESSAGE_BUBBLE_STYLE = f"""
/* Container for message */
QWidget#message_container {{
    background: transparent;
    padding: 10px;
}}

/* Speech bubble frame */
QFrame#speech_bubble {{
    background: {COMIC_COLORS['speech_bubble_white']};
    border: 3px solid {COMIC_COLORS['comic_black']};
    border-radius: 20px;
    padding: 15px 20px;
}}

/* AI message bubble (cream colored) */
QFrame#speech_bubble[ai="true"] {{
    background: {COMIC_COLORS['panel_cream']};
}}

/* Nameplate above bubble */
QLabel#nameplate {{
    background: {COMIC_COLORS['portrait_teal']};
    color: white;
    font-weight: bold;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 12px;
    border: 2px solid {COMIC_COLORS['comic_black']};
    border-radius: 4px;
}}

/* Message text inside bubble */
QLabel#message_text {{
    font-family: "Comic Neue", "Comic Sans MS", cursive;
    font-size: 13px;
    color: {COMIC_COLORS['text_dark']};
    line-height: 1.5;
    background: transparent;
    border: none;
}}
"""


# ============================================================================
# BUTTON STYLING (Comic book action buttons)
# ============================================================================

COMIC_BUTTON_STYLE = f"""
QPushButton {{
    font-family: "Bangers", "Impact", sans-serif;
    font-size: 16px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12px 20px;
    border: 3px solid {COMIC_COLORS['comic_black']};
    border-radius: 6px;
}}

/* Primary button (red) */
QPushButton#primary {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {COMIC_COLORS['banner_red']},
        stop:1 {COMIC_COLORS['banner_red_dark']}
    );
    color: {COMIC_COLORS['banner_yellow']};
}}

QPushButton#primary:hover {{
    background: {COMIC_COLORS['banner_red']};
    border: 4px solid {COMIC_COLORS['comic_black']};
}}

QPushButton#primary:pressed {{
    background: {COMIC_COLORS['banner_red_dark']};
    padding: 13px 19px 11px 21px;
}}

/* Secondary button (teal) */
QPushButton#secondary {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {COMIC_COLORS['portrait_teal']},
        stop:1 {COMIC_COLORS['portrait_teal_dark']}
    );
    color: white;
}}

QPushButton#secondary:hover {{
    background: {COMIC_COLORS['portrait_teal']};
    border: 4px solid {COMIC_COLORS['comic_black']};
}}
"""


# ============================================================================
# INPUT FIELD STYLING
# ============================================================================

INPUT_STYLE = f"""
QLineEdit, QTextEdit, QPlainTextEdit {{
    background: white;
    border: 3px solid {COMIC_COLORS['comic_black']};
    border-radius: 12px;
    padding: 12px 16px;
    font-family: "Comic Neue", "Comic Sans MS", cursive;
    font-size: 13px;
    color: {COMIC_COLORS['text_dark']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 3px solid {COMIC_COLORS['portrait_teal']};
    background: {COMIC_COLORS['panel_cream']};
}}

QComboBox {{
    background: white;
    border: 3px solid {COMIC_COLORS['comic_black']};
    border-radius: 6px;
    padding: 8px 12px;
    font-family: "Comic Neue", "Comic Sans MS", cursive;
    font-size: 12px;
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid {COMIC_COLORS['comic_black']};
    margin-right: 8px;
}}
"""


# ============================================================================
# RIGHT SIDEBAR STYLING
# ============================================================================

SIDEBAR_STYLE = f"""
QWidget#right_sidebar {{
    background: {COMIC_COLORS['portrait_border']};
    border-left: 4px solid {COMIC_COLORS['comic_black']};
    padding: 20px 15px;
}}

/* Tab buttons in sidebar */
QPushButton#sidebar_tab {{
    background: {COMIC_COLORS['portrait_teal']};
    border: 2px solid {COMIC_COLORS['comic_black']};
    border-radius: 4px;
    padding: 10px;
    text-align: center;
    font-weight: bold;
    font-size: 11px;
    text-transform: uppercase;
    color: white;
    margin-bottom: 10px;
}}

QPushButton#sidebar_tab:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {COMIC_COLORS['portrait_teal']},
        stop:1 {COMIC_COLORS['portrait_teal_dark']}
    );
}}

QPushButton#sidebar_tab:checked {{
    background: {COMIC_COLORS['banner_yellow']};
    color: {COMIC_COLORS['comic_black']};
    border: 3px solid {COMIC_COLORS['comic_black']};
}}
"""


# ============================================================================
# SCROLLBAR STYLING (Comic theme)
# ============================================================================

SCROLLBAR_STYLE = f"""
QScrollBar:vertical {{
    background: {COMIC_COLORS['panel_cream']};
    border: 2px solid {COMIC_COLORS['comic_black']};
    width: 16px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COMIC_COLORS['portrait_teal']};
    border: 2px solid {COMIC_COLORS['comic_black']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COMIC_COLORS['banner_red']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: {COMIC_COLORS['panel_cream']};
}}
"""


# ============================================================================
# USAGE EXAMPLE IN PyQt6
# ============================================================================

EXAMPLE_USAGE = """
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt6.QtGui import QFont, QFontDatabase

# Load custom fonts
QFontDatabase.addApplicationFont("fonts/Bangers-Regular.ttf")
QFontDatabase.addApplicationFont("fonts/ComicNeue-Regular.ttf")

# Apply styles to widgets
app = QApplication([])

# Main window
window = QMainWindow()
window.setStyleSheet(BANNER_STYLE + PORTRAIT_COLUMN_STYLE + MESSAGE_BUBBLE_STYLE +
                     COMIC_BUTTON_STYLE + INPUT_STYLE + SIDEBAR_STYLE + SCROLLBAR_STYLE)

# Set object names to match QSS selectors
banner = QWidget()
banner.setObjectName("banner")

title = QLabel("INFERENCE LOUNGE")
title.setObjectName("banner_title")

portrait = QLabel()
portrait.setObjectName("portrait")

# ... etc
"""

if __name__ == "__main__":
    print("Comic Book Theme - PyQt6 Style Examples")
    print("=" * 60)
    print("\nColor Palette:")
    for name, color in COMIC_COLORS.items():
        print(f"  {name:20s} = {color}")
    print("\nStyle sheets defined:")
    print("  - BANNER_STYLE")
    print("  - PORTRAIT_COLUMN_STYLE")
    print("  - MESSAGE_BUBBLE_STYLE")
    print("  - COMIC_BUTTON_STYLE")
    print("  - INPUT_STYLE")
    print("  - SIDEBAR_STYLE")
    print("  - SCROLLBAR_STYLE")
    print("\nSee EXAMPLE_USAGE for implementation pattern.")
