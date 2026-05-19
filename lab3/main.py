#!/usr/bin/env python3
"""
N皇后算法比较 - 主程序

本程序实现并比较了解决N皇后问题的多种算法：
1. DFS寻找所有解
2. DFS寻找单个解
3. BestFS寻找所有解
4. BestFS寻找单个解
5. 优化的BestFS变种

程序包含全面的基准测试和性能分析。
"""

import sys
import time
from typing import List
from algorithms import (
    DFSAllSolver, DFSSingleSolver,
    BestFSAllSolver, BestFSSingleSolver,
    OptimizedBestFSAllSolver, OptimizedBestFSSingleSolver
)
from benchmark import BenchmarkSystem, print_detailed_comparison

def print_board(board: List[int], title: str = "解决方案"):
    """打印棋盘表示"""
    n = len(board)
    print(f"\n{title}:")
    print("  " + "+" + "---+" * n)

    for row in range(n):
        line = "  |"
        for col in range(n):
            if board[row] == col:
                line += " ♛ |"
            else:
                line += "   |"
        print(line)
        print("  " + "+" + "---+" * n)

def demonstrate_algorithms(n: int = 8):
    """在特定棋盘大小上演示所有算法"""
    print(f"\n{'='*60}")
    print(f"演示: {n}x{n} N皇后问题")
    print(f"{'='*60}")

    algorithms = {
        'DFS-All': DFSAllSolver,
        'DFS-Single': DFSSingleSolver,
        'BestFS-All': BestFSAllSolver,
        'BestFS-Single': BestFSSingleSolver,
        'Opt-BestFS-All': OptimizedBestFSAllSolver,
        'Opt-BestFS-Single': OptimizedBestFSSingleSolver,
    }

    results = {}

    for name, algo_class in algorithms.items():
        print(f"\n运行 {name}...")
        try:
            solver = algo_class(n)
            solutions = solver.solve()

            # Check if this is a list of solutions (multiple) or a single solution
            if name.endswith('Single'):
                # Single solution algorithms return individual board configurations
                solution_count = 1 if solutions else 0
                print(f"  时间: {solver.get_execution_time():.4f} seconds")
                print(f"  探索节点数: {solver.nodes_explored}")
                print(f"  找到解数: {solution_count}")

                # Show solution if found
                if solutions:
                    print_board(solutions, f"{name} - 解决方案")
            else:
                # All solution algorithms return lists of board configurations
                solution_count = len(solutions) if solutions else 0
                print(f"  时间: {solver.get_execution_time():.4f} seconds")
                print(f"  探索节点数: {solver.nodes_explored}")
                print(f"  找到解数: {solution_count}")

                # Show first solution if available
                if solutions and len(solutions) > 0:
                    print_board(solutions[0], f"{name} - 首个解决方案")

            results[name] = {
                'solutions': solutions,
                'time': solver.get_execution_time(),
                'nodes': solver.nodes_explored,
                'count': solution_count
            }

        except Exception as e:
            print(f"  Error: {e}")
            results[name] = {'error': str(e)}

    return results

def run_interactive_mode():
    """以交互模式运行，接受用户输入"""
    print("\nN皇后算法比较工具")
    print("================================")

    while True:
        try:
            print("\n选项:")
            print("1. 在特定棋盘大小上演示算法")
            print("2. 运行综合基准测试")
            print("3. 比较特定大小的算法")
            print("4. 退出")

            choice = input("\n请输入您的选择 (1-4): ").strip()

            if choice == '1':
                try:
                    n = int(input("输入棋盘大小 (4-12 recommended): "))
                    if n < 1:
                        print("Board size must be positive!")
                        continue
                    if n > 14:
                        confirm = input(f"警告: {n}x{n} may take very long. 继续? (y/n): ")
                        if confirm.lower() != 'y':
                            continue
                    demonstrate_algorithms(n)
                except ValueError:
                    print("请输入有效数字!")

            elif choice == '2':
                print("\n运行 综合基准测试...")
                benchmark = BenchmarkSystem()

                try:
                    sizes_input = input("输入棋盘大小s (comma-separated, or press Enter for default 4,6,8,10,12): ")
                    if sizes_input.strip():
                        board_sizes = [int(x.strip()) for x in sizes_input.split(',')]
                    else:
                        board_sizes = [4, 6, 8, 10, 12]

                    runs = input("Enter number of runs per algorithm (default 3): ")
                    runs_per_algorithm = int(runs) if runs.strip() else 3

                    print(f"\nBenchmarking algorithms on board sizes: {board_sizes}")
                    print(f"Runs per algorithm: {runs_per_algorithm}")
                    print("This may take several minutes...")

                    benchmark.run_comprehensive_benchmark(board_sizes, runs_per_algorithm)
                    report = benchmark.generate_performance_report()
                    print(f"\n{report}")

                    export = input("\nExport results to file? (y/n): ")
                    if export.lower() == 'y':
                        filename = input("Enter filename (default: benchmark_results.txt): ")
                        filename = filename if filename.strip() else "benchmark_results.txt"
                        benchmark.export_results(filename)

                except ValueError as e:
                    print(f"Invalid input: {e}")
                except KeyboardInterrupt:
                    print("\nBenchmark interrupted.")

            elif choice == '3':
                try:
                    n = int(input("输入棋盘大小 to compare: "))
                    if n < 1:
                        print("Board size must be positive!")
                        continue

                    print(f"\nComparing algorithms for {n}x{n} board...")
                    benchmark = BenchmarkSystem()
                    comparison = benchmark.compare_algorithms(n)
                    print_detailed_comparison(comparison)

                except ValueError:
                    print("请输入有效数字!")

            elif choice == '4':
                print("Goodbye!")
                break

            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")

