# Claude Prompt Enhancer - Usage Guide

This guide provides practical examples and workflows for using the Claude Prompt Enhancer effectively.

## Quick Start

### First-Time Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. Test with dry-run:
   ```bash
   python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500 --dry-run
   ```

4. Run your first enhancement:
   ```bash
   python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500
   ```

## Common Workflows

### Workflow 1: Quick Interactive Enhancement

**Use case**: You have a prompt in mind and want to enhance it quickly.

```bash
# Start interactive mode
python claude_prompt_enhancer.py -t 1000

# Paste your prompt, then press Ctrl+D (Unix) or Ctrl+Z (Windows)
```

**When to use**: Ad-hoc prompt improvements, quick experiments

### Workflow 2: File-Based Enhancement with Output

**Use case**: You have prompts in files and want to save enhanced versions.

```bash
# Enhance and save
python claude_prompt_enhancer.py -i my_prompt.txt -o my_prompt_enhanced.txt -t 2000

# Use the enhanced prompt
cat my_prompt_enhanced.txt | pbcopy  # macOS
cat my_prompt_enhanced.txt | xclip   # Linux
```

**When to use**: Production prompts, team collaboration, version control

### Workflow 3: Comparison and Iteration

**Use case**: You want to see what changes before committing to them.

```bash
# See side-by-side comparison
python claude_prompt_enhancer.py -i my_prompt.txt -t 2000 --compare

# Adjust token limit and compare again
python claude_prompt_enhancer.py -i my_prompt.txt -t 1500 --compare
python claude_prompt_enhancer.py -i my_prompt.txt -t 1000 --compare
```

**When to use**: Learning prompt engineering, quality control, optimization

### Workflow 4: Batch Processing

**Use case**: You have multiple prompts to enhance.

```bash
# Create a batch processing script
cat > enhance_all.sh << 'EOF'
#!/bin/bash
for file in prompts/*.txt; do
    basename="${file%.txt}"
    python claude_prompt_enhancer.py -i "$file" -o "enhanced/${basename}_enhanced.txt" -t 2000
    echo "Processed: $file"
done
EOF

chmod +x enhance_all.sh
./enhance_all.sh
```

**When to use**: Multiple projects, template creation, bulk optimization

### Workflow 5: Model-Specific Optimization

**Use case**: You're targeting a specific Claude model.

```bash
# Optimize for Opus 4.1 (default)
python claude_prompt_enhancer.py -i task.txt -t 4000 -m opus-4.1 -o task_opus.txt

# Optimize for Sonnet 4.5
python claude_prompt_enhancer.py -i task.txt -t 2000 -m sonnet-4.5 -o task_sonnet.txt

# Optimize for Haiku 3.5 (shorter prompts)
python claude_prompt_enhancer.py -i task.txt -t 1000 -m haiku-3.5 -o task_haiku.txt
```

**When to use**: Cost optimization, performance tuning, multi-model deployments

### Workflow 6: Development and Debugging

**Use case**: You're developing or troubleshooting.

```bash
# Verbose mode with full debugging
python claude_prompt_enhancer.py -i test.txt -t 1000 -v 2>&1 | tee debug.log

# Check the log file
tail -f claude_enhancer.log
```

**When to use**: Troubleshooting issues, understanding behavior, development

## Token Limit Guidelines

### How to Choose a Token Limit

**General Formula**: Target = Original × Enhancement Factor

| Enhancement Level | Factor | Description |
|------------------|--------|-------------|
| Minimal | 1.2-1.5× | Basic clarity improvements |
| Moderate | 2-3× | Standard enhancement |
| Comprehensive | 3-5× | Full enhancement with examples |
| Extensive | >5× | Maximum detail and context |

### Examples by Prompt Type

**Simple coding task** (original: ~20 tokens)
```bash
# Minimal: 30-50 tokens
python claude_prompt_enhancer.py -i code_task.txt -t 50

# Moderate: 100-200 tokens
python claude_prompt_enhancer.py -i code_task.txt -t 150

# Comprehensive: 300-500 tokens
python claude_prompt_enhancer.py -i code_task.txt -t 400
```

