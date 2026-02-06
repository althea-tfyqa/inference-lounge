"""
Scenario Editor Dialog - UI for editing conversation scenarios

Provides a PyQt6 dialog for CRUDR operations on scenario configurations.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit,
    QPlainTextEdit, QPushButton, QLabel, QMessageBox, QSplitter,
    QWidget, QInputDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from scenario_manager import ScenarioManager, ScenarioValidationError
from styles import COLORS, get_button_style, get_input_style, get_frame_style


class ScenarioEditorDialog(QDialog):
    """Dialog for editing conversation scenarios."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scenario Editor")
        self.setMinimumSize(1000, 700)

        # Track current state
        self.current_scenario_name = None
        self.scenarios = {}
        self.modified = False  # Track if user made changes

        self._setup_ui()
        self._load_scenarios()

    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Main splitter (scenario list | editor)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left side: Scenario list
        left_widget = self._create_scenario_list()
        splitter.addWidget(left_widget)

        # Right side: Editor
        right_widget = self._create_editor()
        splitter.addWidget(right_widget)

        # Set initial splitter sizes (30% list, 70% editor)
        splitter.setSizes([300, 700])

        layout.addWidget(splitter)

        # Bottom: Dialog buttons
        button_layout = self._create_dialog_buttons()
        layout.addLayout(button_layout)

        # Apply dark theme to dialog
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text_normal']};
            }}
        """)

    def _create_scenario_list(self) -> QWidget:
        """Create the scenario list widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Header
        header = QLabel("Scenarios")
        header.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {COLORS['accent_cyan']};
                padding: 4px;
            }}
        """)
        layout.addWidget(header)

        # List widget
        self.scenario_list = QListWidget()
        self.scenario_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_normal']};
                border: 1px solid {COLORS['accent_cyan']};
                border-radius: 0px;
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border: 1px solid transparent;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent_cyan']};
                color: {COLORS['bg_dark']};
                border: 1px solid {COLORS['accent_cyan']};
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_light']};
            }}
        """)
        self.scenario_list.currentItemChanged.connect(self._on_scenario_selected)
        layout.addWidget(self.scenario_list)

        # List action buttons
        list_btn_layout = QVBoxLayout()
        list_btn_layout.setSpacing(4)

        self.new_btn = QPushButton("New Scenario")
        self.new_btn.setStyleSheet(get_button_style(COLORS['accent_cyan']))
        self.new_btn.clicked.connect(self._on_new_scenario)
        list_btn_layout.addWidget(self.new_btn)

        self.rename_btn = QPushButton("Rename")
        self.rename_btn.setStyleSheet(get_button_style(COLORS['bg_light']))
        self.rename_btn.clicked.connect(self._on_rename_scenario)
        list_btn_layout.addWidget(self.rename_btn)

        layout.addLayout(list_btn_layout)

        return widget

    def _create_editor(self) -> QWidget:
        """Create the editor widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Scenario name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Scenario Name:")
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_bright']};
                font-weight: bold;
            }}
        """)
        name_layout.addWidget(name_label)

        self.name_field = QLineEdit()
        self.name_field.setStyleSheet(get_input_style())
        self.name_field.setPlaceholderText("Enter scenario name...")
        self.name_field.textChanged.connect(self._on_field_changed)
        name_layout.addWidget(self.name_field)

        layout.addLayout(name_layout)

        # AI prompt editors (5 slots)
        self.prompt_editors = {}
        self.token_counters = {}
        for i in range(1, 6):
            ai_slot = f"AI-{i}"

            # Label row with token counter
            label_row = QWidget()
            label_row_layout = QHBoxLayout(label_row)
            label_row_layout.setContentsMargins(0, 0, 0, 0)
            label_row_layout.setSpacing(0)

            label = QLabel(f"{ai_slot} Prompt:")
            label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_bright']};
                    font-weight: bold;
                    font-size: 12px;
                }}
            """)
            label_row_layout.addWidget(label)

            label_row_layout.addStretch()

            # Token counter
            token_counter = QLabel("~0 tokens")
            token_counter.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_dim']};
                    font-size: 10px;
                }}
            """)
            label_row_layout.addWidget(token_counter)
            self.token_counters[ai_slot] = token_counter

            layout.addWidget(label_row)

            # Editor
            editor = QPlainTextEdit()
            editor.setStyleSheet(f"""
                QPlainTextEdit {{
                    background-color: {COLORS['bg_medium']};
                    color: {COLORS['text_normal']};
                    border: 1px solid {COLORS['accent_cyan']};
                    border-radius: 0px;
                    padding: 6px;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 11px;
                    line-height: 1.4;
                }}
                QPlainTextEdit:focus {{
                    border: 1px solid {COLORS['accent_cyan_hover']};
                }}
            """)
            editor.setPlaceholderText(f"Enter system prompt for {ai_slot}...")
            editor.setMinimumHeight(80)
            editor.textChanged.connect(self._on_field_changed)
            editor.textChanged.connect(lambda ai=ai_slot: self._update_token_counter(ai))

            self.prompt_editors[ai_slot] = editor
            layout.addWidget(editor)

        return widget

    def _create_dialog_buttons(self) -> QHBoxLayout:
        """Create the bottom dialog buttons."""
        layout = QHBoxLayout()
        layout.setSpacing(8)

        # Delete button (left side)
        self.delete_btn = QPushButton("Delete Scenario")
        self.delete_btn.setStyleSheet(get_button_style(COLORS['notify_error']))
        self.delete_btn.clicked.connect(self._on_delete_scenario)
        layout.addWidget(self.delete_btn)

        layout.addStretch()

        # Save and Cancel (right side)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(get_button_style(COLORS['bg_light']))
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save All Changes")
        self.save_btn.setStyleSheet(get_button_style(COLORS['accent_green']))
        self.save_btn.clicked.connect(self._on_save)
        layout.addWidget(self.save_btn)

        return layout

    def _load_scenarios(self):
        """Load scenarios from config.py."""
        try:
            self.scenarios = ScenarioManager.load_scenarios()
            self._populate_scenario_list()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Load Error",
                f"Failed to load scenarios:\n{str(e)}"
            )

    def _populate_scenario_list(self):
        """Populate the scenario list widget."""
        self.scenario_list.clear()
        for name in sorted(self.scenarios.keys()):
            self.scenario_list.addItem(name)

        # Select first item if available
        if self.scenario_list.count() > 0:
            self.scenario_list.setCurrentRow(0)

    def _on_scenario_selected(self, current, previous):
        """Handle scenario selection in list."""
        if not current:
            self._clear_editor()
            return

        scenario_name = current.text()
        self._load_scenario_into_editor(scenario_name)

    def _load_scenario_into_editor(self, scenario_name: str):
        """Load a scenario's data into the editor fields."""
        if scenario_name not in self.scenarios:
            return

        self.current_scenario_name = scenario_name
        prompts = self.scenarios[scenario_name]

        # Block signals while loading to prevent marking as modified
        self.name_field.blockSignals(True)
        self.name_field.setText(scenario_name)
        self.name_field.blockSignals(False)

        for ai_slot, editor in self.prompt_editors.items():
            editor.blockSignals(True)
            editor.setPlainText(prompts.get(ai_slot, ""))
            editor.blockSignals(False)
            # Update token counter after loading
            self._update_token_counter(ai_slot)

    def _clear_editor(self):
        """Clear all editor fields."""
        self.current_scenario_name = None
        self.name_field.clear()
        for ai_slot, editor in self.prompt_editors.items():
            editor.clear()
            # Reset token counter
            self._update_token_counter(ai_slot)

    def _on_field_changed(self):
        """Handle field changes (marks as modified)."""
        self.modified = True

    def _update_token_counter(self, ai_slot: str):
        """Update the token counter for a specific AI slot."""
        editor = self.prompt_editors.get(ai_slot)
        counter = self.token_counters.get(ai_slot)
        if editor and counter:
            text = editor.toPlainText()
            token_estimate = len(text) // 4 if text else 0
            counter.setText(f"~{token_estimate} tokens")

    def _get_current_editor_data(self) -> tuple:
        """
        Get current data from editor fields.

        Returns:
            Tuple of (scenario_name, prompts_dict)
        """
        scenario_name = self.name_field.text().strip()
        prompts = {
            ai_slot: editor.toPlainText()
            for ai_slot, editor in self.prompt_editors.items()
        }
        return scenario_name, prompts

    def _on_new_scenario(self):
        """Create a new scenario."""
        # Prompt for name
        name, ok = QInputDialog.getText(
            self,
            "New Scenario",
            "Enter scenario name:",
            QLineEdit.EchoMode.Normal
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        # Check if name already exists
        if name in self.scenarios:
            QMessageBox.warning(
                self,
                "Duplicate Name",
                f"A scenario named '{name}' already exists."
            )
            return

        # Create new scenario with empty prompts
        self.scenarios[name] = {
            "AI-1": "",
            "AI-2": "",
            "AI-3": "",
            "AI-4": "",
            "AI-5": ""
        }

        # Refresh list and select new scenario
        self._populate_scenario_list()

        # Find and select the new item
        items = self.scenario_list.findItems(name, Qt.MatchFlag.MatchExactly)
        if items:
            self.scenario_list.setCurrentItem(items[0])

        self.modified = True

    def _on_rename_scenario(self):
        """Rename the current scenario."""
        if not self.current_scenario_name:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select a scenario to rename."
            )
            return

        old_name = self.current_scenario_name

        # Prompt for new name
        new_name, ok = QInputDialog.getText(
            self,
            "Rename Scenario",
            f"Rename '{old_name}' to:",
            QLineEdit.EchoMode.Normal,
            old_name
        )

        if not ok or not new_name.strip():
            return

        new_name = new_name.strip()

        # Check if unchanged
        if new_name == old_name:
            return

        # Check if new name already exists
        if new_name in self.scenarios:
            QMessageBox.warning(
                self,
                "Duplicate Name",
                f"A scenario named '{new_name}' already exists."
            )
            return

        # Rename in scenarios dict
        self.scenarios[new_name] = self.scenarios.pop(old_name)

        # Update current name
        self.current_scenario_name = new_name

        # Update name field
        self.name_field.setText(new_name)

        # Refresh list
        self._populate_scenario_list()

        # Re-select renamed item
        items = self.scenario_list.findItems(new_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.scenario_list.setCurrentItem(items[0])

        self.modified = True

    def _on_delete_scenario(self):
        """Delete the current scenario."""
        if not self.current_scenario_name:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select a scenario to delete."
            )
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{self.current_scenario_name}'?\n\n"
            "This cannot be undone (but a backup will be created when you save).",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Delete from scenarios dict
        del self.scenarios[self.current_scenario_name]

        # Clear editor
        self._clear_editor()

        # Refresh list
        self._populate_scenario_list()

        self.modified = True

    def _on_save(self):
        """Save all scenarios to config.py."""
        # Update current scenario from editor before saving
        if self.current_scenario_name:
            new_name, prompts = self._get_current_editor_data()

            # If name changed, handle rename
            if new_name != self.current_scenario_name:
                if new_name in self.scenarios:
                    QMessageBox.warning(
                        self,
                        "Duplicate Name",
                        f"Cannot rename to '{new_name}' - name already exists."
                    )
                    return
                # Remove old entry and add with new name
                del self.scenarios[self.current_scenario_name]
                self.scenarios[new_name] = prompts
                self.current_scenario_name = new_name
            else:
                # Just update the prompts
                self.scenarios[self.current_scenario_name] = prompts

        # Validate all scenarios
        is_valid, error = ScenarioManager.validate_all_scenarios(self.scenarios)
        if not is_valid:
            QMessageBox.critical(
                self,
                "Validation Error",
                f"Cannot save scenarios:\n{error}"
            )
            return

        # Save to config.py
        success, message = ScenarioManager.save_scenarios(self.scenarios)

        if success:
            QMessageBox.information(
                self,
                "Success",
                f"{message}\n\nRestart the application to use updated scenarios."
            )
            self.modified = False
            self.accept()  # Close dialog with success
        else:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save scenarios:\n{message}"
            )

    def closeEvent(self, event):
        """Handle dialog close event - warn if unsaved changes."""
        if self.modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to close?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        event.accept()
