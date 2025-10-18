#!/usr/bin/env python3
"""
Command-line interface for void physics module.
"""

import argparse
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_tests():
    """Run the test suite."""
    logger.info("Running void physics tests...")

    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        return False


def run_math_test():
    """Run the math test script."""
    logger.info("Running math tests...")

    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "test_math.py"], capture_output=True, text=True
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run math tests: {e}")
        return False


def run_toy_model():
    """Run the toy model example."""
    logger.info("Running toy model...")

    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "examples/toy_model_0d.py"], capture_output=True, text=True
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run toy model: {e}")
        return False


def run_mypy():
    """Run mypy type checking."""
    logger.info("Running mypy type checking...")

    try:
        import subprocess

        result = subprocess.run(
            [sys.executable, "-m", "mypy", "src/void_physic/"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to run mypy: {e}")
        return False


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Void Physics CLI")
    parser.add_argument(
        "command", choices=["test", "math", "toy", "mypy", "all"], help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "test":
        success = run_tests()
    elif args.command == "math":
        success = run_math_test()
    elif args.command == "toy":
        success = run_toy_model()
    elif args.command == "mypy":
        success = run_mypy()
    elif args.command == "all":
        logger.info("Running all tests...")
        success = run_math_test() and run_tests() and run_mypy() and run_toy_model()

    if success:
        logger.info(" Command completed successfully")
        return 0
    else:
        logger.error(" Command failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