**Complex project** (original: ~100 tokens)
```bash
# Minimal: 150-200 tokens
python claude_prompt_enhancer.py -i project.txt -t 200

# Moderate: 300-500 tokens
python claude_prompt_enhancer.py -i project.txt -t 400

# Comprehensive: 1000-2000 tokens
python claude_prompt_enhancer.py -i project.txt -t 1500
```

**Creative writing** (original: ~15 tokens)
```bash
# Minimal: 25-40 tokens
python claude_prompt_enhancer.py -i story.txt -t 40

# Moderate: 100-300 tokens
python claude_prompt_enhancer.py -i story.txt -t 200

# Comprehensive: 500-1000 tokens
python claude_prompt_enhancer.py -i story.txt -t 800
```

## Best Practices

### 1. Start with Dry-Run

Always preview before making API calls:

```bash
# Check token budget and configuration
python claude_prompt_enhancer.py -i prompt.txt -t 1000 --dry-run

# If satisfied, remove --dry-run
python claude_prompt_enhancer.py -i prompt.txt -t 1000
```

### 2. Use Comparison Mode for Learning

Understand what makes a good prompt:

```bash
# See exactly what changed
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 500 --compare

# Try different limits to see adaptation
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 200 --compare
python claude_prompt_enhancer.py -i examples/simple_prompt.txt -t 1000 --compare
```

### 3. Save Enhanced Prompts

Build a library of high-quality prompts:

```bash
# Create organized structure
mkdir -p prompts/{original,enhanced}

# Enhance and save
python claude_prompt_enhancer.py \
    -i prompts/original/task.txt \
    -o prompts/enhanced/task.txt \
    -t 2000
```

### 4. Version Control Your Prompts

Track prompt evolution:

```bash
git add prompts/original/task.txt
git commit -m "Add original prompt for user authentication"

python claude_prompt_enhancer.py -i prompts/original/task.txt -o prompts/enhanced/task.txt -t 2000

git add prompts/enhanced/task.txt
git commit -m "Add enhanced prompt for user authentication"
```

### 5. Document Token Limits

Keep track of what works:

```bash
# Create a metadata file
cat > prompts/metadata.json << EOF
{
    "task_auth": {
        "original_tokens": 45,
        "enhanced_tokens": 387,
        "token_limit": 500,
        "target_model": "opus-4.1",
        "performance": "excellent"
    }
}
EOF
```

## Real-World Scenarios

### Scenario 1: Code Review Automation

```bash
# Original vague prompt
echo "Review this code" > review_prompt.txt

# Enhance with specific criteria
python claude_prompt_enhancer.py -i review_prompt.txt -t 1200 -o review_enhanced.txt

# Result includes:
# - Security checklist
# - Performance considerations
# - Code style guidelines
# - Documentation requirements
# - Testing coverage expectations
```

### Scenario 2: Data Analysis Tasks

```bash
# Original
echo "Analyze the sales data" > analysis_prompt.txt

# Enhance
python claude_prompt_enhancer.py -i analysis_prompt.txt -t 1500 -o analysis_enhanced.txt

# Result includes:
# - Specific metrics to calculate
# - Visualization requirements
# - Statistical methods to use
# - Report structure
# - Business insights format
```

### Scenario 3: Content Generation

```bash
# Original
echo "Write a blog post about AI" > blog_prompt.txt

# Enhance
python claude_prompt_enhancer.py -i blog_prompt.txt -t 1000 -o blog_enhanced.txt --compare

# Result includes:
# - Target audience definition
# - Tone and style guidelines
# - Structure (intro, body, conclusion)
# - Length requirements
# - SEO considerations
# - Key points to cover
```

### Scenario 4: API Development

```bash
# Original
echo "Create a REST API for user management" > api_prompt.txt

# Enhance with technical details
python claude_prompt_enhancer.py -i api_prompt.txt -t 2500 -m opus-4.1 -o api_enhanced.txt

# Result includes:
# - Endpoint specifications
# - Authentication methods
# - Data validation rules
# - Error handling patterns
# - Response formats
# - Testing requirements
# - Documentation needs
```

## Troubleshooting Common Issues

