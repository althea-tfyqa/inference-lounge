"""
Settings Dialog - Unified configuration interface for Inference Lounge

Replaces the Control Panel with a modal settings dialog that houses all
configuration options in an organized tabbed interface.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QTabWidget, QWidget, QMessageBox,
    QSplitter, QListWidget, QLineEdit, QPlainTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import SYSTEM_PROMPT_PAIRS, STARTING_PROMPTS
from styles import COLORS, get_combobox_style, get_button_style, get_checkbox_style, get_scrollbar_style
from grouped_model_selector import GroupedModelComboBox
from scenario_editor_dialog import ScenarioEditorDialog
from scenario_manager import StartingPromptManager


class NoScrollComboBox(QComboBox):
    """ComboBox that doesn't steal scroll events"""
    def wheelEvent(self, event):
        event.ignore()


class SettingsDialog(QDialog):
    """
    Unified settings dialog for all configuration options.

    Organizes settings into tabs:
    - Conversation: Mode, iterations, AI count
    - AI Models: All 5 model selectors
    - Scenarios: Scenario selector + Edit button
    - Starting Prompts: Prompt editor (new feature)
    - Options: Auto-image, developer tools, etc.
    - Export: Export, View HTML, BackroomsBench buttons
    """

    def __init__(self, parent, current_settings):
        super().__init__(parent)
        self.current_settings = current_settings
        self.setWindowTitle("⚙ Settings")
        self.setMinimumSize(900, 700)

        # Track modifications to starting prompts
        self.prompts_modified = False

        self._setup_ui()
        self._load_current_settings()

    def _setup_ui(self):
        """Set up the dialog UI with tabs"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_dim']};
                padding: 10px 20px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QTabBar::tab:hover {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['accent_cyan']};
                border-bottom: 2px solid {COLORS['accent_cyan']};
            }}
        """)

        # Create tabs
        self.tabs.addTab(self._create_conversation_tab(), "Conversation")
        self.tabs.addTab(self._create_models_tab(), "AI Models")
        self.tabs.addTab(self._create_scenarios_tab(), "Scenarios")
        self.tabs.addTab(self._create_prompts_tab(), "Starting Prompts")
        self.tabs.addTab(self._create_options_tab(), "Options")
        self.tabs.addTab(self._create_export_tab(), "Export")

        layout.addWidget(self.tabs)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(12, 12, 12, 12)
        button_layout.setSpacing(8)
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(get_button_style(COLORS['text_dim']))
        cancel_btn.setMinimumWidth(100)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setStyleSheet(get_button_style(COLORS['accent_cyan']))
        save_btn.setMinimumWidth(100)
        save_btn.setDefault(True)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

        # Apply dark theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_dark']};
                color: {COLORS['text_normal']};
            }}
        """)

    def _create_conversation_tab(self):
        """Create the Conversation settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Mode selector
        mode_label = QLabel("▸ CONVERSATION MODE")
        mode_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(mode_label)

        self.mode_selector = NoScrollComboBox()
        self.mode_selector.addItems(["AI-AI", "Human-AI"])
        self.mode_selector.setStyleSheet(get_combobox_style())
        layout.addWidget(self.mode_selector)

        # Iterations selector
        iterations_label = QLabel("▸ ITERATIONS")
        iterations_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-top: 10px;")
        layout.addWidget(iterations_label)

        self.iterations_selector = NoScrollComboBox()
        self.iterations_selector.addItems(["1", "2", "4", "6", "12", "100"])
        self.iterations_selector.setStyleSheet(get_combobox_style())
        layout.addWidget(self.iterations_selector)

        # Number of AIs selector
        num_ais_label = QLabel("▸ NUMBER OF AIs")
        num_ais_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-top: 10px;")
        layout.addWidget(num_ais_label)

        self.num_ais_selector = NoScrollComboBox()
        self.num_ais_selector.addItems(["1", "2", "3", "4", "5"])
        self.num_ais_selector.setCurrentText("3")
        self.num_ais_selector.setStyleSheet(get_combobox_style())
        self.num_ais_selector.currentTextChanged.connect(self._on_num_ais_changed)
        layout.addWidget(self.num_ais_selector)

        # AI Invite Tier
        invite_tier_label = QLabel("▸ AI INVITE TIER")
        invite_tier_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-top: 10px;")
        layout.addWidget(invite_tier_label)

        invite_tier_info = QLabel("Controls which models AIs can add to the chat")
        invite_tier_info.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 9px;")
        layout.addWidget(invite_tier_info)

        # Button group for invite tier
        btn_group_container = QWidget()
        btn_group_layout = QHBoxLayout(btn_group_container)
        btn_group_layout.setContentsMargins(0, 0, 0, 0)
        btn_group_layout.setSpacing(0)

        self.invite_free_btn = QPushButton("Free")
        self.invite_paid_btn = QPushButton("Paid")
        self.invite_both_btn = QPushButton("All")

        self._invite_tier_buttons = [self.invite_free_btn, self.invite_paid_btn, self.invite_both_btn]

        toggle_btn_style = f"""
            QPushButton {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_dim']};
                border: 1px solid {COLORS['bg_light']};
                padding: 8px 16px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_normal']};
            }}
            QPushButton:checked {{
                background-color: #164E63;
                color: {COLORS['text_bright']};
                border: 1px solid {COLORS['accent_cyan']};
            }}
        """

        for btn in self._invite_tier_buttons:
            btn.setCheckable(True)
            btn.setStyleSheet(toggle_btn_style)
            btn.clicked.connect(self._on_invite_tier_clicked)
            btn_group_layout.addWidget(btn)

        # Round corners on first and last buttons
        self.invite_free_btn.setStyleSheet(toggle_btn_style + "QPushButton { border-radius: 3px 0px 0px 3px; }")
        self.invite_both_btn.setStyleSheet(toggle_btn_style + "QPushButton { border-radius: 0px 3px 3px 0px; }")

        self.invite_free_btn.setChecked(True)

        layout.addWidget(btn_group_container)

        # Allow duplicate models checkbox
        self.allow_duplicate_models_checkbox = QCheckBox("Allow duplicate models")
        self.allow_duplicate_models_checkbox.setStyleSheet(get_checkbox_style())
        self.allow_duplicate_models_checkbox.setToolTip("Allow AIs to add models that are already in the conversation")
        layout.addWidget(self.allow_duplicate_models_checkbox)

        layout.addStretch()

        return widget

    def _create_models_tab(self):
        """Create the AI Models settings tab"""
        widget = QWidget()

        # Make scrollable for when we have many models
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
            {get_scrollbar_style()}
        """)

        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        models_label = QLabel("▸ AI MODELS")
        models_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(models_label)

        # Create all 5 AI model selectors
        self.ai_model_containers = []
        self.ai_model_selectors = []

        for i in range(1, 6):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(5)

            ai_label = QLabel(f"AI-{i}")
            ai_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px;")
            container_layout.addWidget(ai_label)

            model_selector = GroupedModelComboBox(colors=COLORS, parent=self)
            model_selector.setStyleSheet(get_combobox_style())
            container_layout.addWidget(model_selector)

            self.ai_model_containers.append(container)
            self.ai_model_selectors.append(model_selector)
            layout.addWidget(container)

        layout.addStretch()

        scroll_area.setWidget(scroll_content)

        # Wrap scroll area in widget with layout
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll_area)

        return wrapper

    def _create_scenarios_tab(self):
        """Create the Scenarios settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        scenario_label = QLabel("▸ CONVERSATION SCENARIO")
        scenario_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(scenario_label)

        self.scenario_selector = NoScrollComboBox()
        self.scenario_selector.setStyleSheet(get_combobox_style())
        layout.addWidget(self.scenario_selector)

        # Edit Scenarios button
        edit_btn = QPushButton("Edit Scenarios")
        edit_btn.clicked.connect(self._open_scenario_editor)
        edit_btn.setStyleSheet(get_button_style(COLORS['accent_cyan']))
        layout.addWidget(edit_btn)

        layout.addStretch()

        return widget

    def _create_prompts_tab(self):
        """Create the Starting Prompts editor tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Splitter: list on left (30%), editor on right (70%)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left: Prompt list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        list_header = QLabel("Starting Prompts")
        list_header.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {COLORS['accent_cyan']};
            padding: 4px;
        """)
        left_layout.addWidget(list_header)

        self.prompt_list = QListWidget()
        self.prompt_list.setStyleSheet(f"""
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
                border-bottom: 1px solid {COLORS['bg_dark']};
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_light']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['accent_cyan']};
                border-left: 3px solid {COLORS['accent_cyan']};
            }}
        """)
        self.prompt_list.currentTextChanged.connect(self._on_prompt_selected_in_list)
        left_layout.addWidget(self.prompt_list)

        # New/Delete buttons
        btn_layout = QHBoxLayout()
        new_btn = QPushButton("New")
        new_btn.clicked.connect(self._new_prompt)
        new_btn.setStyleSheet(get_button_style(COLORS['accent_cyan']))

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._delete_prompt)
        delete_btn.setStyleSheet(get_button_style(COLORS['notify_error']))

        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(delete_btn)
        left_layout.addLayout(btn_layout)

        # Right: Editor
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        editor_header = QLabel("Edit Prompt")
        editor_header.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {COLORS['accent_cyan']};
            padding: 4px;
        """)
        right_layout.addWidget(editor_header)

        # Prompt name editor
        name_label = QLabel("Prompt Name:")
        name_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px;")
        right_layout.addWidget(name_label)

        self.prompt_name_input = QLineEdit()
        self.prompt_name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_normal']};
                border: 1px solid {COLORS['bg_light']};
                padding: 8px;
                border-radius: 3px;
                font-size: 11px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['accent_cyan']};
            }}
        """)
        right_layout.addWidget(self.prompt_name_input)

        # Prompt text editor
        text_label = QLabel("Prompt Text:")
        text_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px; margin-top: 10px;")
        right_layout.addWidget(text_label)

        self.prompt_text_input = QPlainTextEdit()
        self.prompt_text_input.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text_normal']};
                border: 1px solid {COLORS['bg_light']};
                padding: 8px;
                border-radius: 3px;
                font-size: 11px;
                font-family: monospace;
            }}
            QPlainTextEdit:focus {{
                border: 1px solid {COLORS['accent_cyan']};
            }}
        """)
        self.prompt_text_input.textChanged.connect(self._update_token_count)
        right_layout.addWidget(self.prompt_text_input)

        # Token counter
        self.token_count_label = QLabel("Tokens: 0")
        self.token_count_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 9px;")
        right_layout.addWidget(self.token_count_label)

        # Save button
        save_btn = QPushButton("Save Prompt")
        save_btn.clicked.connect(self._save_prompt)
        save_btn.setStyleSheet(get_button_style(COLORS['accent_cyan']))
        right_layout.addWidget(save_btn)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 600])

        layout.addWidget(splitter)

        # Load prompts into list
        self._load_prompts_list()

        return widget

    def _create_options_tab(self):
        """Create the Options settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        options_label = QLabel("▸ OPTIONS")
        options_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(options_label)

        # Auto-image checkbox
        self.auto_image_checkbox = QCheckBox("Auto-generate images for !image commands")
        self.auto_image_checkbox.setStyleSheet(get_checkbox_style())
        layout.addWidget(self.auto_image_checkbox)

        layout.addStretch()

        return widget

    def _create_export_tab(self):
        """Create the Export settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        export_label = QLabel("▸ EXPORT & EVALUATION")
        export_label.setStyleSheet(f"color: {COLORS['text_glow']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(export_label)

        info_label = QLabel("Note: Export buttons have been moved to the File menu for easier access during conversations.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 10px; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)

        layout.addStretch()

        return widget

    def _load_current_settings(self):
        """Load current settings into the dialog controls"""
        # Conversation tab
        self.mode_selector.setCurrentText(self.current_settings.get('mode', 'AI-AI'))
        self.iterations_selector.setCurrentText(str(self.current_settings.get('iterations', 4)))
        self.num_ais_selector.setCurrentText(str(self.current_settings.get('num_ais', 3)))

        # Invite tier buttons
        invite_tier = self.current_settings.get('invite_tier', 'Free')
        for btn in self._invite_tier_buttons:
            btn.setChecked(False)
        if invite_tier == 'Free':
            self.invite_free_btn.setChecked(True)
        elif invite_tier == 'Paid':
            self.invite_paid_btn.setChecked(True)
        else:
            self.invite_both_btn.setChecked(True)

        self.allow_duplicate_models_checkbox.setChecked(self.current_settings.get('allow_duplicate_models', False))

        # AI Models tab
        ai_models = self.current_settings.get('ai_models', [])
        for i, model_id in enumerate(ai_models):
            if i < len(self.ai_model_selectors):
                self.ai_model_selectors[i].set_model_by_id(model_id)

        # Update visibility based on num_ais
        self._on_num_ais_changed(str(self.current_settings.get('num_ais', 3)))

        # Scenarios tab
        self.scenario_selector.clear()
        self.scenario_selector.addItems(sorted(SYSTEM_PROMPT_PAIRS.keys()))
        current_scenario = self.current_settings.get('scenario', list(SYSTEM_PROMPT_PAIRS.keys())[0] if SYSTEM_PROMPT_PAIRS else "")
        if current_scenario:
            self.scenario_selector.setCurrentText(current_scenario)

        # Options tab
        self.auto_image_checkbox.setChecked(self.current_settings.get('auto_image', False))

    def _on_num_ais_changed(self, num_str):
        """Show/hide AI model selectors based on number of AIs"""
        num_ais = int(num_str)
        for i, container in enumerate(self.ai_model_containers):
            container.setVisible(i < num_ais)

    def _on_invite_tier_clicked(self):
        """Handle invite tier button clicks (radio button behavior)"""
        sender = self.sender()
        # Uncheck all others
        for btn in self._invite_tier_buttons:
            if btn != sender:
                btn.setChecked(False)
        # Ensure at least one is checked
        if not sender.isChecked():
            sender.setChecked(True)

    def _open_scenario_editor(self):
        """Open the scenario editor dialog"""
        dialog = ScenarioEditorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload scenario list
            self.scenario_selector.clear()
            self.scenario_selector.addItems(sorted(SYSTEM_PROMPT_PAIRS.keys()))

    def _load_prompts_list(self):
        """Load starting prompts into the list widget"""
        self.prompt_list.clear()
        try:
            prompts = StartingPromptManager.load_prompts()
            for name in sorted(prompts.keys()):
                self.prompt_list.addItem(name)
            if self.prompt_list.count() > 0:
                self.prompt_list.setCurrentRow(0)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load starting prompts: {str(e)}")

    def _on_prompt_selected_in_list(self, prompt_name):
        """Load selected prompt into editor"""
        if not prompt_name:
            return

        try:
            prompts = StartingPromptManager.load_prompts()
            if prompt_name in prompts:
                self.prompt_name_input.setText(prompt_name)
                self.prompt_text_input.setPlainText(prompts[prompt_name])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load prompt: {str(e)}")

    def _new_prompt(self):
        """Create a new prompt"""
        self.prompt_name_input.setText("New Prompt")
        self.prompt_text_input.setPlainText("")
        self.prompt_name_input.setFocus()
        self.prompt_name_input.selectAll()

    def _save_prompt(self):
        """Save the current prompt"""
        name = self.prompt_name_input.text().strip()
        text = self.prompt_text_input.toPlainText()

        if not name:
            QMessageBox.warning(self, "Error", "Prompt name cannot be empty")
            return

        try:
            prompts = StartingPromptManager.load_prompts()

            # Check if this is a rename
            current_item = self.prompt_list.currentItem()
            old_name = current_item.text() if current_item else None

            if old_name and old_name != name and name in prompts:
                QMessageBox.warning(self, "Error", f"A prompt named '{name}' already exists")
                return

            # Update or add the prompt
            prompts[name] = text

            # Remove old name if renamed
            if old_name and old_name != name and old_name in prompts:
                del prompts[old_name]

            # Save to file
            success, message = StartingPromptManager.save_prompts(prompts)

            if success:
                self.prompts_modified = True
                self._load_prompts_list()
                # Select the saved prompt
                items = self.prompt_list.findItems(name, Qt.MatchFlag.MatchExactly)
                if items:
                    self.prompt_list.setCurrentItem(items[0])
                QMessageBox.information(self, "Success", "Starting prompt saved successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save prompt: {message}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save prompt: {str(e)}")

    def _delete_prompt(self):
        """Delete the selected prompt"""
        current_item = self.prompt_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "No prompt selected")
            return

        prompt_name = current_item.text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the prompt '{prompt_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = StartingPromptManager.delete_prompt(prompt_name)

            if success:
                self.prompts_modified = True
                self._load_prompts_list()
                QMessageBox.information(self, "Success", "Prompt deleted successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete prompt: {message}")

    def _update_token_count(self):
        """Update the token counter (approximate)"""
        text = self.prompt_text_input.toPlainText()
        # Rough approximation: 1 token ≈ 4 characters
        tokens = len(text) // 4
        self.token_count_label.setText(f"Tokens: ~{tokens}")

    def get_settings(self):
        """Return all settings from the dialog"""
        # Get invite tier
        if self.invite_free_btn.isChecked():
            invite_tier = 'Free'
        elif self.invite_paid_btn.isChecked():
            invite_tier = 'Paid'
        else:
            invite_tier = 'Both'

        # Get AI models (all 5, even if not all are used)
        ai_models = []
        for selector in self.ai_model_selectors:
            ai_models.append(selector.get_selected_model_id())

        return {
            'mode': self.mode_selector.currentText(),
            'iterations': int(self.iterations_selector.currentText()),
            'num_ais': int(self.num_ais_selector.currentText()),
            'invite_tier': invite_tier,
            'allow_duplicate_models': self.allow_duplicate_models_checkbox.isChecked(),
            'ai_models': ai_models,
            'scenario': self.scenario_selector.currentText(),
            'auto_image': self.auto_image_checkbox.isChecked(),
        }
