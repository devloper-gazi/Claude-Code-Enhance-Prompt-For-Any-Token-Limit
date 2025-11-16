# Example Prompts

This directory contains example prompts demonstrating various use cases for the Claude Prompt Enhancer.

## Examples Overview

### 1. simple_prompt.txt
**Scenario**: Very basic, single-sentence prompt
**Original**: "Write a function to calculate fibonacci numbers"
**Token Count**: ~10 tokens
**Recommended Limit**: 500-1000 tokens
**Use Case**: Testing enhancement of minimal prompts

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i simple_prompt.txt -t 500 --compare
```

### 2. complex_prompt.txt
**Scenario**: Multi-requirement task with implicit constraints
**Original**: REST API development with multiple features
**Token Count**: ~50 tokens
**Recommended Limit**: 2000-3000 tokens
**Use Case**: Complex projects requiring detailed specifications

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i complex_prompt.txt -t 2000 -o complex_enhanced.txt
```

### 3. tight_limit.txt
**Scenario**: Simple prompt with very restrictive token limit
**Original**: "Explain quantum computing"
**Token Count**: ~5 tokens
**Recommended Limit**: 100-200 tokens
**Use Case**: Testing compression and prioritization

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i tight_limit.txt -t 150 -v
```

### 4. well_structured.txt
**Scenario**: Already well-structured prompt
**Original**: Detailed data analysis request with clear sections
**Token Count**: ~100 tokens
**Recommended Limit**: 1500-2000 tokens
**Use Case**: Enhancing prompts that already follow best practices

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i well_structured.txt -t 1500 --compare
```

### 5. code_review.txt
**Scenario**: Vague request lacking specifics
**Original**: "Review my Python code for security vulnerabilities and performance issues"
**Token Count**: ~15 tokens
**Recommended Limit**: 800-1200 tokens
**Use Case**: Adding structure and criteria to open-ended requests

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i code_review.txt -t 1000
```

### 6. creative_writing.txt
**Scenario**: Creative task with minimal constraints
**Original**: "Write a short story about a time traveler"
**Token Count**: ~10 tokens
**Recommended Limit**: 600-1000 tokens
**Use Case**: Adding style, tone, and structural guidance to creative prompts

**Try it:**
```bash
python ../claude_prompt_enhancer.py -i creative_writing.txt -t 800 --compare
```

## Testing Different Token Limits

You can experiment with different token limits to see how the enhancement adapts:

### Tight Budget (1.2x-1.5x original)
```bash
# Minimal enhancement - essential improvements only
python ../claude_prompt_enhancer.py -i complex_prompt.txt -t 100
```

### Moderate Budget (2x-3x original)
```bash
# Balanced enhancement - structure, context, and examples
python ../claude_prompt_enhancer.py -i complex_prompt.txt -t 300
```

### Generous Budget (>3x original)
```bash
# Comprehensive enhancement - everything included
python ../claude_prompt_enhancer.py -i complex_prompt.txt -t 2000
```

## Batch Processing Examples

Process multiple prompts and save outputs:

```bash
# Process all examples
for file in *.txt; do
    python ../claude_prompt_enhancer.py -i "$file" -t 1000 -o "${file%.txt}_enhanced.txt"
done
```

## Dry Run Testing

Test without using API credits:

```bash
# See what would happen with each example
python ../claude_prompt_enhancer.py -i simple_prompt.txt -t 500 --dry-run
python ../claude_prompt_enhancer.py -i complex_prompt.txt -t 2000 --dry-run
python ../claude_prompt_enhancer.py -i tight_limit.txt -t 150 --dry-run
```

## Expected Enhancement Patterns

### Simple Prompts
**Enhancement includes:**
- Task specification and requirements
- Output format details
- Code quality expectations
- Example input/output
- Error handling requirements

### Complex Prompts
**Enhancement includes:**
- Breaking down into components
- Explicit technical specifications
- API design considerations
- Security and authentication details
- Testing and validation criteria
- Documentation requirements

### Tight Limits
**Enhancement focuses on:**
- Core task clarity
- Essential constraints only
- Minimal but critical context
- Concise language throughout

### Well-Structured Prompts
**Enhancement adds:**
- Additional clarity and precision
- Explicit success criteria
- Output formatting details
- Quality benchmarks
- Edge case considerations

## Creating Your Own Test Cases

To create effective test prompts:

1. **Start vague**: The more basic your prompt, the more dramatic the enhancement
2. **Vary complexity**: Test both simple and multi-part tasks
3. **Test limits**: Try very restrictive token limits to see compression
4. **Mix domains**: Code, writing, analysis, creative tasks, etc.
5. **Include edge cases**: Already perfect prompts, ambiguous prompts, etc.

## Comparing Results

Use comparison mode to see exactly what changed:

```bash
python ../claude_prompt_enhancer.py -i simple_prompt.txt -t 500 --compare
```

This shows original and enhanced side-by-side, making it easy to:
- Understand enhancement patterns
- Learn prompt engineering techniques
- Verify core intent is preserved
- Check token usage efficiency

## Notes

- Token counts are approximations using tiktoken
- Enhancement quality varies by original prompt clarity
- Very tight limits may not allow meaningful enhancement
- Dry-run mode is useful for learning without API costs
