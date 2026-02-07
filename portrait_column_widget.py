"""
Portrait Column Widget for Comic Book Theme

Displays circular character portraits in a vertical column with:
- Active speaker highlighting (border + glow)
- Character name labels
- Smooth visual feedback
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen
from styles import get_portrait_path, COMIC_COLORS


class CircularPortraitWidget(QWidget):
    """
    A circular portrait widget with optional highlighting for active speaker.
    """

    def __init__(self, model_name, character_name, size=100, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.character_name = character_name
        self.portrait_size = size
        self.is_active = False

        # Load portrait image
        portrait_path = get_portrait_path(model_name)
        self.portrait_pixmap = QPixmap(portrait_path)

        # Widget sizing
        border_padding = 16  # Extra space for glow effect
        self.setFixedSize(size + border_padding, size + border_padding)

    def set_active(self, active):
        """Set whether this portrait is the active speaker."""
        self.is_active = active
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """Custom paint event to draw circular portrait with optional glow."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate center position (accounting for border padding)
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = self.portrait_size // 2

        # Draw glow/shadow for active speaker
        if self.is_active:
            # Draw multiple circles for glow effect
            glow_color = QColor(COMIC_COLORS['teal'])
            for i in range(3, 0, -1):
                glow_color.setAlpha(30 * i)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow_color)
                glow_radius = radius + (i * 2)
                painter.drawEllipse(
                    center_x - glow_radius,
                    center_y - glow_radius,
                    glow_radius * 2,
                    glow_radius * 2
                )

        # Create circular clipping path for portrait
        path = QPainterPath()
        path.addEllipse(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        )
        painter.setClipPath(path)

        # Draw portrait image (scaled and centered)
        if not self.portrait_pixmap.isNull():
            scaled_pixmap = self.portrait_pixmap.scaled(
                self.portrait_size,
                self.portrait_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(
                center_x - radius,
                center_y - radius,
                scaled_pixmap
            )
        else:
            # Fallback if image doesn't load
            painter.setBrush(QColor(COMIC_COLORS['pink']))
            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )

        # Remove clipping for border
        painter.setClipPath(QPainterPath())

        # Draw border
        border_width = 6 if self.is_active else 4
        border_color = QColor(COMIC_COLORS['teal'] if self.is_active else COMIC_COLORS['navy'])

        # Create pen with width and color
        border_pen = QPen(border_color, border_width)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        )

        # Apply opacity for inactive speakers
        if not self.is_active:
            self.setWindowOpacity(0.7)
        else:
            self.setWindowOpacity(1.0)


class PortraitCard(QWidget):
    """
    A portrait card consisting of a circular portrait and name label.
    """

    def __init__(self, model_name, character_name, portrait_size=100, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.character_name = character_name

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Portrait
        self.portrait = CircularPortraitWidget(model_name, character_name, portrait_size)
        layout.addWidget(self.portrait, alignment=Qt.AlignmentFlag.AlignCenter)

        # Name label
        self.name_label = QLabel(character_name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COMIC_COLORS['navy']};
                color: white;
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 4px 8px;
                border-radius: 3px;
                border: 2px solid {COMIC_COLORS['black']};
            }}
        """)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_active(self, active):
        """Set whether this portrait is the active speaker."""
        self.portrait.set_active(active)


class PortraitColumnWidget(QWidget):
    """
    Vertical column displaying all participant portraits with active speaker highlighting.
    """

    def __init__(self, participants=None, parent=None):
        """
        Args:
            participants: List of tuples (model_name, character_name)
                         e.g., [("claude", "Claude"), ("gpt", "GPT-4")]
        """
        super().__init__(parent)
        self.portrait_cards = {}  # Map character_name -> PortraitCard (unique even if same model)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Styling
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['teal']},
                    stop:1 {COMIC_COLORS['teal_dark']}
                );
                border-right: 4px solid {COMIC_COLORS['black']};
            }}
        """)

        # Set fixed width (narrower to maximize conversation space)
        self.setFixedWidth(120)

        # Add participants
        if participants:
            for model_name, character_name in participants:
                self.add_participant(model_name, character_name)

    def add_participant(self, model_name, character_name):
        """Add a participant portrait to the column."""
        if character_name not in self.portrait_cards:
            card = PortraitCard(model_name, character_name, portrait_size=90)  # Smaller to fit narrower column
            self.portrait_cards[character_name] = card  # Use character_name as key (unique)
            self.layout().addWidget(card)

    def set_active_speaker(self, character_name):
        """Highlight the active speaker, dim others."""
        for name, card in self.portrait_cards.items():
            card.set_active(name == character_name)

    def clear_active_speaker(self):
        """Remove highlighting from all portraits."""
        for card in self.portrait_cards.values():
            card.set_active(False)


# Demo/test code
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton

    app = QApplication(sys.argv)

    # Create demo window
    demo = QWidget()
    demo.setWindowTitle("Portrait Column Demo")
    demo.resize(400, 600)

    layout = QHBoxLayout(demo)

    # Portrait column
    participants = [
        ("claude", "Claude"),
        ("gpt", "GPT-4"),
        ("gemini", "Gemini"),
        ("grok", "Grok"),
    ]
    portrait_column = PortraitColumnWidget(participants)
    layout.addWidget(portrait_column)

    # Control buttons
    button_layout = QVBoxLayout()
    for model_name, char_name in participants:
        btn = QPushButton(f"Activate {char_name}")
        btn.clicked.connect(lambda checked, m=model_name: portrait_column.set_active_speaker(m))
        button_layout.addWidget(btn)

    clear_btn = QPushButton("Clear Active")
    clear_btn.clicked.connect(portrait_column.clear_active_speaker)
    button_layout.addWidget(clear_btn)

    layout.addLayout(button_layout)

    demo.show()
    sys.exit(app.exec())