### Issue: "Enhanced prompt exceeds limit"

**Solution**:
```bash
# Increase token limit
python claude_prompt_enhancer.py -i prompt.txt -t 2000  # was 1000

# Or simplify original prompt
echo "Simplified version" > prompt_simple.txt
python claude_prompt_enhancer.py -i prompt_simple.txt -t 1000
```

### Issue: "API key not found"

**Solution**:
```bash
# Set environment variable
export ANTHROPIC_API_KEY='your-key-here'

# Or use command line
python claude_prompt_enhancer.py -i prompt.txt -t 1000 --api-key your-key-here

# Or create .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Issue: Enhancement too generic

**Solution**:
```bash
# Provide more context in original prompt
cat > detailed_prompt.txt << EOF
Context: E-commerce platform with 10M users
Task: Optimize checkout flow
Constraints: Must maintain current UI framework
Goal: Reduce cart abandonment by 20%
EOF

python claude_prompt_enhancer.py -i detailed_prompt.txt -t 2000
```

### Issue: Want more control over enhancement

**Solution**:
```bash
# Start with well-structured original
cat > structured_prompt.txt << EOF
As a senior backend engineer, implement a caching layer with:
1. Redis integration
2. Cache invalidation strategy
3. Monitoring and metrics
4. Fallback mechanisms
EOF

# Enhancement will refine rather than restructure
python claude_prompt_enhancer.py -i structured_prompt.txt -t 1500
```

## Advanced Tips

### 1. Chain Enhancements

```bash
# First pass: moderate enhancement
python claude_prompt_enhancer.py -i original.txt -t 1000 -o pass1.txt

# Review and manually edit pass1.txt

# Second pass: further refinement
python claude_prompt_enhancer.py -i pass1.txt -t 1500 -o final.txt
```

### 2. Template Creation

```bash
# Create a base template
cat > template_base.txt << EOF
[Task description]
[Requirements list]
[Output format]
[Constraints]
EOF

# Enhance to create full template
python claude_prompt_enhancer.py -i template_base.txt -t 2000 -o template_full.txt
```

### 3. A/B Testing Prompts

```bash
# Create two versions with different limits
python claude_prompt_enhancer.py -i task.txt -t 1000 -o task_concise.txt
python claude_prompt_enhancer.py -i task.txt -t 2500 -o task_detailed.txt

# Test both with Claude to see which performs better
```

### 4. Integration with Scripts

```python
#!/usr/bin/env python3
import subprocess
import json

def enhance_prompt(prompt_text, token_limit=2000):
    """Enhance a prompt using the tool."""
    # Write prompt to temp file
    with open('/tmp/prompt_in.txt', 'w') as f:
        f.write(prompt_text)

    # Run enhancer
    subprocess.run([
        'python', 'claude_prompt_enhancer.py',
        '-i', '/tmp/prompt_in.txt',
        '-o', '/tmp/prompt_out.txt',
        '-t', str(token_limit)
    ])

    # Read result
    with open('/tmp/prompt_out.txt', 'r') as f:
        return f.read()

# Use in your workflow
enhanced = enhance_prompt("Your prompt here", 1500)
print(enhanced)
```

## Performance Optimization

### Minimize API Costs

```bash
# Use dry-run for testing
python claude_prompt_enhancer.py -i prompt.txt -t 1000 --dry-run

# Batch similar prompts together
# Process during off-peak hours if rate-limited
```

### Optimize Token Usage

```bash
# Find the minimum effective token limit
for limit in 500 1000 1500 2000; do
    echo "Testing limit: $limit"
    python claude_prompt_enhancer.py -i prompt.txt -t $limit -o "test_$limit.txt"
done

# Compare results and choose the sweet spot
```

## Getting Help

```bash
# Show all options
python claude_prompt_enhancer.py --help

# Check logs for errors
tail -n 50 claude_enhancer.log

# Run with verbose mode
python claude_prompt_enhancer.py -i prompt.txt -t 1000 -v
```

## Next Steps

1. Try all examples in the `examples/` directory
2. Experiment with different token limits
3. Create your own prompt library
4. Integrate into your development workflow
5. Share effective prompts with your team
