#!/usr/bin/env python3
"""
Test runner for SpendSense application
Runs all unit and integration tests
"""
import unittest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def run_all_tests(verbosity=2):
    """
    Discover and run all tests in the tests directory
    
    Args:
        verbosity (int): Test output verbosity (0=quiet, 1=normal, 2=verbose)
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Discover all tests in tests directory
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed.")
        return False


def run_specific_test(test_file, verbosity=2):
    """
    Run a specific test file
    
    Args:
        test_file (str): Name of the test file (e.g., 'test_transaction_model.py')
        verbosity (int): Test output verbosity
    
    Returns:
        bool: True if tests passed, False otherwise
    """
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / 'tests'
    suite = loader.discover(start_dir, pattern=test_file)
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run SpendSense tests')
    parser.add_argument(
        '--file',
        type=str,
        help='Run specific test file (e.g., test_transaction_model.py)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    
    args = parser.parse_args()
    
    # Determine verbosity
    verbosity = 2
    if args.verbose:
        verbosity = 2
    elif args.quiet:
        verbosity = 0
    
    # Run tests
    if args.file:
        success = run_specific_test(args.file, verbosity)
    else:
        success = run_all_tests(verbosity)
    
    sys.exit(0 if success else 1)
