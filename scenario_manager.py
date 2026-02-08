"""
Scenario Manager - Business logic for managing conversation scenarios in config.py

Handles CRUDR operations (Create, Read, Update, Delete, Rename) for SYSTEM_PROMPT_PAIRS
in config.py with safe file operations and automatic backups.

New format (unified scenarios):
    SYSTEM_PROMPT_PAIRS = {
        "Scenario Name": {
            "default_prompt": "optional starting prompt text",
            "AI-1": {"prompt": "system prompt", "model": "model/id", "name": "Display Name"},
            "AI-2": {"prompt": "system prompt"},
            ...
        },
    }

AI slots are identified by the pattern AI-\d+. Everything else is scenario metadata.
"""

import os
import re
import ast
import shutil
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Pattern to identify AI slot keys (e.g. "AI-1", "AI-2", etc.)
AI_SLOT_PATTERN = re.compile(r'^AI-\d+$')

# Default model when none is specified in the scenario
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"


# =========================================================================
# Scenario data helpers — work on a single scenario's dict
# =========================================================================

def get_ai_slots(scenario_data: dict) -> List[str]:
    """Return sorted list of AI-N keys in a scenario (e.g. ['AI-1', 'AI-2'])."""
    return sorted(
        [k for k in scenario_data if AI_SLOT_PATTERN.match(k)],
        key=lambda s: int(s.split('-')[1])
    )


def get_num_ais(scenario_data: dict) -> int:
    """Return number of AI slots in a scenario."""
    return len(get_ai_slots(scenario_data))


def get_prompt(scenario_data: dict, ai_slot: str) -> str:
    """Return the system prompt for an AI slot. Handles both old and new format."""
    val = scenario_data.get(ai_slot, {})
    if isinstance(val, dict):
        return val.get("prompt", "")
    # Legacy fallback: value is a plain string
    return str(val)


def get_model(scenario_data: dict, ai_slot: str) -> Optional[str]:
    """Return the model ID for an AI slot, or None if not specified."""
    val = scenario_data.get(ai_slot, {})
    if isinstance(val, dict):
        return val.get("model")
    return None


def get_name(scenario_data: dict, ai_slot: str) -> str:
    """Return the custom display name for an AI slot, or the slot key as fallback."""
    val = scenario_data.get(ai_slot, {})
    if isinstance(val, dict):
        return val.get("name", ai_slot)
    return ai_slot


def get_default_prompt(scenario_data: dict) -> str:
    """Return the default starting prompt for a scenario, or empty string."""
    return scenario_data.get("default_prompt", "")


class ScenarioValidationError(Exception):
    """Raised when scenario validation fails."""
    pass


