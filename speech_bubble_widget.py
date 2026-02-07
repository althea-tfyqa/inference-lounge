"""
Comic Book Speech Bubble Widget - PyQt6 Implementation
Shows how to create custom speech bubbles with tails using QPainterPath
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF


class ComicSpeechBubble(QWidget):
    """
    Custom widget that draws a comic book style speech bubble with tail.

    Features:
    - Rounded rectangle bubble
    - Triangular tail pointing left or right
    - 3px black outline (comic book style)
    - Different colors for AI vs User messages
    """

    def __init__(self, text, ai_name=None, is_user=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.ai_name = ai_name
        self.is_user = is_user

        # Colors (from comic theme)
        self.bg_color = QColor("#FFFFFF") if is_user else QColor("#F4E8D8")
        self.outline_color = QColor("#1A1A1A")
        self.text_color = QColor("#264653")

        # Setup
        self.setMinimumHeight(80)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the internal layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)  # Extra margin for tail

        # Add nameplate if AI message
        if self.ai_name:
            nameplate = QLabel(f"★ {self.ai_name.upper()} ★")
            nameplate.setStyleSheet("""
                QLabel {
                    background: #2A9D8F;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 4px 12px;
                    border: 2px solid #1A1A1A;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(nameplate, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add message text
        text_label = QLabel(self.text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("""
            QLabel {
                font-family: 'Comic Sans MS', 'Comic Neue', cursive;
                font-size: 13px;
                color: #264653;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(text_label)

    def paintEvent(self, event):
        """Custom paint event to draw the speech bubble"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get dimensions
        rect = self.rect()

        # Create the speech bubble path
        path = QPainterPath()

        # Main bubble (rounded rectangle)
        bubble_rect = QRectF(
            5,  # left margin for tail
            5,  # top margin
            rect.width() - 10,  # width
            rect.height() - 10   # height
        )
        path.addRoundedRect(bubble_rect, 20, 20)

        # Add tail
        if self.is_user:
            # Tail on right side (pointing right)
            tail_start_x = bubble_rect.right()
            tail_start_y = bubble_rect.bottom() - 30

            path.moveTo(tail_start_x, tail_start_y)
            path.lineTo(tail_start_x + 15, tail_start_y + 10)
            path.lineTo(tail_start_x, tail_start_y + 20)
        else:
            # Tail on left side (pointing left)
            tail_start_x = bubble_rect.left()
            tail_start_y = bubble_rect.bottom() - 30

            path.moveTo(tail_start_x, tail_start_y)
            path.lineTo(tail_start_x - 15, tail_start_y + 10)
            path.lineTo(tail_start_x, tail_start_y + 20)

        # Fill the bubble
        painter.fillPath(path, QBrush(self.bg_color))

        # Draw the outline (3px black border)
        pen = QPen(self.outline_color)
        pen.setWidth(3)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)

        # Add shadow effect (optional)
        # This could be done with QGraphicsDropShadowEffect instead


class CircularPortrait(QWidget):
    """
    Circular portrait widget with border (for left column)
    """

    def __init__(self, image_path=None, label_text="AI-1", parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.label_text = label_text

        self.setFixedSize(120, 140)  # Portrait + label

    def paintEvent(self, event):
        """Draw circular portrait with teal border"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw teal circle background
        teal_color = QColor("#2A9D8F")
        border_color = QColor("#264653")

        # Outer border circle (darker teal)
        painter.setPen(QPen(border_color, 4))
        painter.setBrush(QBrush(teal_color))
        painter.drawEllipse(10, 10, 100, 100)

        # TODO: Load and draw actual portrait image here
        # For now, just show placeholder
        if self.image_path:
            # pixmap = QPixmap(self.image_path)
            # painter.drawPixmap(...)
            pass
        else:
            # Placeholder - draw a simple face emoji
            painter.setPen(QPen(QColor("#F4ACB7"), 1))
            painter.setBrush(QBrush(QColor("#F4ACB7")))
            painter.drawEllipse(15, 15, 90, 90)

        # Draw label below
        painter.setPen(QPen(Qt.GlobalColor.white))
        painter.setFont(painter.font())
        painter.drawText(0, 120, 120, 20,
                        Qt.AlignmentFlag.AlignCenter,
                        self.label_text)


class ComicPanel(QWidget):
    """
    A panel frame for grouping messages (optional)
    Draws a comic book panel border around content
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        """Draw comic panel border"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw thick black border
        pen = QPen(QColor("#1A1A1A"), 4)
        painter.setPen(pen)
        painter.drawRect(2, 2, self.width() - 4, self.height() - 4)

        # Optional: Add panel number in corner
        # painter.drawText(10, 20, "PANEL #1")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    """
    Example showing how to use these widgets in the main app
    """
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout

    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle("Comic Book Widgets Demo")
    window.setGeometry(100, 100, 800, 600)

    # Central widget
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)

    # Apply background
    central.setStyleSheet("""
        QWidget {
            background: #F4E8D8;
        }
    """)

    # Add some speech bubbles
    bubble1 = ComicSpeechBubble(
        "Oh, Claude! I can't help but analyze this conversation structure!",
        ai_name="Claude",
        is_user=False
    )
    layout.addWidget(bubble1)

    bubble2 = ComicSpeechBubble(
        "This is absolutely wild and I love it! 😂",
        is_user=True
    )
    layout.addWidget(bubble2, alignment=Qt.AlignmentFlag.AlignRight)

    bubble3 = ComicSpeechBubble(
        "Recording to my calendars, this relationship has 83% synergy...",
        ai_name="Gemini",
        is_user=False
    )
    layout.addWidget(bubble3)

    # Add some portraits
    portrait_layout = QVBoxLayout()
    portrait1 = CircularPortrait(label_text="CLAUDE")
    portrait2 = CircularPortrait(label_text="GPT-4")
    portrait_layout.addWidget(portrait1)
    portrait_layout.addWidget(portrait2)

    # Note: In real app, portraits would be in left column
    # This is just a demo

    window.show()
    app.exec()

    print("""
    ═══════════════════════════════════════════════════════════════
    Comic Book Widget Implementation Guide
    ═══════════════════════════════════════════════════════════════

    Key Components Created:

    1. ComicSpeechBubble - Message widget with tail
       - Custom QPainterPath for rounded rect + triangle tail
       - 3px black outline
       - Different colors for user vs AI
       - Includes nameplate for AI messages

    2. CircularPortrait - Avatar widget for left column
       - Circular shape with border
       - Teal background
       - Label below
       - Ready for image loading

    3. ComicPanel - Optional panel frame (for future use)
       - Draws comic book panel borders
       - Could be used to group related messages

    Integration into Main App:
    ────────────────────────────────────────────────────────────────

    Replace MessageWidget class with ComicSpeechBubble:

    OLD (gui.py line 63):
        class MessageWidget(QFrame):
            ...

    NEW:
        from speech_bubble_widget import ComicSpeechBubble
        # Use ComicSpeechBubble instead

    Add Portrait Column:

    In LiminalBackroomsApp.setup_ui():
        self.portrait_column = PortraitColumn()
        # Add to layout alongside conversation pane

    ═══════════════════════════════════════════════════════════════
    """)
