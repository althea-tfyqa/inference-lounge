# styles.py
"""
Centralized styling for the Liminal Backrooms application.

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