class ScenarioManager:
    """Manages reading and writing scenario configurations."""

    CONFIG_PATH = "config.py"

    @classmethod
    def load_scenarios(cls) -> Dict[str, Dict[str, Any]]:
        """
        Load SYSTEM_PROMPT_PAIRS from config.py using AST parsing.

        Returns:
            Dict mapping scenario names to their config dictionaries

        Raises:
            FileNotFoundError: If config.py doesn't exist
            ValueError: If SYSTEM_PROMPT_PAIRS can't be parsed
        """
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"{cls.CONFIG_PATH} not found")

        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file as AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"config.py has syntax errors: {e}")

        # Find the SYSTEM_PROMPT_PAIRS assignment
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "SYSTEM_PROMPT_PAIRS":
                        # Extract the dictionary literal from the AST node
                        start_line = node.value.lineno
                        end_line = node.value.end_lineno
                        start_col = node.value.col_offset
                        end_col = node.value.end_col_offset

                        # Extract those lines
                        lines = content.split('\n')
                        if start_line == end_line:
                            dict_text = lines[start_line - 1][start_col:end_col]
                        else:
                            dict_lines = []
                            for line_num in range(start_line, end_line + 1):
                                line = lines[line_num - 1]
                                if line_num == start_line:
                                    dict_lines.append(line[start_col:])
                                elif line_num == end_line:
                                    dict_lines.append(line[:end_col])
                                else:
                                    dict_lines.append(line)
                            dict_text = '\n'.join(dict_lines)

                        # Parse the dictionary literal
                        try:
                            scenarios = ast.literal_eval(dict_text)
                        except (SyntaxError, ValueError) as e:
                            raise ValueError(f"Failed to parse SYSTEM_PROMPT_PAIRS value: {e}")

                        if not isinstance(scenarios, dict):
                            raise ValueError("SYSTEM_PROMPT_PAIRS is not a dictionary")

                        return scenarios

        raise ValueError("SYSTEM_PROMPT_PAIRS not found in config.py")

    @classmethod
    def validate_scenario(cls, name: str, data: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate a scenario before saving.

        Args:
            name: Scenario name
            data: Scenario config dict (may contain AI slots + metadata keys)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check name is not empty
        if not name or not name.strip():
            return False, "Scenario name cannot be empty"

        # Check for problematic characters in name
        if '"' in name and "'" in name:
            return False, "Scenario name cannot contain both single and double quotes"

        if not isinstance(data, dict):
            return False, "Scenario data must be a dictionary"

        # Must have at least 2 AI slots
        slots = get_ai_slots(data)
        if len(slots) < 2:
            return False, f"Scenario must have at least 2 AI slots, found {len(slots)}"
        if len(slots) > 5:
            return False, f"Scenario can have at most 5 AI slots, found {len(slots)}"

        # Validate each AI slot
        for slot in slots:
            val = data[slot]
            if isinstance(val, dict):
                if "prompt" not in val:
                    return False, f"{slot} must have a 'prompt' key"
                if not isinstance(val["prompt"], str):
                    return False, f"{slot} prompt must be a string"
                # model and name are optional strings
                if "model" in val and not isinstance(val["model"], str):
                    return False, f"{slot} model must be a string"
                if "name" in val and not isinstance(val["name"], str):
                    return False, f"{slot} name must be a string"
            elif isinstance(val, str):
                # Legacy format — plain string prompt, still valid
                pass
            else:
                return False, f"{slot} must be a dict or string, got {type(val).__name__}"

        return True, None

    @classmethod
    def validate_all_scenarios(cls, scenarios: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate all scenarios in a collection.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not scenarios:
            return False, "Must have at least one scenario"

        # Check for duplicate names (case-sensitive check)
        names = list(scenarios.keys())
        if len(names) != len(set(names)):
            return False, "Duplicate scenario names found"

        # Validate each scenario
        for name, data in scenarios.items():
            is_valid, error = cls.validate_scenario(name, data)
            if not is_valid:
                return False, f"Scenario '{name}': {error}"

        return True, None

    @classmethod
    def create_backup(cls) -> str:
        """
        Create a timestamped backup of config.py.

        Returns:
            Path to the backup file
        """
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"{cls.CONFIG_PATH} not found")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = f"{cls.CONFIG_PATH}.backup-{timestamp}"

        shutil.copy2(cls.CONFIG_PATH, backup_path)
        return backup_path

    @classmethod
    def generate_config_content(cls, scenarios: dict) -> str:
        """
        Generate new config.py content with updated scenarios.

        Uses a template approach: reads the original config.py,
        replaces only the SYSTEM_PROMPT_PAIRS section, and preserves
        everything else.
        """
        # Read original config
        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Use AST to find where SYSTEM_PROMPT_PAIRS ends
        try:
            tree = ast.parse(original_content)
        except SyntaxError as e:
            raise ValueError(f"config.py has syntax errors: {e}")

        # Find the SYSTEM_PROMPT_PAIRS assignment in the AST
        start_idx = None
        end_idx = None

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "SYSTEM_PROMPT_PAIRS":
                        start_line = target.lineno
                        end_line = node.end_lineno

                        lines = original_content.split('\n')
                        start_idx = sum(len(line) + 1 for line in lines[:start_line-1])
                        end_idx = sum(len(line) + 1 for line in lines[:end_line])
                        break

        if start_idx is None or end_idx is None:
            raise ValueError("Could not locate SYSTEM_PROMPT_PAIRS in config.py")

        # Generate new SYSTEM_PROMPT_PAIRS content
        output_lines = ["SYSTEM_PROMPT_PAIRS = {"]

        sorted_scenarios = sorted(scenarios.items())

        for s_idx, (scenario_name, data) in enumerate(sorted_scenarios):
            # Determine quote style for scenario name
            if '"' in scenario_name:
                name_quote = "'"
            else:
                name_quote = '"'

            output_lines.append(f'    {name_quote}{scenario_name}{name_quote}: {{')

            # Write metadata keys first (like default_prompt)
            if "default_prompt" in data and data["default_prompt"]:
                dp = data["default_prompt"].replace('\\', '\\\\').replace('"""', '\\"""')
                output_lines.append(f'        "default_prompt": """{dp}""",')
                output_lines.append("        ")

            # Write AI slots
            slots = get_ai_slots(data)
            for slot_idx, slot in enumerate(slots):
                val = data[slot]

                if isinstance(val, dict):
                    # New format: dict with prompt, optional model & name
                    prompt_text = val.get("prompt", "")
                    escaped_prompt = prompt_text.replace('\\', '\\\\').replace('"""', '\\"""')

                    output_lines.append(f'        "{slot}": {{')
                    output_lines.append(f'            "prompt": """{escaped_prompt}""",')

                    if val.get("model"):
                        output_lines.append(f'            "model": "{val["model"]}",')

                    if val.get("name"):
                        # Escape the name for safe Python string
                        name_escaped = val["name"].replace('\\', '\\\\').replace('"', '\\"')
                        output_lines.append(f'            "name": "{name_escaped}",')

                    output_lines.append('        },')
                else:
                    # Legacy format: plain string — convert to new format on save
                    prompt_text = str(val)
                    escaped_prompt = prompt_text.replace('\\', '\\\\').replace('"""', '\\"""')
                    output_lines.append(f'        "{slot}": {{')
                    output_lines.append(f'            "prompt": """{escaped_prompt}""",')
                    output_lines.append('        },')

                # Blank line between AI slots (not after last)
                if slot_idx < len(slots) - 1:
                    output_lines.append("        ")

            # Close scenario dict
            if s_idx < len(sorted_scenarios) - 1:
                output_lines.append("    },")
                output_lines.append("    ")
            else:
                output_lines.append("    }")

        output_lines.append("}")

        new_dict_content = "\n".join(output_lines)

        # Construct final content: before + new dict + after
        before = original_content[:start_idx]
        after = original_content[end_idx:]

        return before + new_dict_content + "\n" + after

    @classmethod
    def save_scenarios(cls, scenarios: dict, create_backup: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Save scenarios to config.py with validation and atomic write.

        Returns:
            Tuple of (success, error_message)
        """
        # Validate all scenarios first
        is_valid, error = cls.validate_all_scenarios(scenarios)
        if not is_valid:
            return False, error

        try:
            # Create backup if requested
            if create_backup:
                backup_path = cls.create_backup()

            # Generate new content
            new_content = cls.generate_config_content(scenarios)

            # Validate the generated content is valid Python
            try:
                ast.parse(new_content)
            except SyntaxError as e:
                return False, f"Generated config has invalid Python syntax: {e}"

            # Atomic write: write to temp file first
            temp_path = f"{cls.CONFIG_PATH}.tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Verify temp file can be parsed
            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
            except Exception as e:
                os.remove(temp_path)
                return False, f"Failed to validate temp config: {e}"

            # Replace original with temp file
            os.replace(temp_path, cls.CONFIG_PATH)

            backup_msg = f" (backup: {backup_path})" if create_backup else ""
            return True, f"Scenarios saved successfully{backup_msg}"

        except Exception as e:
            return False, f"Failed to save scenarios: {str(e)}"

    @classmethod
    def get_scenario_names(cls) -> List[str]:
        """Get sorted list of all scenario names."""
        try:
            scenarios = cls.load_scenarios()
            return sorted(scenarios.keys())
        except Exception:
            return []


class StartingPromptManager:
    """Manages CRUD operations for starting prompts in config.py"""

    CONFIG_PATH = "config.py"

    @classmethod
    def load_prompts(cls) -> Dict[str, str]:
        """
        Load STARTING_PROMPTS from config.py using AST parsing.

        Returns:
            Dict mapping prompt names to prompt text

        Raises:
            FileNotFoundError: If config.py doesn't exist
            ValueError: If STARTING_PROMPTS can't be parsed
        """
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"{cls.CONFIG_PATH} not found")

        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file as AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"config.py has syntax errors: {e}")

        # Find the STARTING_PROMPTS assignment
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "STARTING_PROMPTS":
                        # Extract the dictionary literal
                        start_line = node.value.lineno
                        end_line = node.value.end_lineno
                        start_col = node.value.col_offset
                        end_col = node.value.end_col_offset

                        # Extract those lines
                        lines = content.split('\n')
                        if start_line == end_line:
                            dict_text = lines[start_line - 1][start_col:end_col]
                        else:
                            dict_lines = []
                            for line_num in range(start_line, end_line + 1):
                                line = lines[line_num - 1]
                                if line_num == start_line:
                                    dict_lines.append(line[start_col:])
                                elif line_num == end_line:
                                    dict_lines.append(line[:end_col])
                                else:
                                    dict_lines.append(line)
                            dict_text = '\n'.join(dict_lines)

                        # Parse the dictionary literal
                        try:
                            prompts = ast.literal_eval(dict_text)
                        except (SyntaxError, ValueError) as e:
                            raise ValueError(f"Failed to parse STARTING_PROMPTS value: {e}")

                        if not isinstance(prompts, dict):
                            raise ValueError("STARTING_PROMPTS is not a dictionary")

                        return prompts

        raise ValueError("STARTING_PROMPTS not found in config.py")

    @classmethod
    def create_backup(cls) -> str:
        """
        Create a timestamped backup of config.py.

        Returns:
            Path to the backup file
        """
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"{cls.CONFIG_PATH} not found")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = f"{cls.CONFIG_PATH}.backup-{timestamp}"

        shutil.copy2(cls.CONFIG_PATH, backup_path)
        return backup_path

    @classmethod
    def generate_config_content(cls, prompts: Dict[str, str]) -> str:
        """
        Generate new config.py content with updated starting prompts.

        Args:
            prompts: Dictionary of starting prompts to write

        Returns:
            Complete config.py content as a string
        """
        # Read original config
        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Use AST to find where STARTING_PROMPTS is
        try:
            tree = ast.parse(original_content)
        except SyntaxError as e:
            raise ValueError(f"config.py has syntax errors: {e}")

        # Find the STARTING_PROMPTS assignment
        start_idx = None
        end_idx = None

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "STARTING_PROMPTS":
                        start_line = target.lineno
                        end_line = node.end_lineno

                        # Convert line numbers to character positions
                        lines = original_content.split('\n')

                        # Start at beginning of assignment line
                        start_idx = sum(len(line) + 1 for line in lines[:start_line-1])

                        # End at end of last line
                        end_idx = sum(len(line) + 1 for line in lines[:end_line])

                        break

        if start_idx is None or end_idx is None:
            raise ValueError("Could not locate STARTING_PROMPTS in config.py")

        # Generate new STARTING_PROMPTS content
        lines = ["# Starting prompts for conversations"]
        lines.append("STARTING_PROMPTS = {")

        # Sort prompts by name for consistent ordering
        sorted_prompts = sorted(prompts.items())

        for idx, (name, text) in enumerate(sorted_prompts):
            # Determine quote style for name
            if '"' in name:
                name_quote = "'"
            else:
                name_quote = '"'

            # Escape the text for Python string literal
            # Use double quotes for text values
            escaped_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

            comma = "," if idx < len(sorted_prompts) - 1 else ""
            lines.append(f'    {name_quote}{name}{name_quote}: "{escaped_text}"{comma}')

        lines.append("}")

        new_dict_content = "\n".join(lines)

        # Construct final content
        before = original_content[:start_idx]
        after = original_content[end_idx:]

        return before + new_dict_content + after

    @classmethod
    def save_prompts(cls, prompts: Dict[str, str], create_backup: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Save starting prompts to config.py with validation and atomic write.

        Args:
            prompts: Dictionary of prompts to save
            create_backup: Whether to create a backup before saving

        Returns:
            Tuple of (success, error_message)
        """
        # Validate prompts
        if not prompts:
            return False, "Must have at least one starting prompt"

        for name, text in prompts.items():
            if not name or not name.strip():
                return False, "Prompt name cannot be empty"
            if not isinstance(text, str):
                return False, f"Prompt text for '{name}' must be a string"

        try:
            # Create backup if requested
            if create_backup:
                backup_path = cls.create_backup()

            # Generate new content
            new_content = cls.generate_config_content(prompts)

            # Validate the generated content is valid Python
            try:
                ast.parse(new_content)
            except SyntaxError as e:
                return False, f"Generated config has invalid Python syntax: {e}"

            # Atomic write: write to temp file first
            temp_path = f"{cls.CONFIG_PATH}.tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Verify temp file can be parsed
            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
            except Exception as e:
                os.remove(temp_path)
                return False, f"Failed to validate temp config: {e}"

            # Replace original with temp file
            os.replace(temp_path, cls.CONFIG_PATH)

            backup_msg = f" (backup: {backup_path})" if create_backup else ""
            return True, f"Starting prompts saved successfully{backup_msg}"

        except Exception as e:
            return False, f"Failed to save starting prompts: {str(e)}"

    @classmethod
    def add_prompt(cls, name: str, text: str) -> Tuple[bool, Optional[str]]:
        """Add a new starting prompt."""
        try:
            prompts = cls.load_prompts()
            if name in prompts:
                return False, f"Prompt '{name}' already exists"
            prompts[name] = text
            return cls.save_prompts(prompts)
        except Exception as e:
            return False, str(e)

    @classmethod
    def delete_prompt(cls, name: str) -> Tuple[bool, Optional[str]]:
        """Delete a starting prompt."""
        try:
            prompts = cls.load_prompts()
            if name not in prompts:
                return False, f"Prompt '{name}' not found"
            del prompts[name]
            return cls.save_prompts(prompts)
        except Exception as e:
            return False, str(e)

    @classmethod
    def rename_prompt(cls, old_name: str, new_name: str) -> Tuple[bool, Optional[str]]:
        """Rename a starting prompt."""
        try:
            prompts = cls.load_prompts()
            if old_name not in prompts:
                return False, f"Prompt '{old_name}' not found"
            if new_name in prompts and new_name != old_name:
                return False, f"Prompt '{new_name}' already exists"

            # Preserve order by rebuilding dict
            new_prompts = {}
            for k, v in prompts.items():
                if k == old_name:
                    new_prompts[new_name] = v
                else:
                    new_prompts[k] = v

            return cls.save_prompts(new_prompts)
        except Exception as e:
            return False, str(e)