def run_quick_demo():
    """Run a quick demonstration of all algorithms"""
    print("\n" + "="*60)
    print("QUICK DEMONSTRATION - 8x8 N-Queens Problem")
    print("="*60)

    # Test on smaller board for quick results
    demonstrate_algorithms(8)

def run_automated_test():
    """Run automated tests to verify algorithm correctness"""
    print("\n" + "="*60)
    print("AUTOMATED CORRECTNESS TESTS")
    print("="*60)

    test_sizes = [4, 6, 8]
    algorithms = {
        'DFS-All': DFSAllSolver,
        'BestFS-All': BestFSAllSolver,
        'Opt-BestFS-All': OptimizedBestFSAllSolver,
    }

    all_passed = True

    for n in test_sizes:
        print(f"\nTesting {n}x{n} board:")
        expected_solutions = {
            4: 2,
            6: 4,
            8: 92
        }

        for name, algo_class in algorithms.items():
            try:
                solver = algo_class(n)
                solutions = solver.solve()
                solution_count = len(solutions) if solutions else 0
                expected = expected_solutions.get(n, 0)

                if solution_count == expected:
                    print(f"  ✓ {name}: {solution_count} solutions (correct)")
                else:
                    print(f"  ✗ {name}: {solution_count} solutions (expected {expected})")
                    all_passed = False

                # Verify solution validity
                if solutions:
                    for i, solution in enumerate(solutions[:3]):  # Check first 3 solutions
                        if not is_valid_solution(solution):
                            print(f"  ✗ {name}: Invalid solution detected")
                            all_passed = False
                            break

            except Exception as e:
                print(f"  ✗ {name}: Error - {e}")
                all_passed = False

    if all_passed:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")

    return all_passed

def is_valid_solution(board: List[int]) -> bool:
    """Check if a solution is valid"""
    n = len(board)

    # Check if all queens are placed
    if len([x for x in board if x != -1]) != n:
        return False

    # Check for conflicts
    for i in range(n):
        for j in range(i + 1, n):
            # Same column
            if board[i] == board[j]:
                return False
            # Same diagonal
            if abs(board[i] - board[j]) == abs(i - j):
                return False

    return True

def main():
    """Main function with command line interface"""
    print("N-Queens Algorithm Comparison System")
    print("====================================")

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'demo':
            size = int(sys.argv[2]) if len(sys.argv) > 2 else 8
            demonstrate_algorithms(size)
        elif command == 'test':
            run_automated_test()
        elif command == 'quick':
            run_quick_demo()
        elif command == 'benchmark':
            sizes = [4, 6, 8, 10]
            if len(sys.argv) > 2:
                sizes = [int(x) for x in sys.argv[2].split(',')]

            benchmark = BenchmarkSystem()
            benchmark.run_comprehensive_benchmark(sizes, runs_per_algorithm=2)
            report = benchmark.generate_performance_report()
            print(f"\n{report}")
            benchmark.export_results()
        else:
            print("Usage: python main.py [demo|test|quick|benchmark] [args...]")
            print("  demo [size]     - Run demonstration (default size: 8)")
            print("  test            - Run correctness tests")
            print("  quick           - Quick demonstration")
            print("  benchmark [sizes] - Run benchmark (default: 4,6,8,10)")
    else:
        # Interactive mode
        run_interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)