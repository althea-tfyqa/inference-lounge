# Inference Lounge - UI Component Specification

**Purpose**: Comprehensive breakdown of UI structure for design planning and stylesheet development.

**Status**: Refactored architecture with unified scenarios (Feb 2026). Main app uses comic book theme; dialogs need cohesive theming.

---

## Architecture Overview

### Main Application Window (`gui.py` - LiminalBackroomsApp)
- **Comic book theme**: Bangers font for headers, Comic Neue for body, per-speaker color coding
- **Three-column layout**: Portrait column (140px) | Conversation pane (flex) | (optional future sidebar)
- **Two-mode UI**: Entry mode (configure) → Viewing mode (conversation active)

### Settings Dialog (`settings_dialog.py` - SettingsDialog)
- **Modal dialog**: 900x700px minimum
- **Tabbed interface**: 6 tabs for different setting categories
- **File location**: `settings_dialog.py` (~700 lines)

### Scenario Editor Dialog (`scenario_editor_dialog.py` - ScenarioEditorDialog)
- **Modal dialog**: 1000x700px minimum
- **Split pane**: Scenario list (30%) | Editor (70%)
- **Dynamic AI slots**: 2-5 AI configurations per scenario
- **File location**: `scenario_editor_dialog.py` (~600 lines)

---

## Main Application Components

### 1. Portrait Column (`portrait_column_widget.py`)
**Class**: `PortraitColumnWidget`
**Purpose**: Shows active participant portraits with speaker highlighting

**Widgets**:
- `QWidget` container (140px fixed width)
- `PortraitCard` for each participant
  - `CircularPortraitWidget` - circular portrait with glow
  - `QLabel` - character name badge

**Current Styling**:
- Background: Vertical gradient `#FAF6EE` (cream) → `#EDE4D4`
- Border-right: 4px solid black
- Active speaker: 6px border + glow in speaker color
- Colors defined: `COMIC_COLORS` in `styles.py`

**Per-Speaker Colors** (`MessageWidget.AI_COLORS`):
- AI-1: Red `#E74E52`
- AI-2: Teal `#17C0AA`
- AI-3: Gold `#FFA630`
- AI-4: Purple `#9B59B6`
- AI-5: Navy `#34495E`

---

### 2. Conversation Pane (`gui.py` - ConversationPane)
**Purpose**: Main interaction area - input field, messages, controls

**Sub-components**:

#### a) Banner Frame (top)
- `QFrame` with app title/logo
- Background: `#FF2954` (bright red) - comic style
- Font: Bangers, white text

#### b) Entry Panel (entry mode only)
**Widgets**:
- `QComboBox` - Scenario selector
- `QCheckBox` - "Enable AI image generation"
- Background: `#FAF6EE` (cream)
- Border: 3px solid black

**Design Note**: After refactor, this is MINIMAL - just scenario picker. Models/num_ais come from scenario data.

#### c) Starting Prompt Widget (`StartingPromptWidget`)
**Widgets**:
- `QComboBox` - Prompt dropdown
- `QLineEdit` - Text input
- `QLabel` - Token counter (~N tokens)
- Buttons: "IMAGE" (upload), "CONVERSE" (submit)

**Current Styling**: Comic theme - black borders, colorful buttons

#### d) Chat Scroll Area
**Widgets**:
- `QScrollArea` containing message widgets
- Each message: `MessageWidget` with per-speaker border colors
- Typing indicators: `ThinkingBubbleWithLabel` (Ben-Day dot pattern)

**Message Styling**:
- Border-left: 8px solid [speaker color]
- Background: Alternating cream/white
- Font: Comic Neue

---

## Settings Dialog Structure

### File: `settings_dialog.py`

**Main Container**: `QDialog` with `QTabWidget`

**Tab Bar Styling Points**:
- Background color
- Active tab indicator
- Inactive tab color
- Font weight/size

**6 Tabs**:

#### Tab 1: Conversation
**Widgets**:
- `QLabel` - "CONVERSATION MODE" header
- `QWidget` - Toggle buttons (AI-AI / AI-User / User-User)
  - Layout: `QHBoxLayout` with 3 `QPushButton`s
