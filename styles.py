# styles.py
"""
Centralized styling for the Inference Lounge application.

This module is the SINGLE SOURCE OF TRUTH for all colors, fonts, and widget styles.
Import from here - never hardcode colors or duplicate style definitions.

Usage:
    from styles import COLORS, FONTS, get_combobox_style, get_button_style
"""

# =============================================================================
# COLOR PALETTE - Neutral Light Theme
# =============================================================================

COLORS = {
    # Backgrounds - clean light palette
    'bg_dark': '#FFFFFF',           # White (dialog backgrounds)
    'bg_medium': '#F3F4F6',         # Gray-100 (secondary bg)
    'bg_light': '#E5E7EB',          # Gray-200 (tertiary bg)

    # Primary accents - blue
    'accent_cyan': '#3B82F6',       # Blue-500 (primary)
    'accent_cyan_hover': '#2563EB', # Blue-600
    'accent_cyan_active': '#1D4ED8', # Blue-700

    # Secondary accents
    'accent_pink': '#EC4899',       # Pink-500 (secondary)
    'accent_purple': '#8B5CF6',     # Violet-500 (tertiary)
    'accent_yellow': '#F59E0B',     # Amber-500 for warnings
    'accent_green': '#10B981',      # Emerald-500

    # AI-specific colors (for chat message headers)
    'ai_1': '#2563EB',              # Blue-600 - AI-1
    'ai_2': '#0D9488',              # Teal-600 - AI-2
    'ai_3': '#7C3AED',              # Violet-600 - AI-3
    'ai_4': '#DB2777',              # Pink-600 - AI-4
    'ai_5': '#EA580C',              # Orange-600 - AI-5
    'human': '#4F46E5',             # Indigo-600 - Human User

    # Notification colors
    'notify_error': '#DC2626',      # Red-600 - Error/Failure notifications
    'notify_success': '#16A34A',    # Green-600 - Success notifications
    'notify_info': '#D97706',       # Amber-600 - Informational notifications

    # Text colors
    'text_normal': '#374151',       # Gray-700 (body text)
    'text_dim': '#9CA3AF',          # Gray-400 (subtle text)
    'text_bright': '#111827',       # Gray-900 (bold text)
    'text_glow': '#1D4ED8',         # Blue-700 (section headers)
    'text_timestamp': '#6B7280',    # Gray-500 (timestamps)
    'text_error': '#DC2626',        # Red-600 (error text)

    # Borders and effects
    'border': '#D1D5DB',            # Gray-300
    'border_glow': '#93C5FD',       # Blue-300 (accent borders)
    'border_highlight': '#E5E7EB',  # Gray-200 (highlights)
    'shadow': 'rgba(59, 130, 246, 0.1)',  # Blue shadow

    # Legacy color mappings for compatibility
    'accent_blue': '#3B82F6',       # Blue-500
    'accent_blue_hover': '#2563EB', # Blue-600
    'accent_blue_active': '#1D4ED8', # Blue-700
    'accent_orange': '#F59E0B',     # Amber-500
    'chain_of_thought': '#10B981',  # Emerald-500
    'user_header': '#3B82F6',       # Blue-500
    'ai_header': '#8B5CF6',         # Violet-500
    'system_message': '#F59E0B',    # Amber-500
}


# =============================================================================
# FONT CONFIGURATION
# =============================================================================

