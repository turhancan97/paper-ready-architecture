#!/usr/bin/env python3
"""
Test runner for Neural Network Architecture Visualizer
"""

import sys
import os
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Run all test suites."""
    print("🧪 Running Neural Network Visualizer Test Suite")
    print("=" * 50)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

def run_specific_test(test_name):
    """Run a specific test module."""
    print(f"🧪 Running {test_name}")
    print("=" * 30)
    
    suite = unittest.TestLoader().loadTestsFromName(test_name)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        if not test_name.startswith('test_'):
            test_name = f'test_{test_name}'
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code) 