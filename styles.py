# styles.py
"""
Centralized styling for the Inference Lounge application.

This module is the SINGLE SOURCE OF TRUTH for all colors, fonts, and widget styles.
Import from here - never hardcode colors or duplicate style definitions.

Usage:
    from styles import COLORS, FONTS, get_combobox_style, get_button_style
"""

# =============================================================================
# COLOR PALETTE - Cyberpunk Theme
# =============================================================================

COLORS = {
    # Backgrounds - darker, moodier
    'bg_dark': '#0A0E1A',           # Deep blue-black
    'bg_medium': '#111827',         # Slate dark
    'bg_light': '#1E293B',          # Lighter slate
    
    # Primary accents - neon but muted
    'accent_cyan': '#06B6D4',       # Cyan (primary)
    'accent_cyan_hover': '#0891B2',
    'accent_cyan_active': '#0E7490',
    
    # Secondary accents
    'accent_pink': '#EC4899',       # Hot pink (secondary)
    'accent_purple': '#A855F7',     # Purple (tertiary)
    'accent_yellow': '#FBBF24',     # Amber for warnings
    'accent_green': '#10B981',      # Emerald (rabbithole)
    
    # AI-specific colors (for chat message headers)
    'ai_1': '#6FFFE6',              # Bright Aqua - AI-1
    'ai_2': '#06E2D4',              # Teal - AI-2
    'ai_3': '#54F5E9',              # Turquoise - AI-3
    'ai_4': '#8BFCEF',              # Light Cyan - AI-4
    'ai_5': '#91FCFD',              # Pale Cyan - AI-5
    'human': '#ff00b3',             # Hot Pink/Magenta - Human User
    
    # Notification colors
    'notify_error': '#ff4444',      # Bright Red - Error/Failure notifications (distinct from human pink)
    'notify_success': '#5DFF44',    # Bright Green - Success notifications
    'notify_info': '#FFFF48',       # Yellow - Informational notifications
    
    # Text colors
    'text_normal': '#CBD5E1',       # Slate-200
    'text_dim': '#64748B',          # Slate-500
    'text_bright': '#F1F5F9',       # Slate-50
    'text_glow': '#38BDF8',         # Sky-400 (glowing text)
    'text_timestamp': '#7a8899',    # Subtle timestamp color - readable but not distracting
    'text_error': '#ff4444',        # Red - Error text (matches notify_error)
    
    # Borders and effects
    'border': '#1E293B',            # Slate-800
    'border_glow': '#06B6D4',       # Glowing cyan borders
    'border_highlight': '#334155',  # Slate-700
    'shadow': 'rgba(6, 182, 212, 0.2)',  # Cyan glow shadows
    
    # Legacy color mappings for compatibility
    'accent_blue': '#06B6D4',       # Map old blue to cyan
    'accent_blue_hover': '#0891B2',
    'accent_blue_active': '#0E7490',
    'accent_orange': '#F59E0B',     # Amber-500
    'chain_of_thought': '#10B981',  # Emerald
    'user_header': '#06B6D4',       # Cyan
    'ai_header': '#A855F7',         # Purple
    'system_message': '#F59E0B',    # Amber
}


# =============================================================================
# FONT CONFIGURATION
# =============================================================================

FONTS = {
    # Primary fonts
    'family_mono': "'Iosevka Term', 'Consolas', 'Monaco', monospace",
    'family_display': "'Orbitron', sans-serif",
    'family_ui': "'Segoe UI', sans-serif",

    # Font sizes
    'size_xs': '8px',
    'size_sm': '10px',
    'size_md': '12px',
    'size_lg': '14px',
    'size_xl': '16px',

    # Common combinations
    'default': '10px',              # Default UI font size
    'code': '10pt',                 # Code/monospace size
}


# =============================================================================
# COMIC BOOK THEME - Colors, Portraits, Fonts
# =============================================================================

# Comic book speech bubble colors (subtle backgrounds per speaker)
COMIC_BUBBLE_COLORS = {
    'claude': '#F4E8D8',      # Cream - warm, vintage
    'gpt': '#E8F4F8',         # Pale blue - cool, professional
    'gemini': '#FFF9E8',      # Pale yellow - bright, optimistic
    'grok': '#FFE8D8',        # Pale orange - energetic, chaotic
    'deepseek': '#F0E8F8',    # Pale lavender - mysterious
    'generic': '#F5F5F5',     # Light gray - neutral
    'human': '#FFFFFF',       # Pure white - clean, distinct
}

