#!/usr/bin/env python3
"""
Claude Prompt Enhancer - A tool to enhance prompts for optimal Claude API performance.

This tool takes user prompts and enhances them following best practices while respecting
specified token limits. It uses Claude API to intelligently transform basic prompts into
well-structured, detailed instructions.
"""

import os
import sys
import argparse
import logging
from typing import Optional, Dict, Tuple
from pathlib import Path
import anthropic
from dotenv import load_dotenv
import tiktoken

# Try to import colorama for colored output, but make it optional
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Define dummy color constants
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('claude_enhancer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Claude model configurations
CLAUDE_MODELS = {
    'opus-4.1': 'claude-opus-4-20250514',
    'sonnet-4.5': 'claude-sonnet-4-5-20250929',
    'sonnet-3.5': 'claude-3-5-sonnet-20241022',
    'haiku-3.5': 'claude-3-5-haiku-20241022',
}

# Default token limit safety margin (5%)
SAFETY_MARGIN = 0.05


class TokenCounter:
    """Handle token counting for Claude prompts using tiktoken approximation."""

    def __init__(self):
        """Initialize the token counter with Claude's tokenizer approximation."""
        self.encoder = None
        self.use_fallback = False

        try:
            # Try to use cl100k_base as an approximation for Claude tokens
            # This is similar to GPT-4's tokenizer and provides good estimates
            self.encoder = tiktoken.get_encoding("cl100k_base")
            logger.info("Initialized tiktoken encoder successfully")
        except Exception as e:
            logger.warning(f"Could not initialize tiktoken: {e}")
            logger.info("Using fallback token counting method")
            self.use_fallback = True

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text: The text to count tokens for

        Returns:
            The estimated number of tokens
        """
        if self.use_fallback or self.encoder is None:
            # Fallback method: approximate token count
            # Based on typical Claude tokenization patterns:
            # - Avg ~3.5-4 chars per token for English text
            # - Whitespace is typically a token boundary
            words = text.split()
            # Rough estimate: count words, punctuation, and special chars
            token_estimate = len(words)  # Words
            token_estimate += text.count('\n')  # Newlines
            token_estimate += sum(text.count(p) for p in '.,;:!?()[]{}')  # Punctuation
            # Add extra for longer words (more likely to be split)
            token_estimate += sum(1 for w in words if len(w) > 10)
            return max(len(text) // 4, token_estimate)  # Use whichever is larger

        try:
            tokens = self.encoder.encode(text)
            return len(tokens)
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            # Fallback to rough estimation: ~4 chars per token
            return len(text) // 4

    def estimate_tokens_with_margin(self, text: str, margin: float = SAFETY_MARGIN) -> int:
        """
        Estimate tokens with a safety margin.

        Args:
            text: The text to count tokens for
            margin: Safety margin percentage (default 5%)

        Returns:
            Token count with margin applied
        """
        base_count = self.count_tokens(text)
        return int(base_count * (1 + margin))


class PromptEnhancer:
    """Core prompt enhancement engine using Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: str = 'sonnet-4.5'):
        """
        Initialize the prompt enhancer.

        Args:
            api_key: Anthropic API key (if None, loads from environment)
            model: Claude model to use for enhancement
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or provide it explicitly."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = CLAUDE_MODELS.get(model, CLAUDE_MODELS['sonnet-4.5'])
        self.token_counter = TokenCounter()
        logger.info(f"Initialized PromptEnhancer with model: {self.model}")

    def _create_enhancement_prompt(
        self,
        original_prompt: str,
        token_limit: int,
        target_model: str
    ) -> str:
        """
        Create the meta-prompt for Claude to enhance the user's prompt.

        Args:
            original_prompt: The user's original prompt
            token_limit: Maximum tokens for enhanced prompt
            target_model: The Claude model the enhanced prompt will be used with

        Returns:
            The enhancement instruction prompt
        """
        # Calculate effective token limit with safety margin
        effective_limit = int(token_limit * (1 - SAFETY_MARGIN))

        enhancement_instructions = f"""You are an expert prompt engineer specializing in optimizing prompts for Claude AI models. Your task is to enhance the following user prompt to maximize output quality while STRICTLY adhering to the specified token limit.

ORIGINAL PROMPT:
{original_prompt}

