"""
Thinking Bubble Animation Widget

iPhone/Messenger-style "typing" indicator with three bouncing dots.
Shows in conversation area while AI is generating a response.
"""

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from styles import get_bubble_color, COMIC_COLORS
import math


class ThinkingBubbleWidget(QWidget):
    """
    A small speech bubble with three bouncing dots animation.
    Styled like iPhone/Messenger thinking indicator.
    """

    def __init__(self, speaker_name="AI", parent=None):
        super().__init__(parent)
        self.speaker_name = speaker_name

        # Get bubble color based on speaker
        self.bubble_color = get_bubble_color(speaker_name)

        # Animation state
        self.animation_phase = 0  # 0-11 for smooth wave animation
        self.dot_radius = 4
        self.dot_spacing = 12

        # Widget sizing
        bubble_width = 80
        bubble_height = 40
        self.setFixedSize(bubble_width, bubble_height)

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(150)  # Update every 150ms for smooth bounce

    def _animate(self):
        """Update animation phase and trigger repaint."""
        self.animation_phase = (self.animation_phase + 1) % 12
        self.update()

    def _get_dot_offset(self, dot_index):
        """
        Calculate vertical offset for a dot based on animation phase.
        Creates a wave effect where dots bounce up and down in sequence.

        Args:
            dot_index: 0, 1, or 2 (left, middle, right dot)

        Returns:
            int: Vertical offset in pixels
        """
        # Each dot is offset by 4 phases (12/3 = 4 phases per dot)
        phase = (self.animation_phase + (dot_index * 4)) % 12

        # Create smooth bounce using sine wave
        # Phase 0-6: going up, phase 6-12: coming down
        if phase < 6:
            offset = -int(6 * math.sin((phase / 6) * math.pi))
        else:
            offset = 0

        return offset

    def paintEvent(self, event):
        """Custom paint event to draw bubble and animated dots."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw rounded bubble background
        bubble_color = QColor(self.bubble_color)
        border_color = QColor(COMIC_COLORS['black'])

        # Bubble dimensions
        bubble_rect = QRect(4, 4, self.width() - 8, self.height() - 8)

        # Draw border (3px thick black)
        painter.setPen(QPen(border_color, 3))
        painter.setBrush(QBrush(bubble_color))
        painter.drawRoundedRect(bubble_rect, 20, 20)

        # Draw three bouncing dots
        center_y = self.height() // 2
        start_x = (self.width() - (2 * self.dot_spacing)) // 2

        dot_color = QColor(COMIC_COLORS['navy'])
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(dot_color))

        for i in range(3):
            x = start_x + (i * self.dot_spacing)
            y = center_y + self._get_dot_offset(i)

            painter.drawEllipse(
                x - self.dot_radius,
                y - self.dot_radius,
                self.dot_radius * 2,
                self.dot_radius * 2
            )

    def stop(self):
        """Stop the animation."""
        self.timer.stop()

    def start(self):
        """Start the animation."""
        self.timer.start()


class ThinkingBubbleWithLabel(QWidget):
    """
    Thinking bubble with optional nameplate above it.
    Combines the nameplate and thinking bubble into one widget.
    """

    def __init__(self, speaker_name="AI", show_nameplate=True, parent=None):
        super().__init__(parent)
        self.speaker_name = speaker_name

        # Manual layout (no layout manager for precise positioning)
        self.nameplate = None
        self.thinking_bubble = ThinkingBubbleWidget(speaker_name)

        if show_nameplate:
            # Create nameplate
            self.nameplate = QLabel(f"★ {speaker_name.upper()} ★")
            self.nameplate.setParent(self)
            self.nameplate.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.nameplate.setStyleSheet(f"""
                QLabel {{
                    background-color: {COMIC_COLORS['teal']};
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    padding: 4px 12px;
                    border: 2px solid {COMIC_COLORS['black']};
                    border-radius: 4px;
                }}
            """)
            self.nameplate.adjustSize()

        # Position widgets
        self._layout_widgets()

    def _layout_widgets(self):
        """Position nameplate and thinking bubble."""
        bubble_y = 0

        if self.nameplate:
            # Position nameplate at top
            self.nameplate.move(0, 0)
            bubble_y = self.nameplate.height() + 8

        # Position thinking bubble below nameplate
        self.thinking_bubble.setParent(self)
        self.thinking_bubble.move(0, bubble_y)

        # Set widget size
        width = max(
            self.nameplate.width() if self.nameplate else 0,
            self.thinking_bubble.width()
        )
        height = bubble_y + self.thinking_bubble.height()
        self.setFixedSize(width, height)

    def stop(self):
        """Stop the animation."""
        self.thinking_bubble.stop()

    def start(self):
        """Start the animation."""
        self.thinking_bubble.start()


# Demo/test code
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton

    app = QApplication(sys.argv)

    # Create demo window
    demo = QWidget()
    demo.setWindowTitle("Thinking Bubble Demo")
    demo.resize(400, 500)
    demo.setStyleSheet(f"""
        QWidget {{
            background-color: {COMIC_COLORS['cream']};
        }}
    """)

    layout = QVBoxLayout(demo)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)

    # Add thinking bubbles for different speakers
    speakers = ["Claude", "GPT-4", "Gemini", "Grok"]

    bubbles = []
    for speaker in speakers:
        bubble = ThinkingBubbleWithLabel(speaker, show_nameplate=True)
        layout.addWidget(bubble)
        bubbles.append(bubble)

    layout.addStretch()

    # Control buttons
    start_btn = QPushButton("Start All")
    start_btn.clicked.connect(lambda: [b.start() for b in bubbles])
    layout.addWidget(start_btn)

    stop_btn = QPushButton("Stop All")
    stop_btn.clicked.connect(lambda: [b.stop() for b in bubbles])
    layout.addWidget(stop_btn)

    demo.show()
    sys.exit(app.exec())