- `QLabel` - "MAX ITERATIONS" header
- `QComboBox` - Dropdown (2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 50)
- `QLabel` - "NUMBER OF AIs" header
- `QComboBox` - Dropdown (2, 3, 4, 5)
- `QLabel` - "INVITE TIER" header
- `QWidget` - Toggle buttons (Free / Paid / All)

**Styling Needs**:
- Section headers (uppercase labels)
- Toggle button states (active/inactive)
- Dropdown styling

#### Tab 2: AI Models
**Widgets**:
- `QLabel` - "▸ AI MODELS" header
- 5x `GroupedModelComboBox` - Hierarchical model selectors
  - Each preceded by `QLabel` - "AI-1", "AI-2", etc.

**Styling Challenge**: `GroupedModelComboBox` uses custom delegate (`GroupedItemDelegate`) for hierarchical display
- Tier headers (Paid/Free)
- Provider headers (Anthropic, Google, etc.)
- Model items (selectable)

**Files involved**:
- `grouped_model_selector.py` - Widget + delegate
- Colors passed via constructor: `GroupedModelComboBox(colors=dict, parent=self)`

#### Tab 3: Scenarios
**Widgets**:
- `QLabel` - "▸ CURRENT SCENARIO" header
- `QComboBox` - Scenario selector
- `QPushButton` - "Edit Scenarios..." (opens scenario editor)

#### Tab 4: Starting Prompts
**Widgets**:
- `QLabel` - "▸ STARTING PROMPTS" header
- `QListWidget` - Prompt list (scrollable)
  - Each item shows prompt preview
- Buttons: "New Prompt", "Delete Selected"
- `QWidget` - Editor section
  - `QLabel` - "Name:"
  - `QLineEdit` - Prompt name
  - `QLabel` - "Prompt Text:"
  - `QPlainTextEdit` - Prompt content
  - `QPushButton` - "Save Changes"

#### Tab 5: Options
**Widgets**:
- `QLabel` - "▸ OPTIONS" header
- `QCheckBox` - "Auto-generate images for conversations"
- `QCheckBox` - "Allow duplicate models across AI slots"
- `QCheckBox` - "Show developer tools"

#### Tab 6: Export
**Widgets**:
- `QLabel` - "▸ EXPORT" header
- `QPushButton` - "Export Conversation (JSON)"
- `QPushButton` - "View HTML Report"
- `QPushButton` - "Run BackroomsBench"

**Bottom Buttons** (all tabs):
- `QPushButton` - "Cancel" (left-aligned after stretch)
- `QPushButton` - "Save" (primary action, default button)

---

## Scenario Editor Dialog Structure

### File: `scenario_editor_dialog.py`

**Main Layout**: `QSplitter` (horizontal) with dialog buttons below

### Left Pane: Scenario List (30%)

**Widgets**:
- `QLabel` - "Scenarios" header
- `QListWidget` - Scenario list
  - Displays all scenario names
  - Single selection
- `QPushButton` - "New Scenario"
- `QPushButton` - "Rename"

**Styling Needs**:
- List item normal state
- List item selected state
- List item hover state

### Right Pane: Editor (70%)

**Widgets**:
- `QLineEdit` - Scenario name field (top)
- `QScrollArea` - Contains AI slot cards
- `QPushButton` - "+ Add AI Slot" (max 5)
- `QPushButton` - "− Remove Last AI" (min 2)

**AI Slot Card** (repeated 2-5 times):
Each slot is a `QWidget` container with:
- `QLabel` - Header "━━━ AI-N ━━━"
- `QLabel` - "Display Name:"
- `QLineEdit` - Custom name input (optional)
- `QLabel` - "Model:"
- `GroupedModelComboBox` - Model selector
- `QLabel` - "System Prompt:" + token counter
- `QPlainTextEdit` - Prompt editor (monospace font)

**Styling Needs**:
- Card container (border, background, padding)
- Header styling (centered, colored)
- Input field consistency
- Prompt editor (monospace, syntax-appropriate colors)

