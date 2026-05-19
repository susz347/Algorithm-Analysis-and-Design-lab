#!/usr/bin/env python3
"""
Simple test script for N-Queens algorithms
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms import (
    DFSAllSolver, DFSSingleSolver,
    BestFSAllSolver, BestFSSingleSolver
)

def test_small_boards():
    """Test algorithms on small board sizes"""
    print("Testing N-Queens algorithms on small boards...")

    # Test cases: (board_size, expected_solutions)
    test_cases = [
        (4, 2),
        (6, 4),
        (8, 92)
    ]

    algorithms = [
        ('DFS-All', DFSAllSolver),
        ('DFS-Single', DFSSingleSolver),
        ('BestFS-All', BestFSAllSolver),
        ('BestFS-Single', BestFSSingleSolver)
    ]

    all_passed = True

    for n, expected in test_cases:
        print(f"\nTesting {n}x{n} board (expected: {expected} solutions):")

        for algo_name, algo_class in algorithms:
            try:
                solver = algo_class(n)
                solutions = solver.solve()

                if algo_name.endswith('Single'):
                    # Single solvers should find exactly 1 solution
                    actual = 1 if solutions else 0
                    test_expected = 1
                else:
                    # All solvers should find all solutions
                    actual = len(solutions) if solutions else 0
                    test_expected = expected

                if actual == test_expected:
                    print(f"  PASS {algo_name}: {actual} solutions found")
                else:
                    print(f"  FAIL {algo_name}: {actual} solutions (expected {test_expected})")
                    all_passed = False

                print(f"    Time: {solver.get_execution_time():.4f}s, Nodes: {solver.nodes_explored}")

            except Exception as e:
                print(f"  FAIL {algo_name}: Error - {e}")
                all_passed = False

    return all_passed

def test_solution_validity():
    """Test that found solutions are actually valid"""
    print("\nTesting solution validity...")

    def is_valid(board):
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                # Check column conflicts
                if board[i] == board[j]:
                    return False
                # Check diagonal conflicts
                if abs(board[i] - board[j]) == abs(i - j):
                    return False
        return True

    solver = DFSAllSolver(8)
    solutions = solver.solve()

    valid_count = 0
    for i, solution in enumerate(solutions[:10]):  # Test first 10 solutions
        if is_valid(solution):
            valid_count += 1
        else:
            print(f"  ✗ Solution {i+1} is invalid: {solution}")

    print(f"  Valid solutions: {valid_count}/{min(10, len(solutions))}")
    return valid_count == min(10, len(solutions))

def main():
    """Run all tests"""
    print("N-Queens Algorithm Test Suite")
    print("=" * 40)

    test1_passed = test_small_boards()
    test2_passed = test_solution_validity()

    print(f"\n{'='*40}")
    if test1_passed and test2_passed:
        print("PASS All tests passed!")
        return 0
    else:
        print("FAIL Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())