#!/usr/bin/env python3
"""
Test runner script for the Lünen Terminplaner project.
Provides different test execution options and coverage reporting.
"""

import sys
import subprocess
import argparse
import os

def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {cmd}")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run tests for Lünen Terminplaner')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--fast', action='store_true', help='Skip slow tests')
    parser.add_argument('--file', type=str, help='Run specific test file')
    
    args = parser.parse_args()
    
    # Base pytest command
    pytest_cmd = "python -m pytest"
    
    # Add verbosity
    if args.verbose:
        pytest_cmd += " -v"
    
    # Coverage options
    if args.coverage:
        pytest_cmd += " --cov=. --cov-report=html --cov-report=term-missing"
    
    # Test selection
    if args.unit:
        pytest_cmd += " -m 'not integration'"
    elif args.integration:
        pytest_cmd += " -m integration"
    elif args.fast:
        pytest_cmd += " -m 'not slow and not integration'"
    
    # Specific file
    if args.file:
        pytest_cmd += f" tests/{args.file}"
    
    print("🧪 Lünen Terminplaner Test Suite")
    print("=" * 60)
    
    # Check if pytest is available
    try:
        subprocess.run(["python", "-c", "import pytest"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pytest not found. Please install test dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the tests
    success = run_command(pytest_cmd, "Running Tests")
    
    if success:
        print("\n✅ All tests completed successfully!")
        
        if args.coverage:
            print("\n📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()