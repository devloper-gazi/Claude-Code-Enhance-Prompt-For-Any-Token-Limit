# Quick Start Guide

Get started with Claude Prompt Enhancer in 5 minutes!

## Installation

```bash
# 1. Clone the repository (or download the files)
git clone <repository-url>
cd Claude-Code-Enhance-Prompt-For-Any-Token-Limit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

## Your First Enhancement

### Option 1: Interactive Mode

```bash
# Start the tool
python claude_prompt_enhancer.py -t 1000

# Paste your prompt, then press Ctrl+D (Unix) or Ctrl+Z (Windows)
# Example: "Write a function to sort a list"
```

### Option 2: File Mode

```bash
# Create a prompt file
echo "Write a function to sort a list" > my_prompt.txt

# Enhance it
python claude_prompt_enhancer.py -i my_prompt.txt -t 1000
```

## Try the Examples

```bash
# Test with a simple example (no API calls)
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500 --dry-run

# See what changed
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500 --compare

# Save the enhanced version
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -o enhanced.txt -t 500
```

## Common Commands

```bash
# Get help
python claude_prompt_enhancer.py --help

# Dry run (no API calls, no cost)
python claude_prompt_enhancer.py -i prompt.txt -t 1000 --dry-run

# Compare original vs enhanced
python claude_prompt_enhancer.py -i prompt.txt -t 1000 --compare

# Verbose mode (see details)
python claude_prompt_enhancer.py -i prompt.txt -t 1000 -v

# Specify target model
python claude_prompt_enhancer.py -i prompt.txt -t 1000 -m sonnet-4.5
```

## Understanding Token Limits

**Rule of thumb**: Set token limit to 2-3x your original prompt length

```bash
# For a ~20 token prompt: use 500-1000
python claude_prompt_enhancer.py -i short_prompt.txt -t 500

# For a ~100 token prompt: use 1500-2000
python claude_prompt_enhancer.py -i medium_prompt.txt -t 1500

# For a ~200 token prompt: use 3000-5000
python claude_prompt_enhancer.py -i long_prompt.txt -t 3000
```

## Tips

1. **Always start with --dry-run** to preview without using API credits
2. **Use --compare** to learn what makes a good prompt
3. **Save to files** with `-o` for reusable prompts
4. **Set realistic limits**: More tokens = better enhancement (but diminishing returns)
5. **Check the logs** in `claude_enhancer.log` if something goes wrong

## What Gets Enhanced?

Your prompt gets improved with:
- ✅ Clear structure and organization
- ✅ Specific output format requirements
- ✅ Relevant context and background
- ✅ Concrete examples (when helpful)
- ✅ Explicit constraints and requirements
- ✅ Role-based framing
- ✅ Reasoning guidance for complex tasks
- ✅ Elimination of ambiguity

## Troubleshooting

**"API key not found"**
```bash
export ANTHROPIC_API_KEY='your-key'
# or create .env file
```

**"Token limit too small"**
```bash
# Increase the limit
python claude_prompt_enhancer.py -i prompt.txt -t 2000  # was 500
```

**"Import errors"**
```bash
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [USAGE_GUIDE.md](USAGE_GUIDE.md) for common workflows
- Explore the [examples/](examples/) directory
- Run `python test_examples.py` to verify your installation

## Example Workflow

```bash
# 1. Create your prompt
cat > task.txt << EOF
Build a web API for a todo list app
EOF

# 2. Preview enhancement (free)
python claude_prompt_enhancer.py -i task.txt -t 2000 --dry-run

# 3. Enhance and compare
python claude_prompt_enhancer.py -i task.txt -t 2000 --compare

# 4. Save enhanced version
python claude_prompt_enhancer.py -i task.txt -o task_enhanced.txt -t 2000

# 5. Use it with Claude!
cat task_enhanced.txt
```

Happy prompting! 🚀