FONTS = {
    # Primary fonts - system defaults
    'family_mono': "'SF Mono', 'Consolas', 'Monaco', monospace",
    'family_display': "'SF Pro Display', 'Segoe UI', system-ui, sans-serif",
    'family_ui': "'SF Pro Text', 'Segoe UI', system-ui, sans-serif",

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

# Theme colors — neutral light palette (keys preserved for future re-theming)
COMIC_COLORS = {
    'banner_red': '#374151',        # Gray-700 (app header bg)
    'banner_red_dark': '#1F2937',   # Gray-800 (header gradient)
    'banner_yellow': '#FFFFFF',     # White (header title text)
    'teal': '#3B82F6',             # Blue-500 (primary accent)
    'teal_dark': '#2563EB',        # Blue-600 (accent dark)
    'navy': '#1F2937',             # Gray-800 (dark containers)
    'cream': '#F9FAFB',            # Gray-50 (main backgrounds)
    'gold': '#F3F4F6',             # Gray-100 (input area bg)
    'black': '#111827',            # Gray-900 (borders/outlines)
    'pink': '#DBEAFE',             # Blue-100 (subtle accents)
}

# Theme fonts — system defaults (keys preserved for future re-theming)
COMIC_FONTS = {
    'family_title': "'SF Pro Display', 'Segoe UI', system-ui, sans-serif",  # Display font for titles
    'family_body': "'SF Pro Text', 'Segoe UI', system-ui, sans-serif",     # Body text font
    'family_mono': "'SF Mono', 'Consolas', 'Monaco', monospace",           # Monospace for technical text
}


# =============================================================================
# THEME HELPER FUNCTIONS
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
    """Get the style for comboboxes."""
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
            background-color: {COLORS['accent_cyan']};
            color: #FFFFFF;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: {COLORS['bg_light']};
            color: {COLORS['text_bright']};
        }}
    """


def get_button_style(accent_color=None):
    """
    Get button style.

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
    """Get style for text inputs."""
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
    """Get style for checkboxes."""
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
    Get style for scrollbars.

    Features:
    - Clean, minimal design
    - Blue accent on hover
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
# THEMED WIDGET STYLE GENERATORS
# =============================================================================

# Color mapping for GroupedModelComboBox (expects cyberpunk-style keys).
# Maps those keys to neutral theme equivalents so the delegate renders in-theme.
COMIC_COLORS_FULL = {
    'bg_dark': COMIC_COLORS['cream'],           # Dropdown list background
    'bg_medium': '#FFFFFF',                      # Combo box background (white)
    'bg_light': '#E5E7EB',                       # Hover highlight (gray-200)
    'text_bright': COMIC_COLORS['black'],        # Bold text
    'text_normal': '#374151',                    # Normal text (gray-700)
    'accent_cyan': COMIC_COLORS['teal'],         # Accent color (blue)
}


def get_comic_combobox_style():
    """Get neutral-themed combobox style — white background, subtle borders, blue accents."""
    return f"""
        QComboBox {{
            background-color: #FFFFFF;
            color: {COMIC_COLORS['black']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 5px 10px;
            min-height: 24px;
            font-size: 12px;
            font-family: {COMIC_FONTS['family_body']};
        }}
        QComboBox:hover {{
            border: 1px solid {COMIC_COLORS['teal']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 22px;
            border-left: 1px solid {COLORS['border']};
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
            border: 1px solid {COLORS['border']};
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
            background-color: #E5E7EB;
            color: {COMIC_COLORS['black']};
        }}
    """


def get_comic_button_style(variant='primary'):
    """
    Get themed button style.

    Args:
        variant: 'primary' (gray/white), 'secondary' (blue/white), or 'subtle' (transparent/blue)
    """
    if variant == 'primary':
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['banner_red']},
                    stop:1 {COMIC_COLORS['banner_red_dark']});
                color: {COMIC_COLORS['banner_yellow']};
                border: 1px solid {COMIC_COLORS['black']};
                border-radius: 6px;
                padding: 8px 14px;
                font-family: {COMIC_FONTS['family_title']};
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4B5563,
                    stop:1 {COMIC_COLORS['banner_red']});
            }}
            QPushButton:pressed {{
                background: {COMIC_COLORS['banner_red_dark']};
            }}
            QPushButton:disabled {{
                background: #E5E7EB;
                color: #9CA3AF;
                border-color: #D1D5DB;
            }}
        """
    elif variant == 'secondary':
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['teal']},
                    stop:1 {COMIC_COLORS['teal_dark']});
                color: white;
                border: 1px solid {COMIC_COLORS['black']};
                border-radius: 6px;
                padding: 10px 16px;
                font-family: {COMIC_FONTS['family_title']};
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60A5FA,
                    stop:1 {COMIC_COLORS['teal']});
            }}
            QPushButton:pressed {{
                background: {COMIC_COLORS['teal_dark']};
            }}
            QPushButton:disabled {{
                background: #E5E7EB;
                color: #9CA3AF;
                border-color: #D1D5DB;
            }}
        """
    else:  # subtle
        return f"""
            QPushButton {{
                background: transparent;
                color: {COMIC_COLORS['teal']};
                border: 1px solid {COMIC_COLORS['teal']};
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
                color: #9CA3AF;
                border-color: #D1D5DB;
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