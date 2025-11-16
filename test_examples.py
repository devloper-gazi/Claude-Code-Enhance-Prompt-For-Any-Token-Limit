#!/usr/bin/env python3
"""
Test script for Claude Prompt Enhancer.

This script runs various test scenarios to validate the tool's functionality.
It can run in dry-run mode (no API calls) or full mode (with API calls).
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class TestRunner:
    """Test runner for the prompt enhancer."""

    def __init__(self, dry_run: bool = True):
        """Initialize the test runner."""
        self.dry_run = dry_run
        self.passed = 0
        self.failed = 0
        self.examples_dir = Path(__file__).parent / 'examples'
        self.script = Path(__file__).parent / 'claude_prompt_enhancer.py'

    def print_header(self, text: str):
        """Print a test section header."""
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")

    def print_test(self, name: str, status: str, details: str = ""):
        """Print test result."""
        symbols = {'PASS': '✓', 'FAIL': '✗', 'SKIP': '○'}
        colors = {'PASS': '\033[92m', 'FAIL': '\033[91m', 'SKIP': '\033[93m'}
        reset = '\033[0m'

        symbol = symbols.get(status, '?')
        color = colors.get(status, '')

        print(f"{color}{symbol} {name:<50} [{status}]{reset}")
        if details:
            print(f"  {details}")

    def run_command(self, args: List[str]) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def test_installation(self):
        """Test that all dependencies are installed."""
        self.print_header("Installation Tests")

        # Test Python version
        import sys
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self.print_test("Python version (>=3.8)", "PASS", f"Python {version.major}.{version.minor}")
            self.passed += 1
        else:
            self.print_test("Python version (>=3.8)", "FAIL", f"Python {version.major}.{version.minor}")
            self.failed += 1

        # Test required modules
        modules = ['anthropic', 'tiktoken', 'dotenv']
        for module in modules:
            try:
                __import__(module)
                self.print_test(f"Module: {module}", "PASS")
                self.passed += 1
            except ImportError:
                self.print_test(f"Module: {module}", "FAIL", "Run: pip install -r requirements.txt")
                self.failed += 1

        # Test script exists
        if self.script.exists():
            self.print_test("Script exists", "PASS", str(self.script))
            self.passed += 1
        else:
            self.print_test("Script exists", "FAIL", f"Not found: {self.script}")
            self.failed += 1

    def test_examples_exist(self):
        """Test that all example files exist."""
        self.print_header("Example Files Tests")

        examples = [
            'simple_prompt.txt',
            'complex_prompt.txt',
            'tight_limit.txt',
            'well_structured.txt',
            'code_review.txt',
            'creative_writing.txt'
        ]

        for example in examples:
            filepath = self.examples_dir / example
            if filepath.exists():
                self.print_test(f"Example: {example}", "PASS")
                self.passed += 1
            else:
                self.print_test(f"Example: {example}", "FAIL", "File missing")
                self.failed += 1

    def test_help_command(self):
        """Test that --help works."""
        self.print_header("CLI Interface Tests")

        returncode, stdout, stderr = self.run_command([
            'python', str(self.script), '--help'
        ])

        if returncode == 0 and 'usage:' in stdout:
            self.print_test("Help command", "PASS")
            self.passed += 1
        else:
            self.print_test("Help command", "FAIL", f"Exit code: {returncode}")
            self.failed += 1

    def test_dry_run_mode(self):
        """Test dry-run mode (no API calls)."""
        self.print_header("Dry-Run Mode Tests")

        test_cases = [
            ('simple_prompt.txt', 500, "Simple prompt with moderate limit"),
            ('complex_prompt.txt', 2000, "Complex prompt with generous limit"),
            ('tight_limit.txt', 150, "Tight token limit scenario"),
        ]

        for filename, token_limit, description in test_cases:
            filepath = self.examples_dir / filename

            if not filepath.exists():
                self.print_test(description, "SKIP", "Example file missing")
                continue

            returncode, stdout, stderr = self.run_command([
                'python', str(self.script),
                '-i', str(filepath),
                '-t', str(token_limit),
                '--dry-run'
            ])

            if returncode == 0 and 'Dry run complete' in stdout:
                self.print_test(description, "PASS")
                self.passed += 1
            else:
                self.print_test(description, "FAIL", f"Exit code: {returncode}")
                self.failed += 1

    def test_api_mode(self):
        """Test actual API calls (only if API key is available)."""
        self.print_header("API Enhancement Tests")

        # Check for API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            self.print_test("API key check", "SKIP", "ANTHROPIC_API_KEY not set")
            print("\nℹ️  To run API tests, set ANTHROPIC_API_KEY environment variable")
            return

        self.print_test("API key check", "PASS")
        self.passed += 1

        # Test simple enhancement
        filepath = self.examples_dir / 'simple_prompt.txt'
        if not filepath.exists():
            self.print_test("Simple enhancement", "SKIP", "Example file missing")
            return

        returncode, stdout, stderr = self.run_command([
            'python', str(self.script),
            '-i', str(filepath),
            '-t', '500'
        ])

        if returncode == 0 and 'ENHANCED PROMPT' in stdout:
            self.print_test("Simple enhancement", "PASS")
            self.passed += 1
        else:
            self.print_test("Simple enhancement", "FAIL", f"Exit code: {returncode}")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            self.failed += 1

    def test_file_output(self):
        """Test file output mode."""
        self.print_header("File Output Tests")

        output_file = Path('/tmp/test_enhanced_output.txt')
        input_file = self.examples_dir / 'simple_prompt.txt'

        # Clean up any existing output file
        if output_file.exists():
            output_file.unlink()

        if not input_file.exists():
            self.print_test("File output", "SKIP", "Example file missing")
            return

        returncode, stdout, stderr = self.run_command([
            'python', str(self.script),
            '-i', str(input_file),
            '-o', str(output_file),
            '-t', '500',
            '--dry-run'  # Use dry-run to avoid API calls
        ])

        # Note: dry-run mode doesn't actually create output files
        # This test just verifies the command runs without error
        if returncode == 0:
            self.print_test("File output (dry-run)", "PASS")
            self.passed += 1
        else:
            self.print_test("File output (dry-run)", "FAIL", f"Exit code: {returncode}")
            self.failed += 1

    def test_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        self.print_header("Error Handling Tests")

        # Test missing token limit
        returncode, stdout, stderr = self.run_command([
            'python', str(self.script),
            '-i', str(self.examples_dir / 'simple_prompt.txt')
        ])

        if returncode != 0:
            self.print_test("Missing token limit error", "PASS", "Correctly rejected")
            self.passed += 1
        else:
            self.print_test("Missing token limit error", "FAIL", "Should have failed")
            self.failed += 1

        # Test non-existent input file
        returncode, stdout, stderr = self.run_command([
            'python', str(self.script),
            '-i', '/nonexistent/file.txt',
            '-t', '1000',
            '--dry-run'
        ])

        if returncode != 0:
            self.print_test("Non-existent file error", "PASS", "Correctly rejected")
            self.passed += 1
        else:
            self.print_test("Non-existent file error", "FAIL", "Should have failed")
            self.failed += 1

    def test_model_options(self):
        """Test different model options."""
        self.print_header("Model Options Tests")

        models = ['opus-4.1', 'sonnet-4.5', 'sonnet-3.5', 'haiku-3.5']
        input_file = self.examples_dir / 'simple_prompt.txt'

        if not input_file.exists():
            self.print_test("Model options", "SKIP", "Example file missing")
            return

        for model in models:
            returncode, stdout, stderr = self.run_command([
                'python', str(self.script),
                '-i', str(input_file),
                '-t', '500',
                '-m', model,
                '--dry-run'
            ])

            if returncode == 0:
                self.print_test(f"Model option: {model}", "PASS")
                self.passed += 1
            else:
                self.print_test(f"Model option: {model}", "FAIL", f"Exit code: {returncode}")
                self.failed += 1

    def run_all_tests(self):
        """Run all tests."""
        print("\n" + "="*70)
        print("  CLAUDE PROMPT ENHANCER - TEST SUITE")
        print("="*70)

        if self.dry_run:
            print("\n⚠️  Running in DRY-RUN mode (no API calls)")
        else:
            print("\n🔴 Running in FULL mode (will make API calls)")

        # Run test suites
        self.test_installation()
        self.test_examples_exist()
        self.test_help_command()
        self.test_dry_run_mode()
        self.test_invalid_inputs()
        self.test_model_options()

        # Only run API tests if not in dry-run mode
        if not self.dry_run:
            self.test_api_mode()
            self.test_file_output()

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print("\n" + "="*70)
        print("  TEST SUMMARY")
        print("="*70)
        print(f"\n  Total tests: {total}")
        print(f"  ✓ Passed:    {self.passed}")
        print(f"  ✗ Failed:    {self.failed}")

        if self.failed == 0:
            print(f"\n  🎉 All tests passed!\n")
        else:
            print(f"\n  ⚠️  Some tests failed. Please review the output above.\n")

        return 0 if self.failed == 0 else 1


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Test suite for Claude Prompt Enhancer'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full tests including API calls (requires API key)'
    )

    args = parser.parse_args()

    runner = TestRunner(dry_run=not args.full)
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
