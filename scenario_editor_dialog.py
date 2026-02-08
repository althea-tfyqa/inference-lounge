"""
Scenario Editor Dialog - UI for editing conversation scenarios

Provides a PyQt6 dialog for CRUDR operations on scenario configurations.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit,
    QPlainTextEdit, QPushButton, QLabel, QMessageBox, QSplitter,
    QWidget, QInputDialog, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from scenario_manager import (
    ScenarioManager, ScenarioValidationError,
    get_ai_slots, get_num_ais, get_prompt, get_model, get_name, DEFAULT_MODEL
)
from styles import COLORS  # Keep for minimal compatibility
from grouped_model_selector import GroupedModelComboBox
from config import AI_MODELS

# Minimal styling - using Qt defaults with slight tweaks
# For comprehensive theming, see UI_SPEC.md in project root


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

        # Track AI slot widgets - each AI slot has: prompt editor, model selector, name field, container
        self.ai_slot_widgets = {}  # Dict: "AI-1" -> {"container": QWidget, "prompt": QPlainTextEdit, "model": GroupedModelComboBox, "name": QLineEdit}
        self.ai_slots_layout = None  # Will hold the VBoxLayout for AI slot containers

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

        # Use Qt default styling (system native)
        # Custom theme should be applied via comprehensive stylesheet - see UI_SPEC.md
        pass

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
                color: {COLORS['text_glow']};
                padding: 4px;
                font-family: 'Comic Neue';
            }}
        """)
        layout.addWidget(header)

        # List widget
        self.scenario_list = QListWidget()
        self.scenario_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border: 1px solid transparent;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent_cyan']};
                color: white;
                border: 1px solid {COLORS['accent_cyan']};
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['border']};
            }}
        """)
        self.scenario_list.currentItemChanged.connect(self._on_scenario_selected)
        layout.addWidget(self.scenario_list)

        # List action buttons
        list_btn_layout = QVBoxLayout()
        list_btn_layout.setSpacing(4)

        self.new_btn = QPushButton("New Scenario")
        self.new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_cyan']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['text_glow']};
            }}
        """)
        self.new_btn.clicked.connect(self._on_new_scenario)
        list_btn_layout.addWidget(self.new_btn)

        self.rename_btn = QPushButton("Rename")
        self.rename_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']};
            }}
        """)
        self.rename_btn.clicked.connect(self._on_rename_scenario)
        list_btn_layout.addWidget(self.rename_btn)

        layout.addLayout(list_btn_layout)

        return widget

    def _create_editor(self) -> QWidget:
        """Create the editor widget with dynamic AI slots."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Scenario name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Scenario Name:")
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_dim']};
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
        """)
        name_layout.addWidget(name_label)

        self.name_field = QLineEdit()
        self.name_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_bright']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-family: 'Comic Neue';
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_cyan']};
            }}
        """)
        self.name_field.setPlaceholderText("Enter scenario name...")
        self.name_field.textChanged.connect(self._on_field_changed)
        name_layout.addWidget(self.name_field)

        layout.addLayout(name_layout)

        # Scroll area for AI slots
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
        """)

        scroll_content = QWidget()
        self.ai_slots_layout = QVBoxLayout(scroll_content)
        self.ai_slots_layout.setContentsMargins(0, 0, 0, 0)
        self.ai_slots_layout.setSpacing(12)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area, 1)  # Give scroll area flex space

        # Add/Remove AI slot buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        self.add_ai_btn = QPushButton("+ Add AI Slot")
        self.add_ai_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_cyan']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['text_glow']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['text_dim']};
            }}
        """)
        self.add_ai_btn.clicked.connect(self._on_add_ai_slot)
        button_row.addWidget(self.add_ai_btn)

        self.remove_ai_btn = QPushButton("− Remove Last AI")
        self.remove_ai_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['text_dim']};
            }}
        """)
        self.remove_ai_btn.clicked.connect(self._on_remove_ai_slot)
        button_row.addWidget(self.remove_ai_btn)

        button_row.addStretch()

        layout.addLayout(button_row)

        # Initialize with 2 AI slots (minimum)
        self._add_ai_slot_widget("AI-1")
        self._add_ai_slot_widget("AI-2")
        self._update_add_remove_buttons()

        return widget

    def _create_dialog_buttons(self) -> QHBoxLayout:
        """Create the bottom dialog buttons."""
        layout = QHBoxLayout()
        layout.setSpacing(8)

        # Delete button (left side) — red/coral for danger action
        self.delete_btn = QPushButton("Delete Scenario")
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: #C0392B;
            }}
        """)
        self.delete_btn.clicked.connect(self._on_delete_scenario)
        layout.addWidget(self.delete_btn)

        layout.addStretch()

        # Save and Cancel (right side)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['border']};
            }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save All Changes")
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_cyan']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-family: 'Comic Neue';
            }}
            QPushButton:hover {{
                background-color: {COLORS['text_glow']};
            }}
        """)
        self.save_btn.clicked.connect(self._on_save)
        layout.addWidget(self.save_btn)

        return layout

    def _add_ai_slot_widget(self, ai_name: str):
        """Add a single AI slot widget (name, model, prompt fields)."""
        # Container for this AI slot — white card with subtle border
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)

        # Header row with AI slot label
        header = QLabel(f"━━━ {ai_name} ━━━")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_glow']};
                font-weight: bold;
                font-size: 13px;
                padding: 4px;
                font-family: 'Comic Neue';
            }}
        """)
        container_layout.addWidget(header)

        # Name field row
        name_row = QHBoxLayout()
        name_label = QLabel("Display Name:")
        name_label.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-weight: bold;
            min-width: 100px;
            font-family: 'Comic Neue';
        """)
        name_row.addWidget(name_label)

        name_field = QLineEdit()
        name_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_bright']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-family: 'Comic Neue';
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_cyan']};
            }}
        """)
        name_field.setPlaceholderText(f"Optional custom name (defaults to {ai_name})")
        name_field.textChanged.connect(self._on_field_changed)
        name_row.addWidget(name_field)
        container_layout.addLayout(name_row)

        # Model selector row
        model_row = QHBoxLayout()
        model_label = QLabel("Model:")
        model_label.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-weight: bold;
            min-width: 100px;
            font-family: 'Comic Neue';
        """)
        model_row.addWidget(model_label)

        model_selector = GroupedModelComboBox(colors=COLORS, parent=self)
        # Simple styling - don't fight the delegate too hard
        model_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                color: {COLORS['text_normal']};
                border: 2px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-family: 'Comic Neue';
            }}
        """)
        # Style the popup view directly
        if model_selector.view():
            model_selector.view().setStyleSheet(f"""
                QTreeView {{
                    background-color: white;
                    color: {COLORS['text_normal']};
                    border: 2px solid {COLORS['border']};
                    selection-background-color: {COLORS['accent_cyan']};
                    selection-color: white;
                }}
                QTreeView::item {{
                    padding: 6px;
                }}
                QTreeView::item:hover {{
                    background-color: {COLORS['border']};
                }}
            """)
        model_selector.currentIndexChanged.connect(self._on_field_changed)
        model_row.addWidget(model_selector)
        container_layout.addLayout(model_row)

        # Prompt editor with token counter
        prompt_header_row = QHBoxLayout()
        prompt_label = QLabel("System Prompt:")
        prompt_label.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-weight: bold;
            font-family: 'Comic Neue';
        """)
        prompt_header_row.addWidget(prompt_label)
        prompt_header_row.addStretch()

        token_counter = QLabel("~0 tokens")
        token_counter.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-size: 10px;
            font-family: 'Comic Neue';
        """)
        prompt_header_row.addWidget(token_counter)
        container_layout.addLayout(prompt_header_row)

        prompt_editor = QPlainTextEdit()
        prompt_editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_bright']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                line-height: 1.5;
            }}
            QPlainTextEdit:focus {{
                border: 2px solid {COLORS['accent_cyan']};
            }}
        """)
        prompt_editor.setPlaceholderText(f"Enter system prompt for {ai_name}...")
        prompt_editor.setMinimumHeight(100)
        prompt_editor.textChanged.connect(self._on_field_changed)
        prompt_editor.textChanged.connect(lambda: self._update_token_counter_for_slot(ai_name))
        container_layout.addWidget(prompt_editor)

        # Store references
        self.ai_slot_widgets[ai_name] = {
            "container": container,
            "name": name_field,
            "model": model_selector,
            "prompt": prompt_editor,
            "token_counter": token_counter
        }

        # Add to layout
        self.ai_slots_layout.addWidget(container)

    def _on_add_ai_slot(self):
        """Add a new AI slot (up to 5 maximum)."""
        current_count = len(self.ai_slot_widgets)
        if current_count >= 5:
            return

        next_num = current_count + 1
        ai_name = f"AI-{next_num}"
        self._add_ai_slot_widget(ai_name)
        self._update_add_remove_buttons()
        self.modified = True

    def _on_remove_ai_slot(self):
        """Remove the last AI slot (minimum 2)."""
        current_count = len(self.ai_slot_widgets)
        if current_count <= 2:
            return

        # Remove last AI slot
        ai_name = f"AI-{current_count}"
        if ai_name in self.ai_slot_widgets:
            widgets = self.ai_slot_widgets.pop(ai_name)
            widgets["container"].setParent(None)
            widgets["container"].deleteLater()

        self._update_add_remove_buttons()
        self.modified = True

    def _update_add_remove_buttons(self):
        """Enable/disable add/remove buttons based on slot count."""
        current_count = len(self.ai_slot_widgets)
        self.add_ai_btn.setEnabled(current_count < 5)
        self.remove_ai_btn.setEnabled(current_count > 2)

    def _update_token_counter_for_slot(self, ai_name: str):
        """Update the token counter for a specific AI slot."""
        if ai_name not in self.ai_slot_widgets:
            return

        widgets = self.ai_slot_widgets[ai_name]
        text = widgets["prompt"].toPlainText()
        token_estimate = len(text) // 4 if text else 0
        widgets["token_counter"].setText(f"~{token_estimate} tokens")

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
        scenario_data = self.scenarios[scenario_name]

        # Block signals while loading to prevent marking as modified
        self.name_field.blockSignals(True)
        self.name_field.setText(scenario_name)
        self.name_field.blockSignals(False)

        # Clear existing AI slots
        for ai_name in list(self.ai_slot_widgets.keys()):
            widgets = self.ai_slot_widgets.pop(ai_name)
            widgets["container"].setParent(None)
            widgets["container"].deleteLater()

        # Get AI slots from scenario data
        ai_slots = get_ai_slots(scenario_data)

        # Create AI slot widgets for each slot in the scenario
        for ai_name in sorted(ai_slots):
            self._add_ai_slot_widget(ai_name)

            # Load data into widgets
            widgets = self.ai_slot_widgets[ai_name]

            # Name field
            widgets["name"].blockSignals(True)
            # get_name() returns ai_name as fallback if no custom name
            custom_name = get_name(scenario_data, ai_name)
            # Only show in field if it's different from ai_name (i.e., actually custom)
            widgets["name"].setText(custom_name if custom_name != ai_name else "")
            widgets["name"].blockSignals(False)

            # Model selector
            widgets["model"].blockSignals(True)
            model_id = get_model(scenario_data, ai_name) or DEFAULT_MODEL
            widgets["model"].set_model_by_id(model_id)
            widgets["model"].blockSignals(False)

            # Prompt editor
            widgets["prompt"].blockSignals(True)
            widgets["prompt"].setPlainText(get_prompt(scenario_data, ai_name))
            widgets["prompt"].blockSignals(False)

            # Update token counter
            self._update_token_counter_for_slot(ai_name)

        self._update_add_remove_buttons()

    def _clear_editor(self):
        """Clear all editor fields."""
        self.current_scenario_name = None
        self.name_field.clear()

        # Remove all AI slot widgets
        for ai_name in list(self.ai_slot_widgets.keys()):
            widgets = self.ai_slot_widgets.pop(ai_name)
            widgets["container"].setParent(None)
            widgets["container"].deleteLater()

        # Reset to 2 empty AI slots
        self._add_ai_slot_widget("AI-1")
        self._add_ai_slot_widget("AI-2")
        self._update_add_remove_buttons()

    def _on_field_changed(self):
        """Handle field changes (marks as modified)."""
        self.modified = True

    def _get_current_editor_data(self) -> tuple:
        """
        Get current data from editor fields in new nested format.

        Returns:
            Tuple of (scenario_name, scenario_data_dict)
            where scenario_data_dict is: {"AI-1": {"prompt": "...", "model": "...", "name": "..."}, ...}
        """
        scenario_name = self.name_field.text().strip()
        scenario_data = {}

        for ai_name, widgets in self.ai_slot_widgets.items():
            ai_data = {}

            # Prompt (required)
            ai_data["prompt"] = widgets["prompt"].toPlainText()

            # Model (optional, include if not default)
            model_id = widgets["model"].get_selected_model_id()
            if model_id and model_id != DEFAULT_MODEL:
                ai_data["model"] = model_id

            # Name (optional, include if provided)
            custom_name = widgets["name"].text().strip()
            if custom_name:
                ai_data["name"] = custom_name

            scenario_data[ai_name] = ai_data

        return scenario_name, scenario_data

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

        # Create new scenario with 2 empty AI slots (minimum) in new nested format
        self.scenarios[name] = {
            "AI-1": {"prompt": ""},
            "AI-2": {"prompt": ""}
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
