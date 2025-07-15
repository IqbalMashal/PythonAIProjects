# OpenAI Python Chat

A simple command-line chat interface for OpenAI's GPT models with history tracking and enhanced user experience.

## Features

- 🤖 Chat with OpenAI's GPT-4o-mini model
- 📚 Persistent chat history with timestamps
- 🔍 Command history with auto-suggestions
- 🎨 Colored console output for better readability
- 🔄 Automatic retry mechanism for API calls
- 💾 Local storage of conversations in JSON format

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd openaiwithpython
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Create a `.env` file in the project root:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual OpenAI API key.

## Usage

Run the chat application:
```bash
uv run python main.py
```

### Available Commands

- Type any question to chat with the AI
- `history` - View your previous conversations
- `exit` - Quit the application

### Features in Action

- **Auto-suggestions**: The prompt will suggest previous questions as you type
- **Persistent history**: All conversations are saved to `chat_history.json`
- **Colored output**: Different colors for questions, answers, and system messages
- **Error handling**: Automatic retries for API failures

## Project Structure

```
openaiwithpython/
├── main.py              # Main application file
├── chat_history.json    # Chat history storage (auto-generated)
├── prompt_history.txt   # Command history (auto-generated)
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Configuration

The application uses these environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Dependencies

- `openai==0.28` - OpenAI API client
- `prompt-toolkit>=3.0.0` - Enhanced command-line interface
- `colorama>=0.4.6` - Colored console output
- `python-dotenv>=1.0.0` - Environment variable loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

**prompt-toolkit not working**: Try running in a different terminal or check if your terminal supports the required features.

**API errors**: Ensure your OpenAI API key is valid and has sufficient credits.

**Permission errors**: Make sure the application has write permissions for creating history files.

### Getting Help

If you encounter issues:
1. Check that your `.env` file contains a valid OpenAI API key
2. Ensure you're using a compatible terminal
3. Try reinstalling dependencies with `uv sync --reinstall`

## Acknowledgments

- OpenAI for providing the GPT API
- The prompt-toolkit team for the excellent CLI framework
- The uv team for the fast Python package manager