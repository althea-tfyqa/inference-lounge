# Attribution

**Inference Lounge** is a fork of [Liminal Backrooms](https://github.com/liminalbardo/liminal_backrooms) by LiminalBackrooms.

## Original Project

- **Original Repository**: https://github.com/liminalbardo/liminal_backrooms
- **Original Author**: LiminalBackrooms
- **Original License**: MIT License (see LICENSE file)

## What Was Changed

This fork includes the following modifications and enhancements:

### New Features Added
- **Scenario Editor** (February 2026) - Full CRUDR interface for managing conversation scenarios
  - Create, edit, rename, and delete scenarios through GUI
  - Automatic timestamped backups
  - Multi-line prompt editors with syntax handling
  - Integrated into control panel with purple "Edit Scenarios" button
  - Files: `scenario_manager.py`, `scenario_editor_dialog.py`

### Bug Fixes
- Made OpenAI API key optional (was causing crashes when not present)
- Fixed PyQt6 framework initialization issues

### Branding Changes
- Renamed to "Inference Lounge"
- Updated UI text and branding
- Maintained all original functionality

## Acknowledgments

Thank you to LiminalBackrooms for creating the original multi-AI conversation platform. The core architecture, agentic commands system, and creative scenarios are all from the original project.

## License

This fork maintains the original MIT License. See the LICENSE file for full details.