# Portrait mapping: AI provider/model → character portrait filename
# Maps model names to their character portrait files in assets/comic/portraits/
PORTRAIT_MAP = {
    # Map various provider/model names to portrait files
    'claude': 'claudette.png',
    'anthropic': 'claudette.png',
    'gpt': 'chad-gpt.png',
    'openai': 'chad-gpt.png',
    'chatgpt': 'chad-gpt.png',
    'gemini': 'gemini.png',
    'google': 'gemini.png',
    'grok': 'grok.png',
    'xai': 'grok.png',
    'deepseek': 'deep-seek.png',
    'human': 'human.png',
    'user': 'human.png',
    'generic': 'generic-ai.png',  # Fallback for unknown models
}

# Comic book theme colors (for future full theme implementation)
COMIC_COLORS = {
    'banner_red': '#E63946',        # Red banner background
    'banner_red_dark': '#C81F2A',   # Darker red gradient
    'banner_yellow': '#FFD60A',     # Yellow title text
    'teal': '#2A9D8F',             # Teal accents (portrait frames, nameplate)
    'teal_dark': '#1A7A6E',        # Darker teal gradient
    'navy': '#264653',             # Navy (portrait label background)
    'cream': '#F4E8D8',            # Cream paper background
    'gold': '#E9C46A',             # Gold (input area)
    'black': '#1A1A1A',            # Black borders and outlines
    'pink': '#F4ACB7',             # Pink accents
}

# Comic book fonts (for future implementation)
COMIC_FONTS = {
    'family_title': "'Bangers', cursive",                      # Bold display font for titles
    'family_body': "'Comic Neue', 'Comic Sans MS', cursive",   # Body text font
    'family_mono': "'Courier New', monospace",                 # Monospace for technical text
}


# =============================================================================
# COMIC THEME HELPER FUNCTIONS
# =============================================================================

def get_portrait_path(model_or_provider):
    """
    Get the portrait file path for a given AI model or provider.

    Args:
        model_or_provider: Model name, provider name, or AI identifier (case-insensitive)

    Returns:
        str: Absolute path to portrait image file

    Example:
        get_portrait_path("Claude Opus 4.5") -> "/full/path/to/assets/comic/portraits/claudette.png"
        get_portrait_path("gpt-4") -> "/full/path/to/assets/comic/portraits/chad-gpt.png"
    """
    import os

    # Get the project root (where main.py is located)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Normalize the input: lowercase, extract key words
    normalized = model_or_provider.lower()

    # Check for matches in portrait map
    for key, portrait_file in PORTRAIT_MAP.items():
        if key in normalized:
            return os.path.join(project_root, 'assets', 'comic', 'portraits', portrait_file)

    # Default to generic AI portrait
    return os.path.join(project_root, 'assets', 'comic', 'portraits', PORTRAIT_MAP['generic'])


def get_bubble_color(model_or_provider):
    """
    Get the speech bubble background color for a given AI model or provider.

    Args:
        model_or_provider: Model name, provider name, or AI identifier (case-insensitive)

    Returns:
        str: Hex color code for bubble background

    Example:
        get_bubble_color("Claude Opus 4.5") -> "#F4E8D8" (cream)
        get_bubble_color("gpt-4") -> "#E8F4F8" (pale blue)
    """
    # Normalize the input
    normalized = model_or_provider.lower()

    # Check for matches in bubble colors
    for key, color in COMIC_BUBBLE_COLORS.items():
        if key in normalized:
            return color

    # Default to generic gray
    return COMIC_BUBBLE_COLORS['generic']


# =============================================================================
# WIDGET STYLE GENERATORS
# =============================================================================

def get_combobox_style():
    """Get the style for comboboxes - cyberpunk themed."""
    return f"""
        QComboBox {{
            background-color: {COLORS['bg_medium']};
            color: {COLORS['text_normal']};
            border: 1px solid {COLORS['border_glow']};
            border-radius: 0px;
            padding: 4px 8px;
            min-height: 20px;
            font-size: {FONTS['size_sm']};
        }}
        QComboBox:hover {{
            border: 1px solid {COLORS['accent_cyan']};
            color: {COLORS['text_bright']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {COLORS['border_glow']};
            border-radius: 0px;
        }}
        QComboBox::down-arrow {{
            width: 12px;
            height: 12px;
            image: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_normal']};
            border: 1px solid {COLORS['border_glow']};
            border-radius: 0px;
            padding: 2px;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 22px;
            padding: 2px 4px;
            padding-left: 8px;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: #164E63;
            color: {COLORS['text_bright']};
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: {COLORS['bg_light']};
            color: {COLORS['text_bright']};
        }}
    """


