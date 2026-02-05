# Scenario Editor Implementation Plan

## Overview
Create a scenario editing tool for the Liminal Backrooms application that allows creating, reading, updating, deleting, and renaming (CRUDR) conversation scenarios stored in `config.py`.

## User Preferences
- **UI**: Separate dialog window (modal)
- **Features**: Basic CRUDR operations only
- **Backups**: Auto-backup on every save with timestamps

## What We're Building

A PyQt6 dialog window that:
1. Lists all existing scenarios in a scrollable list
2. Shows an editor with name field + 5 AI prompt text areas
3. Provides buttons for: New, Rename, Delete, Save, Cancel
4. Safely writes changes to `config.py` with automatic timestamped backups
5. Validates data before saving
6. Requires app restart to use updated scenarios (no hot reload)

## Architecture Decisions

### Why Separate Dialog?
- Scenario editing is infrequent - doesn't need to clutter main UI
- Modal prevents accidentally changing scenarios during conversations
- Matches existing pattern (QFileDialog, QMessageBox)

### Why Template-Based Config Writing?
- Simpler than AST manipulation
- More maintainable - user can read generated file
- Easier to debug when issues arise
- Trade-off: Must preserve exact Python dict format

### Why No Hot Reload?
- Config already requires restart (current behavior)
- Hot reload would require propagating changes through active conversation state, model selectors, etc.
- High complexity for minimal benefit

## Data Structure

### Current Format in config.py:
```python
SYSTEM_PROMPT_PAIRS = {
    "Scenario Name": {
        "AI-1": "system prompt text...",
        "AI-2": "system prompt text...",
        "AI-3": "system prompt text...",
        "AI-4": "system prompt text...",
        "AI-5": "system prompt text..."
    },
    # ... 11 scenarios total
}
```

### Validation Rules:
- Each scenario must have exactly 5 AI slots (AI-1 through AI-5)
- Slot values must be strings (can be empty)
- Scenario names must be unique
- No special characters that break Python syntax

## Implementation Steps

### Step 1: Create Scenario Manager (`scenario_manager.py`)
**Purpose**: Business logic layer - handles all config.py reading/writing

**Functions needed**:
- `load_scenarios()` - Extract SYSTEM_PROMPT_PAIRS from config.py safely
- `save_scenarios(scenarios_dict)` - Write scenarios back to config.py with validation
- `validate_scenario(name, prompts)` - Check structure is valid
- `create_backup()` - Make timestamped backup before any write
- `generate_config_content(scenarios_dict)` - Use template to create new config.py content

**Key details**:
- Use `ast.literal_eval()` to safely parse the dict from config.py
- Template preserves everything in config.py except SYSTEM_PROMPT_PAIRS
- Atomic write pattern: write to `config.py.tmp`, validate, then `os.rename()`
- Backup format: `config.py.backup-YYYYMMDD-HHMMSS`

### Step 2: Create Editor Dialog (`scenario_editor_dialog.py`)
**Purpose**: UI for editing scenarios

**Layout**:
```
┌─────────────────────────────────────────────┐
│ Scenario Editor                         [X] │
├──────────────┬──────────────────────────────┤
│ Scenarios    │ Scenario Name:               │
│              │ [text field]                 │
│ ┌──────────┐ │                              │
│ │Backrooms │ │ AI-1 Prompt:                 │
│ │Group Chat│ │ [multi-line text]            │
│ │D&D       │ │                              │
│ │...       │ │ AI-2 Prompt:                 │
│ └──────────┘ │ [multi-line text]            │
│              │ ... (AI-3, AI-4, AI-5)       │
│ [New]        │                              │
│ [Rename]     │ [Save] [Cancel] [Delete]     │
└──────────────┴──────────────────────────────┘
```

**Widgets**:
- Left: `QListWidget` for scenario list
- Right top: `QLineEdit` for scenario name
- Right middle: 5 x `QPlainTextEdit` for AI prompts (labeled AI-1 through AI-5)
- Bottom: Buttons with styling from `styles.py`

**Behavior**:
- Clicking scenario in list loads it into editor
- "New" creates blank scenario (prompts user for name)
- "Rename" changes selected scenario's name
- "Delete" removes scenario (with confirmation)
- "Save" validates and writes to config.py, creates backup
- "Cancel" closes dialog without saving

**Styling**: Use functions from `styles.py`:
- `get_button_style(COLORS['accent_cyan'])` for Save button
- `get_button_style(COLORS['accent_red'])` for Delete button
- `get_frame_style('message')` for containers
- Cyberpunk/CRT theme with sharp corners

### Step 3: Add Entry Point to GUI (`gui.py`)
**Location**: In `ControlPanel` class, near the scenario selector (around line 2970)