**Bottom Buttons**:
- `QPushButton` - "Delete Scenario" (left, danger color)
- `QPushButton` - "Cancel" (right)
- `QPushButton` - "Save All Changes" (right, primary)

---

## Widget Type Inventory

### Standard Qt Widgets Used

1. **QDialog** - Modal dialogs
2. **QTabWidget** / **QTabBar** - Tabbed interface
3. **QSplitter** - Resizable split panes
4. **QScrollArea** - Scrollable content
5. **QListWidget** - Item lists
6. **QComboBox** - Dropdowns
7. **QLineEdit** - Single-line text input
8. **QPlainTextEdit** - Multi-line text editor
9. **QLabel** - Text labels, headers
10. **QPushButton** - Buttons
11. **QCheckBox** - Toggle checkboxes
12. **QWidget** - Generic containers
13. **QFrame** - Styled containers

### Custom Widgets

1. **GroupedModelComboBox** (`grouped_model_selector.py`)
   - Extends: `QComboBox`
   - Delegate: `GroupedItemDelegate` (custom paint methods)
   - Purpose: Hierarchical model selection
   - Color configuration: Passed via constructor

2. **PortraitColumnWidget** (`portrait_column_widget.py`)
   - Extends: `QWidget`
   - Purpose: Character portraits with active speaker highlighting

3. **CircularPortraitWidget** (`portrait_column_widget.py`)
   - Extends: `QWidget`
   - Purpose: Circular portrait with custom painting

4. **MessageWidget** (`gui.py`)
   - Extends: `QWidget`
   - Purpose: Chat message display
   - Contains: Sender label, content area, actions menu

5. **ThinkingBubbleWithLabel** (`thinking_bubble_widget.py`)
   - Extends: `QWidget`
   - Purpose: Typing indicator with Ben-Day dots

6. **StartingPromptWidget** (`gui.py`)
   - Extends: `QWidget`
   - Purpose: Combo of prompt dropdown + text input + counter

7. **NoScrollComboBox** (multiple files)
   - Extends: `QComboBox`
   - Purpose: Prevents scroll wheel changes

---

## Styling Application Points

### Current Styling Methods

1. **Inline `setStyleSheet()`** - Most common, scattered throughout
2. **Style functions** (`styles.py`):
   - `get_button_style(color)`
   - `get_combobox_style()`
   - `get_checkbox_style()`
   - `get_input_style()`
   - `get_scrollbar_style()`
3. **Color dictionaries**:
   - `COLORS` - Original dark theme (still used in some places)
   - `COMIC_COLORS` - Comic book theme
   - `COMIC_COLORS_FULL` - Extended comic palette

### Styling Challenges

**Current Issues**:
1. **Inconsistent color sources**: Some widgets use COLORS, some use COMIC_COLORS, some use custom palettes
2. **Dialog theming**: Settings and Scenario Editor don't match main app theme
3. **GroupedModelComboBox**: Custom delegate painting overrides stylesheets
4. **Dropdown menus**: `QAbstractItemView` / `QTreeView` inside combos need explicit styling

**What Works Well**:
- Main conversation UI (comic theme is cohesive)
- Portrait column (clean, functional highlighting)
- Message widgets (per-speaker colors work great)

**What Needs Work**:
- Settings dialog (mixing themes)
- Scenario editor (mixing themes)
- All dropdown menus (fighting custom delegate)
- Toggle button styling (inconsistent active states)

---

## Color Palette Reference

### Current Comic Theme (Main App)

**Defined in**: `styles.py` - `COMIC_COLORS` dict

```python
'cream': '#FAF6EE',         # Backgrounds
'black': '#000000',         # Borders, text
'red': '#E74E52',          # AI-1
'teal': '#17C0AA',         # AI-2
'gold': '#FFA630',         # AI-3
'purple': '#9B59B6',       # AI-4
'navy': '#34495E',         # AI-5
'white': '#FFFFFF',        # Cards, surfaces
'light_gray': '#ECF0F1',   # Subtle backgrounds
```

### Proposed Dialog Palette (from settings_dialog_palette.md)