def get_button_style(accent_color=None):
    """
    Get cyberpunk-themed button style.
    
    Args:
        accent_color: Override accent color (defaults to accent_cyan)
    """
    accent = accent_color or COLORS['accent_cyan']
    return f"""
        QPushButton {{
            background-color: {COLORS['bg_medium']};
            color: {accent};
            border: 1px solid {accent};
            border-radius: 0px;
            padding: 10px 14px;
            font-size: {FONTS['size_sm']};
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {accent};
            color: {COLORS['bg_dark']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['bg_light']};
        }}
        QPushButton:disabled {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_dim']};
            border-color: {COLORS['text_dim']};
        }}
    """


def get_input_style():
    """Get style for text inputs - cyberpunk themed."""
    return f"""
        QLineEdit, QTextEdit {{
            background-color: {COLORS['bg_medium']};
            color: {COLORS['text_normal']};
            border: 1px solid {COLORS['border_glow']};
            border-radius: 0px;
            padding: 8px;
            font-size: {FONTS['size_sm']};
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border: 1px solid {COLORS['accent_cyan']};
            color: {COLORS['text_bright']};
        }}
    """


def get_label_style(style_type='normal'):
    """
    Get style for labels.
    
    Args:
        style_type: One of 'normal', 'header', 'glow', 'dim'
    """
    styles = {
        'normal': f"""
            QLabel {{
                color: {COLORS['text_normal']};
                font-size: {FONTS['size_sm']};
            }}
        """,
        'header': f"""
            QLabel {{
                color: {COLORS['text_glow']};
                font-size: {FONTS['size_sm']};
                font-weight: bold;
                letter-spacing: 1px;
            }}
        """,
        'glow': f"""
            QLabel {{
                color: {COLORS['text_glow']};
                font-size: {FONTS['size_sm']};
            }}
        """,
        'dim': f"""
            QLabel {{
                color: {COLORS['text_dim']};
                font-size: {FONTS['size_xs']};
            }}
        """,
    }
    return styles.get(style_type, styles['normal'])


def get_checkbox_style():
    """Get style for checkboxes - cyberpunk themed."""
    return f"""
        QCheckBox {{
            color: {COLORS['text_dim']};
            font-size: 10px;
            spacing: 6px;
            padding: 4px 0px;
        }}
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
            border: 1px solid {COLORS['border_glow']};
            border-radius: 0px;
            background-color: {COLORS['bg_dark']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {COLORS['accent_cyan']};
            border-color: {COLORS['accent_cyan']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {COLORS['accent_cyan']};
        }}
    """


def get_scrollbar_style():
    """
    Get style for scrollbars - retro CRT/cyberpunk theme.
    
    Features:
    - No rounded corners (sharp edges for retro look)
    - Cyan glow on hover
    - Minimal design
    """
    return f"""
        QScrollBar:vertical {{
            background-color: {COLORS['bg_dark']};
            width: 12px;
            border: 1px solid {COLORS['border']};
            border-radius: 0px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {COLORS['border_glow']};
            border: none;
            border-radius: 0px;
            min-height: 30px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['accent_cyan']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
            border: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            background-color: {COLORS['bg_dark']};
            height: 12px;
            border: 1px solid {COLORS['border']};
            border-radius: 0px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {COLORS['border_glow']};
            border: none;
            border-radius: 0px;
            min-width: 30px;
            margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS['accent_cyan']};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
            border: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
    """


def get_frame_style(style_type='default'):
    """
    Get style for frames/containers.
    
    Args:
        style_type: One of 'default', 'bordered', 'glow'
    """
    styles = {
        'default': f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: none;
            }}
        """,
        'bordered': f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border']};
                border-radius: 0px;
            }}
        """,
        'glow': f"""
            QFrame {{
                background-color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['border_glow']};
                border-radius: 0px;
            }}
        """,
    }
    return styles.get(style_type, styles['default'])


def get_tooltip_style():
    """Get style for tooltips."""
    return f"""
        QToolTip {{
            background-color: {COLORS['bg_medium']};
            color: {COLORS['text_bright']};
            border: 1px solid {COLORS['accent_cyan']};
            padding: 6px;
            font-size: {FONTS['size_sm']};
        }}
    """


def get_menu_style():
    """Get style for context menus."""
    return f"""
        QMenu {{
            background-color: {COLORS['bg_medium']};
            color: {COLORS['text_normal']};
            border: 1px solid {COLORS['border_glow']};
            padding: 4px;
        }}
        QMenu::item {{
            padding: 6px 20px;
        }}
        QMenu::item:selected {{
            background-color: {COLORS['accent_cyan']};
            color: {COLORS['bg_dark']};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {COLORS['border']};
            margin: 4px 8px;
        }}
    """


