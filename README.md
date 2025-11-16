# Claude Prompt Enhancer

A production-ready command-line tool that transforms basic prompts into well-structured, detailed instructions optimized for Claude AI models while respecting specified token limits.

## Features

- **Intelligent Enhancement**: Uses Claude API to enhance prompts following best practices
- **Token Management**: Strict adherence to token limits with automatic compression
- **Multiple Modes**: Interactive, file-based, dry-run, and comparison modes
- **Model Support**: Compatible with all Claude models (Opus, Sonnet, Haiku)
- **Smart Compression**: Automatically compresses prompts when approaching limits
- **Comprehensive Validation**: Input validation, error handling, and quality checks
- **Colored Output**: Beautiful terminal output with progress indicators
- **Logging**: Detailed logging for debugging and monitoring

## Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Claude-Code-Enhance-Prompt-For-Any-Token-Limit.git
   cd Claude-Code-Enhance-Prompt-For-Any-Token-Limit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

   Alternatively, set the environment variable directly:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

## Usage

### Interactive Mode

Enter your prompt directly and receive the enhanced version:

```bash
python claude_prompt_enhancer.py -t 2000
```

Then paste your prompt and press `Ctrl+D` (Unix) or `Ctrl+Z` (Windows) when done.

### File Mode

Process prompts from files:

```bash
# Read from file, display result
python claude_prompt_enhancer.py -i input.txt -t 2000

# Read from file, save to output file
python claude_prompt_enhancer.py -i input.txt -o enhanced.txt -t 2000
```

### Dry Run Mode

Preview what would be done without making API calls:

```bash
python claude_prompt_enhancer.py -i input.txt -t 2000 --dry-run
```

### Comparison Mode

View original and enhanced prompts side-by-side:

```bash
python claude_prompt_enhancer.py -i input.txt -t 2000 --compare
```

### Verbose Mode

Enable detailed logging and debug information:

```bash
python claude_prompt_enhancer.py -i input.txt -t 2000 -v
```

### Specify Target Model

Optimize for a specific Claude model:

```bash
python claude_prompt_enhancer.py -i input.txt -t 2000 -m sonnet-4.5
```

Available models:
- `opus-4.1` (default) - Claude Opus 4
- `sonnet-4.5` - Claude Sonnet 4.5
- `sonnet-3.5` - Claude Sonnet 3.5
- `haiku-3.5` - Claude Haiku 3.5

## Command-Line Options

```
usage: claude_prompt_enhancer.py [-h] [-i INPUT] [-o OUTPUT] -t TOKEN_LIMIT
                                  [-m {opus-4.1,sonnet-4.5,sonnet-3.5,haiku-3.5}]
                                  [--dry-run] [--compare] [-v] [--api-key API_KEY]

Options:
  -h, --help            Show help message and exit
  -i, --input INPUT     Input file containing the prompt to enhance
  -o, --output OUTPUT   Output file for the enhanced prompt
  -t, --token-limit TOKEN_LIMIT
                        Maximum token limit for the enhanced prompt (required)
  -m, --target-model {opus-4.1,sonnet-4.5,sonnet-3.5,haiku-3.5}
                        Target Claude model (default: opus-4.1)
  --dry-run             Show what would be done without making API calls
  --compare             Show side-by-side comparison of prompts
  -v, --verbose         Enable verbose output for debugging
  --api-key API_KEY     Anthropic API key (overrides environment variable)
```

## Enhancement Strategy

The tool enhances prompts using the following strategies:

### 1. Structure & Clarity
- Breaks complex requests into logical sections
- Adds clear headings and organization
- Numbers steps when sequence matters

### 2. Output Specifications
- Defines desired length, format, and structure
- Specifies tone and style
- Sets quality expectations

### 3. Context & Background
- Adds relevant domain context
- Specifies intended audience
- Clarifies task purpose and goals

### 4. Examples
- Provides concrete examples of desired output
- Shows input/output patterns
- Illustrates edge cases

### 5. Constraints & Requirements
- Makes implicit constraints explicit
- Defines boundaries and limitations
- Specifies what to avoid

### 6. Role-Based Framing
- Assigns relevant expertise
- Defines perspective or viewpoint
- Sets appropriate knowledge level

### 7. Reasoning Guidance
- Requests step-by-step analysis
- Asks for multiple perspectives
- Specifies decision-making criteria

### 8. Ambiguity Elimination
- Replaces vague terms with precise language
- Clarifies multiple interpretations
- Defines domain-specific terminology

## Token Management

The tool implements intelligent token management:

- **5% Safety Margin**: Always stays 5% below the specified limit
- **Adaptive Enhancement**: Adjusts enhancement depth based on available budget
- **Automatic Compression**: Compresses prompts that exceed limits
- **Accurate Counting**: Uses tiktoken for precise token estimation
- **Clear Feedback**: Reports token usage and compliance

