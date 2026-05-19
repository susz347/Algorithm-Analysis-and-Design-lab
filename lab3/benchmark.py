import time
import statistics
import psutil
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from algorithms import (
    DFSAllSolver, DFSSingleSolver,
    BestFSAllSolver, BestFSSingleSolver,
    OptimizedBestFSAllSolver, OptimizedBestFSSingleSolver
)

@dataclass
class BenchmarkResult:
    """Results from benchmarking an algorithm"""
    algorithm_name: str
    board_size: int
    execution_time: float
    solutions_found: int
    nodes_explored: int
    memory_usage_mb: float
    success: bool

class BenchmarkSystem:
    """System for benchmarking N-Queens algorithms"""

    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.algorithms = {
            'DFS-All': DFSAllSolver,
            'DFS-Single': DFSSingleSolver,
            'BestFS-All': BestFSAllSolver,
            'BestFS-Single': BestFSSingleSolver,
            'Opt-BestFS-All': OptimizedBestFSAllSolver,
            'Opt-BestFS-Single': OptimizedBestFSSingleSolver,
        }

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def benchmark_algorithm(self, algorithm_class, n: int, runs: int = 1) -> BenchmarkResult:
        """Benchmark a single algorithm on board size n"""
        algorithm_name = algorithm_class.__name__.replace('Solver', '')
        execution_times = []
        nodes_counts = []
        memory_usages = []
        solutions_counts = []
        success = True

        print(f"  Running {algorithm_name} on {n}x{n} board...")

        for run in range(runs):
            try:
                # Memory measurement
                initial_memory = self.get_memory_usage()

                # Create and run solver
                solver = algorithm_class(n)
                solutions = solver.solve()

                final_memory = self.get_memory_usage()
                memory_used = final_memory - initial_memory

                execution_times.append(solver.get_execution_time())
                nodes_counts.append(solver.nodes_explored)
                memory_usages.append(max(memory_used, 0.1))  # Minimum 0.1 MB
                solutions_counts.append(len(solver.solutions))

            except Exception as e:
                print(f"    Error in run {run + 1}: {e}")
                success = False
                break

        if not success or not execution_times:
            return BenchmarkResult(
                algorithm_name=algorithm_name,
                board_size=n,
                execution_time=float('inf'),
                solutions_found=0,
                nodes_explored=0,
                memory_usage_mb=0,
                success=False
            )

        # Calculate averages
        avg_time = statistics.mean(execution_times)
        avg_nodes = statistics.mean(nodes_counts)
        avg_memory = statistics.mean(memory_usages)
        avg_solutions = statistics.mean(solutions_counts)

        result = BenchmarkResult(
            algorithm_name=algorithm_name,
            board_size=n,
            execution_time=avg_time,
            solutions_found=int(avg_solutions),
            nodes_explored=int(avg_nodes),
            memory_usage_mb=avg_memory,
            success=True
        )

        return result

    def run_comprehensive_benchmark(self, board_sizes: List[int] = None, runs_per_algorithm: int = 3):
        """Run comprehensive benchmark across multiple board sizes and algorithms"""
        if board_sizes is None:
            board_sizes = [4, 6, 8, 10, 12]

        print("=" * 60)
        print("N-QUEENS ALGORITHM BENCHMARK")
        print("=" * 60)

        for n in board_sizes:
            print(f"\nTesting board size: {n}x{n}")
            print("-" * 40)

            for algo_name, algo_class in self.algorithms.items():
                result = self.benchmark_algorithm(algo_class, n, runs_per_algorithm)
                self.results.append(result)

                if result.success:
                    print(f"  {algo_name:15} | "
                          f"Time: {result.execution_time:8.4f}s | "
                          f"Solutions: {result.solutions_found:3d} | "
                          f"Nodes: {result.nodes_explored:6d} | "
                          f"Memory: {result.memory_usage_mb:6.2f}MB")
                else:
                    print(f"  {algo_name:15} | FAILED")

    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance report"""
        if not self.results:
            return "No benchmark results available."

        report = []
        report.append("=" * 80)
        report.append("N-QUEENS ALGORITHM PERFORMANCE REPORT")
        report.append("=" * 80)

        # Group results by board size
        by_board_size = {}
        for result in self.results:
            if result.board_size not in by_board_size:
                by_board_size[result.board_size] = []
            by_board_size[result.board_size].append(result)

        for board_size in sorted(by_board_size.keys()):
            results = by_board_size[board_size]
            report.append(f"\nBoard Size: {board_size}x{board_size}")
            report.append("-" * 50)

            # Sort by execution time
            successful_results = [r for r in results if r.success]
            successful_results.sort(key=lambda x: x.execution_time)

            report.append(f"{'Algorithm':<20} {'Time(s)':<10} {'Solutions':<10} {'Nodes':<10} {'Memory(MB)':<12} {'Rank'}")
            report.append("-" * 65)

            for i, result in enumerate(successful_results, 1):
                report.append(
                    f"{result.algorithm_name:<20} "
                    f"{result.execution_time:<10.4f} "
                    f"{result.solutions_found:<10} "
                    f"{result.nodes_explored:<10} "
                    f"{result.memory_usage_mb:<12.2f} "
                    f"#{i}"
                )

        # Overall statistics
        report.append(f"\n{'='*80}")
        report.append("OVERALL PERFORMANCE ANALYSIS")
        report.append(f"{'='*80}")

        # Calculate algorithm rankings
        algorithm_stats = {}
        for result in self.results:
            if not result.success:
                continue

            if result.algorithm_name not in algorithm_stats:
                algorithm_stats[result.algorithm_name] = {
                    'total_time': 0,
                    'total_nodes': 0,
                    'total_memory': 0,
                    'wins': 0,
                    'tests': 0
                }

            stats = algorithm_stats[result.algorithm_name]
            stats['total_time'] += result.execution_time
            stats['total_nodes'] += result.nodes_explored
            stats['total_memory'] += result.memory_usage_mb
            stats['tests'] += 1

        # Find winners for each board size
        for board_size in by_board_size:
            results = [r for r in by_board_size[board_size] if r.success]
            if results:
                fastest = min(results, key=lambda x: x.execution_time)
                algorithm_stats[fastest.algorithm_name]['wins'] += 1

        # Sort algorithms by wins
        sorted_algorithms = sorted(algorithm_stats.items(), key=lambda x: x[1]['wins'], reverse=True)

        report.append("\nAlgorithm Rankings (by number of wins):")
        report.append("-" * 50)
        for i, (algo_name, stats) in enumerate(sorted_algorithms, 1):
            avg_time = stats['total_time'] / stats['tests']
            avg_nodes = stats['total_nodes'] / stats['tests']
            avg_memory = stats['total_memory'] / stats['tests']

            report.append(
                f"{i:2d}. {algo_name:<15} | "
                f"Wins: {stats['wins']:2d} | "
                f"Avg Time: {avg_time:.4f}s | "
                f"Avg Nodes: {avg_nodes:.0f} | "
                f"Avg Memory: {avg_memory:.2f}MB"
            )

        return "\n".join(report)

    def export_results(self, filename: str = "benchmark_results.txt"):
        """Export benchmark results to file"""
        report = self.generate_performance_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Results exported to {filename}")

    def compare_algorithms(self, n: int) -> Dict:
        """Compare all algorithms for a specific board size"""
        comparison = {
            'board_size': n,
            'algorithms': {},
            'summary': {}
        }

        for algo_name, algo_class in self.algorithms.items():
            result = self.benchmark_algorithm(algo_class, n, runs=1)
            comparison['algorithms'][algo_name] = {
                'time': result.execution_time,
                'solutions': result.solutions_found,
                'nodes': result.nodes_explored,
                'memory': result.memory_usage_mb,
                'success': result.success
            }

        # Find best performers
        successful_results = [
            (name, data) for name, data in comparison['algorithms'].items()
            if data['success']
        ]

        if successful_results:
            fastest = min(successful_results, key=lambda x: x[1]['time'])
            most_efficient = min(successful_results, key=lambda x: x[1]['nodes'])
            least_memory = min(successful_results, key=lambda x: x[1]['memory'])

            comparison['summary'] = {
                'fastest': fastest[0],
                'most_efficient': most_efficient[0],
                'least_memory': least_memory[0]
            }

        return comparison

def print_detailed_comparison(comparison: Dict):
    """Print detailed algorithm comparison"""
    n = comparison['board_size']
    print(f"\nDetailed Comparison for {n}x{n} board:")
    print("=" * 60)

    algorithms = comparison['algorithms']
    for algo_name, data in algorithms.items():
        if data['success']:
            print(f"\n{algo_name}:")
            print(f"  Execution Time: {data['time']:.6f} seconds")
            print(f"  Solutions Found: {data['solutions']}")
            print(f"  Nodes Explored: {data['nodes']}")
            print(f"  Memory Usage: {data['memory']:.2f} MB")
        else:
            print(f"\n{algo_name}: FAILED")

    if 'summary' in comparison:
        summary = comparison['summary']
        print(f"\nSummary:")
        print(f"  Fastest: {summary.get('fastest', 'N/A')}")
        print(f"  Most Efficient: {summary.get('most_efficient', 'N/A')}")
        print(f"  Least Memory: {summary.get('least_memory', 'N/A')}")