TARGET MODEL: {target_model}
MAXIMUM TOKEN LIMIT: {token_limit} tokens (with 5% safety margin, aim for {effective_limit} tokens)

ENHANCEMENT REQUIREMENTS:

1. **Structure & Clarity**
   - Break complex requests into logical sections
   - Use clear headings and organization
   - Number steps when sequence matters
   - Separate concerns into distinct parts

2. **Output Specifications**
   - Define desired length, format, and structure
   - Specify tone (formal, casual, technical, etc.)
   - Indicate preferred formatting (markdown, bullet points, paragraphs)
   - Set quality and depth expectations

3. **Context & Background**
   - Add relevant domain context
   - Specify the intended audience
   - Define success criteria
   - Clarify the task's purpose and goals

4. **Examples (when beneficial)**
   - Provide concrete examples of desired output
   - Show input/output patterns if applicable
   - Illustrate edge cases to handle

5. **Constraints & Requirements**
   - Make implicit constraints explicit
   - Define boundaries and limitations
   - Specify what to avoid or exclude
   - Set quality thresholds

6. **Role-Based Framing (when appropriate)**
   - Assign relevant expertise ("You are an expert...")
   - Define perspective or viewpoint
   - Set the appropriate knowledge level

7. **Reasoning Guidance (for complex tasks)**
   - Request step-by-step analysis
   - Ask for consideration of multiple perspectives
   - Specify decision-making criteria
   - Request explanation of reasoning

8. **Ambiguity Elimination**
   - Replace vague terms with precise language
   - Clarify potentially multiple interpretations
   - Define domain-specific terminology
   - Remove unnecessary jargon

TOKEN MANAGEMENT STRATEGY:

- **If token budget is generous (>2x original)**: Include comprehensive enhancements, multiple examples, extensive context, detailed formatting specs
- **If token budget is tight (<1.5x original)**: Prioritize core task clarity, essential constraints, minimal necessary context
- **If approaching limit**: Use concise language, combine related instructions, remove redundancy while preserving all critical information

CRITICAL RULES:
1. The enhanced prompt MUST stay within {effective_limit} tokens (with safety margin)
2. Maintain the EXACT core intent of the original prompt
3. Do NOT introduce unintended assumptions or constraints
4. Do NOT change the fundamental task or goal
5. Follow Anthropic's prompt engineering best practices
6. Output ONLY the enhanced prompt, no commentary or explanations

Enhanced prompt:"""

        return enhancement_instructions

    def enhance_prompt(
        self,
        original_prompt: str,
        token_limit: int,
        target_model: str = 'opus-4.1',
        verbose: bool = False
    ) -> Dict[str, any]:
        """
        Enhance a prompt using Claude API.

        Args:
            original_prompt: The original user prompt
            token_limit: Maximum tokens for the enhanced prompt
            target_model: The Claude model the prompt will be used with
            verbose: Whether to include debug information

        Returns:
            Dictionary containing enhancement results and metadata
        """
        logger.info("Starting prompt enhancement...")

        # Validate inputs
        if not original_prompt or not original_prompt.strip():
            raise ValueError("Original prompt cannot be empty")

        if token_limit < 50:
            raise ValueError("Token limit must be at least 50 tokens")

        # Count original tokens
        original_tokens = self.token_counter.count_tokens(original_prompt)
        logger.info(f"Original prompt: {original_tokens} tokens")

        # Check if original already exceeds limit
        if original_tokens > token_limit:
            logger.warning(
                f"Original prompt ({original_tokens} tokens) exceeds "
                f"target limit ({token_limit} tokens)"
            )

        # Create enhancement prompt
        enhancement_prompt = self._create_enhancement_prompt(
            original_prompt,
            token_limit,
            target_model
        )

        if verbose:
            logger.debug(f"Enhancement prompt length: {len(enhancement_prompt)} chars")

        try:
            # Call Claude API for enhancement
            logger.info("Calling Claude API for enhancement...")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,  # Lower temperature for more consistent enhancements
                messages=[{
                    "role": "user",
                    "content": enhancement_prompt
                }]
            )

            enhanced_prompt = response.content[0].text.strip()

            # Count enhanced tokens
            enhanced_tokens = self.token_counter.count_tokens(enhanced_prompt)
            logger.info(f"Enhanced prompt: {enhanced_tokens} tokens")

            # Validate token limit compliance
            if enhanced_tokens > token_limit:
                logger.warning(
                    f"Enhanced prompt ({enhanced_tokens} tokens) exceeds "
                    f"limit ({token_limit} tokens). Attempting compression..."
                )
                # Try to compress by requesting a more concise version
                enhanced_prompt = self._compress_prompt(
                    enhanced_prompt,
                    token_limit,
                    target_model
                )
                enhanced_tokens = self.token_counter.count_tokens(enhanced_prompt)

            # Calculate statistics
            improvement_ratio = enhanced_tokens / original_tokens if original_tokens > 0 else 0
            within_limit = enhanced_tokens <= token_limit

            result = {
                'original_prompt': original_prompt,
                'enhanced_prompt': enhanced_prompt,
                'original_tokens': original_tokens,
                'enhanced_tokens': enhanced_tokens,
                'token_limit': token_limit,
                'within_limit': within_limit,
                'improvement_ratio': improvement_ratio,
                'target_model': target_model,
                'enhancement_model': self.model,
                'api_usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                }
            }

            if verbose:
                result['enhancement_instructions'] = enhancement_prompt

            logger.info("Enhancement completed successfully")
            return result

        except anthropic.APIError as e:
            logger.error(f"API error during enhancement: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during enhancement: {e}")
            raise

    def _compress_prompt(
        self,
        prompt: str,
        token_limit: int,
        target_model: str
    ) -> str:
        """
        Compress a prompt to fit within token limit.

        Args:
            prompt: The prompt to compress
            token_limit: Target token limit
            target_model: Target Claude model

        Returns:
            Compressed prompt
        """
        effective_limit = int(token_limit * (1 - SAFETY_MARGIN))

        compression_prompt = f"""Compress the following prompt to fit within {effective_limit} tokens while preserving ALL critical information and intent:

PROMPT TO COMPRESS:
{prompt}

COMPRESSION RULES:
1. Remove redundant phrasing
2. Combine related instructions
3. Use more concise language
4. Keep all essential constraints and requirements
5. Maintain clarity and precision
6. Do NOT remove important context or specifications

Output ONLY the compressed prompt, nothing else:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": compression_prompt
                }]
            )

            compressed = response.content[0].text.strip()
            compressed_tokens = self.token_counter.count_tokens(compressed)

            if compressed_tokens <= token_limit:
                logger.info(f"Successfully compressed to {compressed_tokens} tokens")
                return compressed
            else:
                logger.error(
                    f"Compression failed: {compressed_tokens} tokens still exceeds "
                    f"{token_limit} limit"
                )
                raise ValueError(
                    f"Unable to compress prompt to {token_limit} tokens. "
                    f"Current size: {compressed_tokens} tokens. "
                    "Please increase the token limit or simplify the original prompt."
                )
        except Exception as e:
            logger.error(f"Compression failed: {e}")
            raise


class CLIInterface:
    """Command-line interface for the prompt enhancer."""

    def __init__(self):
        """Initialize the CLI interface."""
        self.enhancer = None
        self.token_counter = TokenCounter()

    def print_colored(self, text: str, color: str = None, bright: bool = False):
        """Print colored text if colorama is available."""
        if COLORS_AVAILABLE and color:
            color_code = getattr(Fore, color.upper(), Fore.WHITE)
            style = Style.BRIGHT if bright else ""
            print(f"{style}{color_code}{text}{Style.RESET_ALL}")
        else:
            print(text)

    def print_header(self, text: str):
        """Print a section header."""
        self.print_colored(f"\n{'='*70}", 'cyan')
        self.print_colored(f"  {text}", 'cyan', bright=True)
        self.print_colored(f"{'='*70}", 'cyan')

    def print_separator(self):
        """Print a separator line."""
        self.print_colored('-' * 70, 'blue')

    def display_results(self, results: Dict, show_comparison: bool = False):
        """
        Display enhancement results to the user.

        Args:
            results: Enhancement results dictionary
            show_comparison: Whether to show side-by-side comparison
        """
        self.print_header("ENHANCEMENT RESULTS")

        # Token statistics
        self.print_colored("\n📊 Token Statistics:", 'yellow', bright=True)
        print(f"  Original tokens:  {results['original_tokens']}")
        print(f"  Enhanced tokens:  {results['enhanced_tokens']}")
        print(f"  Token limit:      {results['token_limit']}")
        print(f"  Improvement:      {results['improvement_ratio']:.2f}x")

        # Status
        status_color = 'green' if results['within_limit'] else 'red'
        status_text = '✓ Within limit' if results['within_limit'] else '✗ Exceeds limit'
        self.print_colored(f"  Status:           {status_text}", status_color, bright=True)

        # API usage
        if 'api_usage' in results:
            self.print_colored("\n🔧 API Usage:", 'yellow', bright=True)
            print(f"  Input tokens:     {results['api_usage']['input_tokens']}")
            print(f"  Output tokens:    {results['api_usage']['output_tokens']}")

        # Model info
        self.print_colored("\n🤖 Models:", 'yellow', bright=True)
        print(f"  Enhancement:      {results['enhancement_model']}")
        print(f"  Target:           {results['target_model']}")

        # Enhanced prompt
        self.print_header("ENHANCED PROMPT")
        print(results['enhanced_prompt'])

        # Comparison mode
        if show_comparison:
            self.print_header("COMPARISON VIEW")
            self.print_colored("\n[ORIGINAL]", 'red', bright=True)
            print(results['original_prompt'])
            self.print_separator()
            self.print_colored("\n[ENHANCED]", 'green', bright=True)
            print(results['enhanced_prompt'])

        print()  # Final newline

    def interactive_mode(self, args):
        """Run the tool in interactive mode."""
        self.print_header("CLAUDE PROMPT ENHANCER - Interactive Mode")

        print("\nEnter your prompt (press Ctrl+D or Ctrl+Z when done):")
        print("───────────────────────────────────────────────────────")

        try:
            original_prompt = sys.stdin.read().strip()
        except KeyboardInterrupt:
            print("\n\nCancelled by user.")
            return

        if not original_prompt:
            self.print_colored("\n✗ Error: Empty prompt provided.", 'red', bright=True)
            return

        # Show original token count
        original_tokens = self.token_counter.count_tokens(original_prompt)
        print(f"\n📝 Original prompt: {original_tokens} tokens")

        # Run enhancement
        try:
            results = self.enhancer.enhance_prompt(
                original_prompt,
                args.token_limit,
                args.target_model,
                verbose=args.verbose
            )

            self.display_results(results, show_comparison=args.compare)

        except Exception as e:
            self.print_colored(f"\n✗ Enhancement failed: {e}", 'red', bright=True)
            logger.error(f"Enhancement failed: {e}", exc_info=True)

    def file_mode(self, args):
        """Process prompts from input file."""
        input_file = Path(args.input)

        if not input_file.exists():
            self.print_colored(
                f"✗ Error: Input file not found: {input_file}",
                'red',
                bright=True
            )
            return

        # Read input
        try:
            original_prompt = input_file.read_text(encoding='utf-8').strip()
        except Exception as e:
            self.print_colored(
                f"✗ Error reading input file: {e}",
                'red',
                bright=True
            )
            return

        if not original_prompt:
            self.print_colored("✗ Error: Input file is empty.", 'red', bright=True)
            return

        # Show original info
        original_tokens = self.token_counter.count_tokens(original_prompt)
        self.print_colored(
            f"\n📂 Processing: {input_file}",
            'cyan',
            bright=True
        )
        print(f"   Original: {original_tokens} tokens")

        # Run enhancement
        try:
            results = self.enhancer.enhance_prompt(
                original_prompt,
                args.token_limit,
                args.target_model,
                verbose=args.verbose
            )

            # Write output if specified
            if args.output:
                output_file = Path(args.output)
                output_file.write_text(results['enhanced_prompt'], encoding='utf-8')
                self.print_colored(
                    f"✓ Enhanced prompt saved to: {output_file}",
                    'green',
                    bright=True
                )

            self.display_results(results, show_comparison=args.compare)

        except Exception as e:
            self.print_colored(f"✗ Enhancement failed: {e}", 'red', bright=True)
            logger.error(f"Enhancement failed: {e}", exc_info=True)

    def dry_run_mode(self, args):
        """Show what would be done without making API calls."""
        self.print_header("DRY RUN MODE")

        if args.input:
            input_file = Path(args.input)
            if not input_file.exists():
                self.print_colored(
                    f"✗ Error: Input file not found: {input_file}",
                    'red',
                    bright=True
                )
                return
            prompt = input_file.read_text(encoding='utf-8').strip()
        else:
            print("\nEnter your prompt (press Ctrl+D or Ctrl+Z when done):")
            print("───────────────────────────────────────────────────────")
            try:
                prompt = sys.stdin.read().strip()
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
                return

        if not prompt:
            self.print_colored("✗ Error: Empty prompt provided.", 'red', bright=True)
            return

        tokens = self.token_counter.count_tokens(prompt)

        self.print_colored("\n📋 Configuration:", 'yellow', bright=True)
        print(f"  Input tokens:     {tokens}")
        print(f"  Token limit:      {args.token_limit}")
        print(f"  Target model:     {args.target_model}")
        print(f"  Enhancement with: {CLAUDE_MODELS.get('sonnet-4.5')}")

        if args.output:
            print(f"  Output file:      {args.output}")

        budget = args.token_limit - tokens
        self.print_colored(f"\n📊 Token Budget:", 'yellow', bright=True)
        print(f"  Available for enhancement: {budget} tokens")

        if budget < 0:
            self.print_colored(
                "  ⚠ Warning: Original already exceeds limit!",
                'red',
                bright=True
            )
        elif budget < tokens * 0.5:
            self.print_colored(
                "  ⚠ Tight budget - minimal enhancements possible",
                'yellow'
            )
        else:
            self.print_colored(
                "  ✓ Sufficient budget for comprehensive enhancement",
                'green'
            )

        self.print_colored("\n✓ Dry run complete. Use without --dry-run to execute.", 'green', bright=True)

    def run(self):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(
            description='Claude Prompt Enhancer - Optimize prompts for Claude API',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Interactive mode:
    %(prog)s -t 2000

  File mode:
    %(prog)s -i input.txt -o enhanced.txt -t 2000

  Dry run:
    %(prog)s -i input.txt -t 2000 --dry-run

  Comparison mode:
    %(prog)s -i input.txt -t 2000 --compare

  Verbose output:
    %(prog)s -i input.txt -t 2000 -v
            """
        )

        # Input options
        parser.add_argument(
            '-i', '--input',
            type=str,
            help='Input file containing the prompt to enhance'
        )
        parser.add_argument(
            '-o', '--output',
            type=str,
            help='Output file for the enhanced prompt'
        )

        # Enhancement options
        parser.add_argument(
            '-t', '--token-limit',
            type=int,
            required=True,
            help='Maximum token limit for the enhanced prompt'
        )
        parser.add_argument(
            '-m', '--target-model',
            type=str,
            default='opus-4.1',
            choices=list(CLAUDE_MODELS.keys()),
            help='Target Claude model for the enhanced prompt (default: opus-4.1)'
        )

        # Mode options
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making API calls'
        )
        parser.add_argument(
            '--compare',
            action='store_true',
            help='Show side-by-side comparison of original and enhanced prompts'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output for debugging'
        )

        # API configuration
        parser.add_argument(
            '--api-key',
            type=str,
            help='Anthropic API key (overrides ANTHROPIC_API_KEY env var)'
        )

        args = parser.parse_args()

        # Configure logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)

        # Dry run mode doesn't need API key
        if args.dry_run:
            self.dry_run_mode(args)
            return

        # Initialize enhancer
        try:
            self.enhancer = PromptEnhancer(
                api_key=args.api_key,
                model='sonnet-4.5'
            )
        except ValueError as e:
            self.print_colored(f"✗ Configuration error: {e}", 'red', bright=True)
            self.print_colored(
                "\nℹ Set your API key using one of these methods:",
                'yellow'
            )
            print("  1. Environment variable: export ANTHROPIC_API_KEY='your-key'")
            print("  2. .env file: ANTHROPIC_API_KEY=your-key")
            print("  3. Command line: --api-key your-key")
            return
        except Exception as e:
            self.print_colored(f"✗ Initialization error: {e}", 'red', bright=True)
            logger.error(f"Initialization failed: {e}", exc_info=True)
            return

        # Run appropriate mode
        if args.input:
            self.file_mode(args)
        else:
            self.interactive_mode(args)


def main():
    """Main entry point for the application."""
    # Load environment variables from .env file
    load_dotenv()

    # Create and run CLI
    cli = CLIInterface()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