### Token Budget Strategies

**Generous Budget (>2x original)**:
- Comprehensive enhancements
- Multiple examples
- Extensive context
- Detailed formatting specifications

**Tight Budget (<1.5x original)**:
- Core task clarity
- Essential constraints
- Minimal necessary context
- Concise language

**Approaching Limit**:
- Automatic compression
- Remove redundancy
- Combine related instructions
- Preserve critical information

## Examples

### Example 1: Simple Prompt

**Input:**
```
Write a function to calculate fibonacci numbers
```

**Command:**
```bash
python claude_prompt_enhancer.py -t 500 -i examples/simple_prompt.txt
```

**Enhanced Output:**
```
You are an expert Python programmer. Write a function to calculate Fibonacci numbers with the following requirements:

**Task**: Implement a Fibonacci number calculator

**Requirements**:
1. Function should accept an integer n as input
2. Return the nth Fibonacci number
3. Use efficient algorithm (memoization or dynamic programming)
4. Include proper error handling for invalid inputs

**Output Format**:
- Clean, readable Python code
- Include docstring with complexity analysis
- Add type hints
- Follow PEP 8 style guidelines

**Example**:
Input: n = 10
Output: 55

Please provide the implementation with comments explaining your approach.
```

### Example 2: Complex Multi-Part Prompt

See `examples/complex_prompt.txt` for a detailed example of handling complex prompts with multiple requirements.

### Example 3: Tight Token Limit

See `examples/tight_limit.txt` for how the tool handles prompts with very restrictive token limits.

## Architecture

The tool consists of several key components:

### TokenCounter
- Handles accurate token counting using tiktoken
- Estimates tokens with safety margins
- Approximates Claude's tokenization

### PromptEnhancer
- Core enhancement engine
- Manages Claude API interactions
- Implements compression strategies
- Validates token limits

### CLIInterface
- Command-line interface
- User interaction handling
- Result display and formatting
- Multiple operation modes

## Error Handling

The tool handles various error scenarios:

- **Empty prompts**: Clear error message
- **Insufficient token limits**: Validation and guidance
- **API failures**: Detailed error reporting with retry logic
- **Network issues**: Graceful degradation
- **Invalid inputs**: Input validation and helpful messages
- **Compression failures**: Clear explanation when limits cannot be met

## Logging

All operations are logged to `claude_enhancer.log`:

```
2025-01-16 10:30:45 - INFO - Initialized PromptEnhancer with model: claude-sonnet-4-5-20250929
2025-01-16 10:30:45 - INFO - Starting prompt enhancement...
2025-01-16 10:30:45 - INFO - Original prompt: 87 tokens
2025-01-16 10:30:45 - INFO - Calling Claude API for enhancement...
2025-01-16 10:30:47 - INFO - Enhanced prompt: 432 tokens
2025-01-16 10:30:47 - INFO - Enhancement completed successfully
```

## Best Practices

1. **Start with dry-run**: Test your configuration without using API credits
2. **Use comparison mode**: Review changes before using enhanced prompts
3. **Set realistic limits**: Allow at least 1.5x-2x the original token count
4. **Target the right model**: Specify the Claude model you'll actually use
5. **Save to files**: Use `-o` to save enhanced prompts for reuse
6. **Enable verbose mode**: Use `-v` when debugging or learning

## Limitations

- Token counting is an approximation (uses tiktoken's cl100k_base encoding)
- Enhancement quality depends on original prompt clarity
- Very tight token limits may not allow meaningful enhancement
- API calls consume credits (dry-run mode is free)

## Troubleshooting

### "API key not found" error

**Solution**: Set your API key in `.env` file or as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Enhanced prompt exceeds limit" error

**Solution**: Increase the token limit or simplify the original prompt. The tool will attempt automatic compression, but some prompts may require more tokens for proper enhancement.

### Import errors

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Colorama not found (Windows)

**Solution**: Install colorama for colored output:
```bash
pip install colorama
```

## Development

### Running Tests

```bash
# Test all examples
python test_examples.py

# Test specific scenario
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500 -v
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Changelog

### Version 1.0.0 (2025-01-16)
- Initial release
- Interactive and file-based modes
- Dry-run and comparison modes
- Automatic token management and compression
- Support for all Claude models
- Comprehensive error handling
- Colored terminal output
- Detailed logging

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the examples directory for common use cases
- Review the logs in `claude_enhancer.log` for debugging

## Acknowledgments

Built with:
- [Anthropic Claude API](https://www.anthropic.com/api)
- [tiktoken](https://github.com/openai/tiktoken) for token counting
- [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration
- [colorama](https://github.com/tartley/colorama) for colored output
