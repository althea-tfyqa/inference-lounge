# Inference Lounge 🛋️

A Python-based application that enables dynamic conversations between multiple AI models in a graphical user interface. Originally forked from [Liminal Backrooms](https://github.com/liminalbardo/liminal_backrooms), enhanced with a scenario editor and quality-of-life improvements.

> **Attribution**: This is a fork of the excellent [Liminal Backrooms](https://github.com/liminalbardo/liminal_backrooms) by LiminalBackrooms. See [ATTRIBUTION.md](ATTRIBUTION.md) for full details.

## What's New in Inference Lounge

### ✨ New Features
- **📝 Scenario Editor** - Create, edit, rename, and delete conversation scenarios through a GUI
  - Visual editor with 5 AI prompt fields
  - Automatic timestamped backups before saves
  - Handles complex prompts with quotes, newlines, special characters
  - Purple "Edit Scenarios" button in control panel
  - No need to manually edit config.py anymore!

### 🐛 Bug Fixes
- Made OpenAI API key optional (only needed for Sora video generation)
- Fixed PyQt6 installation issues on macOS

## What It Does

All the original Liminal Backrooms features, plus easier scenario management:

- **Dynamic AI Participants**: Models can invite other AIs into the conversation using `!add_ai` (up to 5 participants)
- **AI-Generated Images**: Models create their own images using Gemini 3 Pro Image Preview via `!image` command
- **AI-Generated Videos**: Sora 2 video generation via `!video` command (currently disabled in scenarios - expensive!)
- **Self-Muting**: Some scenarios include `!mute_self` so AIs can sit out a turn and just listen
- **AI Self-Modification**: Models can modify their own system prompts (`!prompt`) and adjust their temperature (`!temperature`)
- **Web Search**: Models can search the internet for up-to-date information (`!search`)
- **BackroomsBench Evaluation (Beta)**: Multi-judge LLM evaluation system
- **Better HTML Export**: Styled dark theme output for sharing conversations

## Included Scenarios

Fresh scenario prompts written by Claude Opus 4.5:
- WhatsApp group chat energy
- Anthropic Slack #random
- Museum of Cursed Objects
- Conspiracy Theory chat
- Dystopian Ad Agency
- Dark fantasy D&D campaigns
- And the original Backrooms exploration

**Plus**: Now you can create your own scenarios without editing Python code!

## How It Works

All LLMs run through **OpenRouter**. For Sora video generation, you'll need an **OpenAI API key** (optional).

## Features

- Multi-model AI conversations with support for:
  - Claude (Anthropic) - all versions
  - GPT (OpenAI)
  - Grok (xAI)
  - Gemini (Google)
  - DeepSeek R1
  - Kimi K2
  - Anything on OpenRouter

- AI Agent Commands:
  - `!add_ai "Model Name" "persona"` - invite another AI to the conversation (max 5)
  - `!image "description"` - generate an image (Gemini 3 Pro)
  - `!video "description"` - generate a video (Sora 2) [currently disabled in scenarios]
  - `!search "query"` - search the web for up-to-date information
  - `!prompt "text"` - modify your own system prompt (persists across turns)
  - `!temperature X` - adjust your own sampling temperature (0-2, default 1.0)
  - `!mute_self` - sit out a turn and just listen

- Advanced Features:
  - **Scenario Editor GUI** - Create and manage scenarios visually
  - Chain of Thought reasoning display (optional)
  - Customizable conversation turns and modes (AI-AI or Human-AI)
  - Export functionality for conversations and generated images
  - Modern dark-themed GUI interface
  - Conversation memory system
  - AI self-modification (system prompt and temperature control)
  - Web search integration for real-time information
  - BackroomsBench evaluation system (beta) with multi-judge LLM scoring

## Prerequisites

- Python 3.10 or higher (but lower than 3.12)
- Poetry for dependency management
- macOS, Windows 10/11, or Linux (tested on Ubuntu 20.04+)

## API Keys Required

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key    # Required - all LLMs route through here
OPENAI_API_KEY=your_openai_api_key            # Optional - only needed for Sora video generation
```

Get your keys:
- OpenRouter: https://openrouter.ai/
- OpenAI (for Sora): https://platform.openai.com/

## Installation

1. Clone the repository:

```bash
git clone [your-repository-url]
cd inference-lounge
```

2. Install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:

```bash
poetry install
```

4. Create your `.env` file with API keys (see above)

## Usage

1. Start the application:

```bash
poetry run python main.py
```

2. GUI Controls:
   - **Mode Selection**: Choose between AI-AI conversation or Human-AI interaction
   - **Iterations**: Set number of conversation turns (1-100)
   - **AI Model Selection**: Choose models for each AI slot
   - **Prompt Style**: Select from predefined scenarios
   - **Edit Scenarios** 🆕: Click the purple button to create/edit scenarios
   - **Input Field**: Enter your message or initial prompt
   - **Export**: Save conversation and generated images
   - **View HTML**: Open styled conversation in browser
   - **BackroomsBench (beta)**: Run multi-judge evaluation on conversations

3. The AIs take it from there - they can add each other, generate images, and go wherever the scenario takes them.

## Using the Scenario Editor 🆕

1. Click the purple **"Edit Scenarios"** button in the control panel
2. Select a scenario from the list or click **"New Scenario"**
3. Edit the scenario name and 5 AI prompts
4. Click **"Save All Changes"** - a timestamped backup is created automatically
5. Restart the app to use your new scenarios

**Features**:
- Creates backups before every save: `config.py.backup-YYYYMMDD-HHMMSS`
- Handles multi-line prompts, quotes, and special characters
- Validates scenario structure before saving
- Rename and delete existing scenarios

## Configuration

Application settings in `config.py`:
- Runtime settings (turn delay, etc.)
- Available AI models in `AI_MODELS` dictionary
- Scenario prompts in `SYSTEM_PROMPT_PAIRS` dictionary (or use the GUI editor!)

### Developer Tools

For debugging the GUI, set `DEVELOPER_TOOLS = True` in `config.py`. This enables:
- **F12**: Toggle debug inspector panel
- **Ctrl+Shift+C**: Pick and inspect any UI element

Keep this `False` for normal usage.

### Adding New Models

Add entries to `AI_MODELS` in config.py:

```python
"Model Display Name": "openrouter/model-id",
```

### Creating Custom Scenarios

**Easy way**: Use the scenario editor GUI (click "Edit Scenarios")

**Manual way**: Add entries to `SYSTEM_PROMPT_PAIRS` in config.py. Each scenario needs prompts for AI-1 through AI-5.

## Sora 2 Video Generation

To enable video generation:

1. Set one AI slot to `Sora 2` or `Sora 2 Pro`
2. Or add `!video` commands to your scenario prompts
3. Videos save to `videos/` folder

Environment variables (optional):

```env
SORA_SECONDS=12        # clip duration (4, 8, 10, 12)
SORA_SIZE=1280x720     # resolution
```

**Note**: Video generation is expensive. The `!video` command has been removed from default scenarios but is easy to add back.

## Troubleshooting

1. **API Issues**:
   - Check API key validity in `.env`
   - Verify you have credits on OpenRouter
   - Check console for error messages

2. **GUI Issues**:
   - Ensure PyQt6 is installed (handled by Poetry install)
   - Check Python version compatibility
   - Try: `poetry remove PyQt6 && poetry add PyQt6`

3. **Empty Responses**:
   - Some models occasionally return empty - the app will retry once automatically
   - Check OpenRouter status if persistent

4. **Scenario Editor Issues**:
   - Backups are created automatically in the project root
   - If save fails, restore from `config.py.backup-YYYYMMDD-HHMMSS`
   - Restart app after saving scenarios

## Contributing

Contributions are welcome! Please:

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

## Credits

- **Original Project**: [Liminal Backrooms](https://github.com/liminalbardo/liminal_backrooms) by LiminalBackrooms
- **Scenario Editor**: Added in Inference Lounge fork (February 2026)
- See [ATTRIBUTION.md](ATTRIBUTION.md) for full details

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Enjoy your AI conversations in the Inference Lounge!** 🛋️✨