**Changes**:
1. Import the dialog: `from scenario_editor_dialog import ScenarioEditorDialog`
2. Add button after `prompt_pair_selector`:
   ```python
   edit_scenarios_btn = QPushButton("Edit Scenarios")
   edit_scenarios_btn.clicked.connect(self.open_scenario_editor)
   ```
3. Add method:
   ```python
   def open_scenario_editor(self):
       dialog = ScenarioEditorDialog(self)
       if dialog.exec():  # If user saved changes
           QMessageBox.information(self, "Restart Required",
               "Scenarios saved! Restart the app to use updated scenarios.")
           # Optionally: refresh the scenario dropdown
   ```

### Step 4: Testing & Validation
**Manual testing checklist**:
- [ ] Create new scenario with 5 prompts
- [ ] Edit existing scenario
- [ ] Rename scenario (name changes everywhere)
- [ ] Delete scenario (with confirmation)
- [ ] Cancel without saving (no changes persist)
- [ ] Verify backup created with timestamp
- [ ] Verify config.py syntax is valid Python after save
- [ ] Restart app and confirm new/edited scenarios appear in dropdown
- [ ] Test edge cases: empty prompts, long prompts, special characters

**Validation tests**:
- [ ] Duplicate scenario name rejected
- [ ] Missing AI slots rejected
- [ ] Invalid Python syntax rejected (shouldn't happen with proper escaping)

## Critical Files

### New Files to Create:
1. **`/Users/adelwich/Projects/tools/liminal_backrooms/scenario_manager.py`**
   - All config.py manipulation logic
   - No UI dependencies (pure Python)
   - ~200-300 lines

2. **`/Users/adelwich/Projects/tools/liminal_backrooms/scenario_editor_dialog.py`**
   - PyQt6 dialog UI
   - Calls scenario_manager for data operations
   - ~300-400 lines

### Files to Modify:
3. **`/Users/adelwich/Projects/tools/liminal_backrooms/gui.py`**
   - Add "Edit Scenarios" button in ControlPanel class (around line 2970)
   - Import and instantiate dialog
   - ~10-20 lines added

### Files to Reference:
4. **`/Users/adelwich/Projects/tools/liminal_backrooms/config.py`**
   - Study SYSTEM_PROMPT_PAIRS structure (lines 181-1138)
   - Understand formatting requirements

5. **`/Users/adelwich/Projects/tools/liminal_backrooms/styles.py`**
   - Use styling functions for consistent look

6. **`/Users/adelwich/Projects/tools/liminal_backrooms/tools/debug_tools.py`**
   - Reference StylesheetEditor pattern (lines 250-349)
   - Example of QPlainTextEdit with Apply/Reset buttons

## Verification Plan

### After Implementation:
1. Run the app: `poetry run python main.py`
2. Click "Edit Scenarios" button in control panel
3. Create a test scenario named "Test Scene"
4. Add prompts for all 5 AI slots
5. Click Save
6. Verify `config.py.backup-TIMESTAMP` was created
7. Open `config.py` and confirm "Test Scene" is present
8. Restart the app
9. Check that "Test Scene" appears in scenario dropdown
10. Select it and start a conversation to verify prompts work

### Edge Case Testing:
- Scenario names with quotes: `"Alice's" Adventure`
- Multi-line prompts with special formatting
- Empty AI slots (empty strings)
- Very long prompts (>5000 characters)
- Cancel without saving (changes discarded)

## Safety Features

1. **Timestamped Backups**: Every save creates `config.py.backup-YYYYMMDD-HHMMSS`
2. **Atomic Writes**: Write to temp file, validate, then rename (never corrupts config)
3. **Validation**: Check structure before writing
4. **Confirmation Dialogs**: Confirm before deleting scenarios
5. **Syntax Validation**: Use `ast.parse()` to verify valid Python before finalizing

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Breaking config.py syntax | Multi-layer validation + backups |
| User edits config.py manually during editing | Read fresh on dialog open + warn in tooltip |
| Very long prompts causing issues | QPlainTextEdit handles this well, no explicit limit |
| Forgetting to restart app | Show explicit message after save |
| Accumulating backup files over time | User can manually delete old backups, or add cleanup later |

## Why This Approach Works for You

Based on your profile (advanced beginner, prefers simple/maintainable):
- **Separation of concerns**: scenario_manager.py has zero UI code - easy to understand and test
- **Familiar patterns**: Uses PyQt6 widgets you've seen before
- **Safe by default**: Multiple validation layers prevent breaking things
- **Small steps**: Can implement and test one piece at a time
- **No magic**: Template-based approach is straightforward, no complex AST manipulation
- **Git-friendly**: You can always revert if something goes wrong

## Next Steps After Approval

1. Create `scenario_manager.py` with load/save/validate functions
2. Test it independently (can write simple test script)
3. Create `scenario_editor_dialog.py` with UI
4. Test dialog in isolation
5. Integrate into main GUI
6. Full end-to-end testing
7. Document usage for future reference