```python
'bg_cream': '#FAF6EE',           # Dialog background
'bg_white': '#FFFFFF',           # Section cards
'bg_dark_navy': '#1A1A2E',       # Title/tab bar
'bg_input': '#2D3748',           # Input fields
'text_input': '#F0EDE8',         # Input text
'text_label': '#6B7280',         # Labels
'text_dark': '#4A5568',          # Body text
'text_muted': '#7A9A96',         # Inactive tabs
'teal_header': '#1A8A7D',        # Section headers
'teal_accent': '#22A394',        # Active state
'teal_border': '#3D8B84',        # Borders
'border_light': '#E8E0D4',       # Subtle borders
```

---

## File Locations Summary

### Core UI Files
- `gui.py` - Main app, conversation UI (~5000 lines)
- `styles.py` - Color definitions, style functions
- `portrait_column_widget.py` - Portrait column
- `settings_dialog.py` - Settings dialog (~700 lines)
- `scenario_editor_dialog.py` - Scenario editor (~600 lines)
- `grouped_model_selector.py` - Hierarchical combo box
- `thinking_bubble_widget.py` - Typing indicators

### Configuration
- `config.py` - AI_MODELS, SYSTEM_PROMPT_PAIRS, STARTING_PROMPTS
- `scenario_manager.py` - Scenario CRUD operations

### Supporting
- `main.py` - API workers, conversation orchestration
- `shared_utils.py` - Image generation, HTML export

---

## Design Planning Recommendations

### For Comprehensive Theming

1. **Create unified stylesheet** covering:
   - All Qt widget base styles
   - Hover states
   - Focus states
   - Disabled states
   - Selection states

2. **Handle custom widgets explicitly**:
   - GroupedModelComboBox: Pass color dict OR override delegate paint
   - Custom painted widgets: Update paint methods OR use stylesheet vars

3. **Test surfaces**:
   - Light backgrounds (cream/white)
   - Dark backgrounds (navy/charcoal)
   - Ensure text contrast meets WCAG AA

4. **Consider states**:
   - Default
   - Hover
   - Active/Selected
   - Disabled
   - Focus

5. **Dropdown menus specifically**:
   - QComboBox base widget
   - QComboBox::drop-down
   - QComboBox::down-arrow
   - QAbstractItemView (popup)
   - QTreeView (for hierarchical)
   - Selection highlighting
   - Hover highlighting

### Suggested Workflow

1. **Design phase** (claude.ai or design tool):
   - Create comprehensive color system
   - Map colors to Qt widget states
   - Generate complete stylesheet

2. **Implementation**:
   - Apply master stylesheet at app level
   - Override specific widgets as needed
   - Update custom delegates to use theme colors

3. **Testing**:
   - Visual inspection of all dialogs
   - Test all interactive states
   - Verify dropdown menus
   - Check focus indicators

---

## Questions to Answer in Design Phase

1. Should dialogs match comic theme or be distinct "backstage" aesthetic?
2. Dark inputs vs light inputs - which feels better?
3. Tab bar design - integrated or distinct?
4. Button hierarchy - how to distinguish primary/secondary/danger?
5. Dropdown styling - match input fields or distinct treatment?
6. List selection - subtle or bold highlighting?
7. Focus indicators - visible or minimal?
8. Disabled state - grayed or faded?

---

## Technical Constraints

### Qt Stylesheet Limitations
- Can't style delegate-painted items via stylesheet alone
- Must use delegates for complex custom rendering
- Stylesheet specificity can be tricky with nested widgets

### GroupedModelComboBox Special Handling
- Uses `QStyledItemDelegate` for custom painting
- Color dict passed to constructor
- Delegate expects these keys: `bg_dark`, `bg_medium`, `bg_light`, `text_bright`, `text_normal`, `accent_cyan`
- To theme: Either pass themed colors OR rewrite delegate

### Performance Considerations
- Large stylesheets can impact startup time
- Inline setStyleSheet on many widgets can be slow
- Consider master stylesheet + minimal overrides

---

**End of Specification**

*Generated: February 2026*
*For: Inference Lounge v0.7*
*Refactor Status: Unified Scenarios architecture complete*