# =============================================================================
# COMIC THEME - Widget Style Generators
# =============================================================================

# Color mapping for GroupedModelComboBox (expects cyberpunk-style keys).
# Maps those keys to comic theme equivalents so the delegate renders in-theme.
COMIC_COLORS_FULL = {
    'bg_dark': COMIC_COLORS['cream'],           # Dropdown list background
    'bg_medium': '#FFFFFF',                      # Combo box background (white)
    'bg_light': '#EDE4D4',                       # Hover highlight
    'text_bright': COMIC_COLORS['black'],        # Bold text
    'text_normal': '#333333',                    # Normal text
    'accent_cyan': COMIC_COLORS['teal'],         # Accent color (teal instead of cyan)
}


def get_comic_combobox_style():
    """Get comic-themed combobox style — cream/white background, black borders, teal accents."""
    return f"""
        QComboBox {{
            background-color: #FFFFFF;
            color: {COMIC_COLORS['black']};
            border: 3px solid {COMIC_COLORS['black']};
            border-radius: 4px;
            padding: 5px 10px;
            min-height: 24px;
            font-size: 12px;
            font-family: {COMIC_FONTS['family_body']};
        }}
        QComboBox:hover {{
            border: 3px solid {COMIC_COLORS['teal']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 22px;
            border-left: 3px solid {COMIC_COLORS['black']};
            border-radius: 0px;
        }}
        QComboBox::down-arrow {{
            width: 12px;
            height: 12px;
            image: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {COMIC_COLORS['cream']};
            color: {COMIC_COLORS['black']};
            border: 3px solid {COMIC_COLORS['black']};
            border-radius: 0px;
            padding: 2px;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 22px;
            padding: 2px 4px;
            padding-left: 8px;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: {COMIC_COLORS['teal']};
            color: white;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: #EDE4D4;
            color: {COMIC_COLORS['black']};
        }}
    """


def get_comic_button_style(variant='primary'):
    """
    Get comic-themed button style.

    Args:
        variant: 'primary' (red/yellow), 'secondary' (teal/white), or 'subtle' (transparent/teal)
    """
    if variant == 'primary':
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['banner_red']},
                    stop:1 {COMIC_COLORS['banner_red_dark']});
                color: {COMIC_COLORS['banner_yellow']};
                border: 3px solid {COMIC_COLORS['black']};
                border-radius: 6px;
                padding: 8px 14px;
                font-family: {COMIC_FONTS['family_title']};
                font-size: 14px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F04A57,
                    stop:1 {COMIC_COLORS['banner_red']});
            }}
            QPushButton:pressed {{
                background: {COMIC_COLORS['banner_red_dark']};
            }}
            QPushButton:disabled {{
                background: #CCCCCC;
                color: #888888;
                border-color: #999999;
            }}
        """
    elif variant == 'secondary':
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['teal']},
                    stop:1 {COMIC_COLORS['teal_dark']});
                color: white;
                border: 3px solid {COMIC_COLORS['black']};
                border-radius: 6px;
                padding: 10px 16px;
                font-family: {COMIC_FONTS['family_title']};
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #35B8A8,
                    stop:1 {COMIC_COLORS['teal']});
            }}
            QPushButton:pressed {{
                background: {COMIC_COLORS['teal_dark']};
            }}
            QPushButton:disabled {{
                background: #CCCCCC;
                color: #888888;
                border-color: #999999;
            }}
        """
    else:  # subtle
        return f"""
            QPushButton {{
                background: transparent;
                color: {COMIC_COLORS['teal']};
                border: 3px solid {COMIC_COLORS['teal']};
                border-radius: 6px;
                padding: 10px 16px;
                font-family: {COMIC_FONTS['family_body']};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {COMIC_COLORS['teal']};
                color: white;
            }}
            QPushButton:pressed {{
                background: {COMIC_COLORS['teal_dark']};
                color: white;
            }}
            QPushButton:disabled {{
                background: transparent;
                color: #AAAAAA;
                border-color: #CCCCCC;
            }}
        """


# =============================================================================
# COMPLETE APPLICATION STYLESHEET
# =============================================================================

def get_app_stylesheet():
    """
    Get a complete application stylesheet combining all widget styles.
    Apply this to QApplication for global styling.
    """
    return f"""
        {get_tooltip_style()}
        {get_menu_style()}
        {get_scrollbar_style()}
    """