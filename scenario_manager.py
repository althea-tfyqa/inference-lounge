"""
Scenario Manager - Business logic for managing conversation scenarios in config.py

Handles CRUDR operations (Create, Read, Update, Delete, Rename) for SYSTEM_PROMPT_PAIRS
in config.py with safe file operations and automatic backups.
"""

import os
import ast
import shutil
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class ScenarioValidationError(Exception):
    """Raised when scenario validation fails."""
    pass


class ScenarioManager:
    """Manages reading and writing scenario configurations."""

    CONFIG_PATH = "config.py"

    # Required AI slots for each scenario
    REQUIRED_SLOTS = ["AI-1", "AI-2", "AI-3", "AI-4", "AI-5"]

    @classmethod
    def load_scenarios(cls) -> Dict[str, Dict[str, str]]:
        """
        Load SYSTEM_PROMPT_PAIRS from config.py using AST parsing.

        Returns:
            Dict mapping scenario names to their AI prompt dictionaries

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
                        # Get the text of just the value part
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
    def validate_scenario(cls, name: str, prompts: Dict[str, str]) -> Tuple[bool, Optional[str]]:
        """
        Validate a scenario before saving.

        Args:
            name: Scenario name
            prompts: Dictionary mapping AI slot names to prompt text

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check name is not empty
        if not name or not name.strip():
            return False, "Scenario name cannot be empty"

        # Check for problematic characters in name
        if '"' in name and "'" in name:
            return False, "Scenario name cannot contain both single and double quotes"

        # Check all required slots are present
        if not isinstance(prompts, dict):
            return False, "Prompts must be a dictionary"

        missing_slots = [slot for slot in cls.REQUIRED_SLOTS if slot not in prompts]
        if missing_slots:
            return False, f"Missing required AI slots: {', '.join(missing_slots)}"

        # Check all values are strings
        for slot, prompt in prompts.items():
            if not isinstance(prompt, str):
                return False, f"Prompt for {slot} must be a string, got {type(prompt).__name__}"

        return True, None

    @classmethod
    def validate_all_scenarios(cls, scenarios: Dict[str, Dict[str, str]]) -> Tuple[bool, Optional[str]]:
        """
        Validate all scenarios in a collection.

        Args:
            scenarios: Dictionary of all scenarios

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
        for name, prompts in scenarios.items():
            is_valid, error = cls.validate_scenario(name, prompts)
            if not is_valid:
                return False, f"Scenario '{name}': {error}"

        return True, None

    @classmethod
    def create_backup(cls) -> str:
        """
        Create a timestamped backup of config.py.

        Returns:
            Path to the backup file

        Raises:
            FileNotFoundError: If config.py doesn't exist
        """
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(f"{cls.CONFIG_PATH} not found")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = f"{cls.CONFIG_PATH}.backup-{timestamp}"

        shutil.copy2(cls.CONFIG_PATH, backup_path)
        return backup_path

    @classmethod
    def generate_config_content(cls, scenarios: Dict[str, Dict[str, str]]) -> str:
        """
        Generate new config.py content with updated scenarios.

        This uses a template approach: reads the original config.py,
        replaces only the SYSTEM_PROMPT_PAIRS section, and preserves
        everything else.

        Args:
            scenarios: Dictionary of scenarios to write

        Returns:
            Complete config.py content as a string
        """
        # Read original config
        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Use AST to find where SYSTEM_PROMPT_PAIRS ends
        # This is more reliable than manual parsing
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
                        # Found it! Get line and column info
                        start_line = target.lineno
                        end_line = node.end_lineno

                        # Convert line numbers to character positions
                        lines = original_content.split('\n')

                        # Start is at the beginning of the assignment line
                        start_idx = sum(len(line) + 1 for line in lines[:start_line-1])

                        # End is at the end of the last line of the assignment
                        end_idx = sum(len(line) + 1 for line in lines[:end_line])

                        break

        if start_idx is None or end_idx is None:
            raise ValueError("Could not locate SYSTEM_PROMPT_PAIRS in config.py")

        # Generate new SYSTEM_PROMPT_PAIRS content
        lines = ["SYSTEM_PROMPT_PAIRS = {"]
        lines.append("    # this is a basic system prompt for a conversation between two AIs. Experiment with different prompts to see how they affect the conversation. Add new prompts to the library to use them in the GUI.")
        lines.append("    ")

        # Sort scenarios by name for consistent ordering
        sorted_scenarios = sorted(scenarios.items())

        for idx, (scenario_name, prompts) in enumerate(sorted_scenarios):
            # Determine quote style for scenario name
            if '"' in scenario_name:
                name_quote = "'"
            else:
                name_quote = '"'

            lines.append(f'    {name_quote}{scenario_name}{name_quote}: {{')

            # Write each AI slot
            for slot in cls.REQUIRED_SLOTS:
                prompt_text = prompts.get(slot, "")

                # For triple-quoted strings, we need to handle:
                # 1. Backslashes (\ -> \\)
                # 2. Triple quotes (""" -> \"\"\")
                # 3. String ending with " (would create """" at the end)

                escaped_prompt = prompt_text.replace('\\', '\\\\').replace('"""', '\\"""')

                # If string ends with one or two quotes, escape the last one
                # to prevent creating """ " or """" at the end
                if escaped_prompt.endswith('"'):
                    escaped_prompt = escaped_prompt[:-1] + '\\"'
                elif escaped_prompt.endswith('""'):
                    escaped_prompt = escaped_prompt[:-2] + '"\\"'

                lines.append(f'        "{slot}": """{escaped_prompt}""",')

                # Add blank line after each AI except the last
                if slot != cls.REQUIRED_SLOTS[-1]:
                    lines.append("        ")

            # Close scenario dict
            if idx < len(sorted_scenarios) - 1:
                lines.append("    },")
                lines.append("    ")
            else:
                lines.append("    }")

        lines.append("}")

        new_dict_content = "\n".join(lines)

        # Construct final content: before + new dict + after
        before = original_content[:start_idx]
        after = original_content[end_idx:]

        return before + new_dict_content + after

    @classmethod
    def save_scenarios(cls, scenarios: Dict[str, Dict[str, str]], create_backup: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Save scenarios to config.py with validation and atomic write.

        Args:
            scenarios: Dictionary of scenarios to save
            create_backup: Whether to create a backup before saving

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
        """
        Get list of all scenario names.

        Returns:
            List of scenario names, sorted alphabetically
        """
        try:
            scenarios = cls.load_scenarios()
            return sorted(scenarios.keys())
        except Exception:
            return []
