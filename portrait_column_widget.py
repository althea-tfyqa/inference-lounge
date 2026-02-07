"""
Portrait Column Widget for Comic Book Theme

Displays circular character portraits in a vertical column with:
- Per-speaker color coding (matches message border colors)
- Active speaker highlighting (border + glow in speaker color)
- Character name labels with matching color
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen
from styles import get_portrait_path, COMIC_COLORS


class CircularPortraitWidget(QWidget):
    """
    A circular portrait widget with per-speaker color and active highlighting.
    """

    def __init__(self, model_name, character_name, speaker_color=None, size=100, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.character_name = character_name
        self.portrait_size = size
        self.is_active = False
        # Speaker color for border/glow — falls back to teal
        self.speaker_color = speaker_color or COMIC_COLORS['teal']

        # Load portrait image
        portrait_path = get_portrait_path(model_name)
        self.portrait_pixmap = QPixmap(portrait_path)

        # Widget sizing — extra space for glow effect
        border_padding = 16
        self.setFixedSize(size + border_padding, size + border_padding)

    def set_active(self, active):
        """Set whether this portrait is the active speaker."""
        self.is_active = active
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """Custom paint event to draw circular portrait with optional glow."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = self.portrait_size // 2

        # Draw glow for active speaker — uses speaker color
        if self.is_active:
            glow_color = QColor(self.speaker_color)
            for i in range(4, 0, -1):
                glow_color.setAlpha(40 * i)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow_color)
                glow_radius = radius + (i * 3)
                painter.drawEllipse(
                    center_x - glow_radius,
                    center_y - glow_radius,
                    glow_radius * 2,
                    glow_radius * 2
                )

        # Circular clipping path for portrait image
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
            # Fallback — solid circle in speaker color
            painter.setBrush(QColor(self.speaker_color))
            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )

        # Remove clipping for border
        painter.setClipPath(QPainterPath())

        # Border — always in speaker color, thicker when active
        border_width = 6 if self.is_active else 3
        border_color = QColor(self.speaker_color)
        if not self.is_active:
            border_color.setAlpha(140)  # Slightly faded when inactive

        border_pen = QPen(border_color, border_width)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        )


class PortraitCard(QWidget):
    """
    A portrait card: circular portrait + name label, colored per speaker.
    """

    def __init__(self, model_name, character_name, speaker_color=None, portrait_size=100, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.character_name = character_name
        self.speaker_color = speaker_color or COMIC_COLORS['teal']

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Portrait — with speaker color
        self.portrait = CircularPortraitWidget(
            model_name, character_name, speaker_color, portrait_size
        )
        layout.addWidget(self.portrait, alignment=Qt.AlignmentFlag.AlignCenter)

        # Name label — background matches speaker color
        self.name_label = QLabel(character_name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_label_style(active=False)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def _update_label_style(self, active=False):
        """Update name label styling based on active state."""
        bg = self.speaker_color
        border_width = 3 if active else 2
        font_size = 12 if active else 11
        self.name_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: white;
                font-weight: bold;
                font-size: {font_size}px;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 4px 8px;
                border-radius: 3px;
                border: {border_width}px solid {COMIC_COLORS['black']};
            }}
        """)

    def set_active(self, active):
        """Set whether this portrait is the active speaker."""
        self.portrait.set_active(active)
        self._update_label_style(active)


class PortraitColumnWidget(QWidget):
    """
    Vertical column displaying all participant portraits with active speaker highlighting.
    """

    def __init__(self, participants=None, parent=None):
        """
        Args:
            participants: List of tuples (model_name, character_name, speaker_color)
        """
        super().__init__(parent)
        self.portrait_cards = {}  # Map character_name -> PortraitCard

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Background styling
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COMIC_COLORS['cream']},
                    stop:1 #EDE4D4
                );
                border-right: 4px solid {COMIC_COLORS['black']};
            }}
        """)

        self.setFixedWidth(140)

        if participants:
            for args in participants:
                self.add_participant(*args)

    def add_participant(self, model_name, character_name, speaker_color=None):
        """Add a participant portrait to the column."""
        if character_name not in self.portrait_cards:
            card = PortraitCard(
                model_name, character_name,
                speaker_color=speaker_color,
                portrait_size=90
            )
            self.portrait_cards[character_name] = card
            self.layout().addWidget(card)

    def set_active_speaker(self, character_name):
        """Highlight the active speaker, dim others."""
        for name, card in self.portrait_cards.items():
            card.set_active(name == character_name)

    def clear_active_speaker(self):
        """Remove highlighting from all portraits."""
        for card in self.portrait_cards.values():
            card.set_active(False)
