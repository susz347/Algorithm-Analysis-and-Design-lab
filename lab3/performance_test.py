import time
import statistics
from typing import Dict, List, Tuple
from n_queens_solver import NQueensSolver


class PerformanceTest:
    """N皇后问题算法性能测试类"""

    def __init__(self, n_values: List[int], iterations: int = 5):
        self.n_values = n_values
        self.iterations = iterations
        self.results = {}

    def time_algorithm(self, solver: NQueensSolver, algorithm_name: str,
                      all_solutions: bool = True) -> Dict[str, float]:
        """测试特定算法的执行时间"""
        times = []
        solution_counts = []

        for _ in range(self.iterations):
            start_time = time.time()

            if algorithm_name == "dfs":
                if all_solutions:
                    solutions = solver.dfs_all_solutions()
                    solution_counts.append(len(solutions))
                else:
                    solution = solver.dfs_one_solution()
                    solution_counts.append(1 if solution else 0)
            elif algorithm_name == "bestfs":
                if all_solutions:
                    solutions = solver.bestfs_all_solutions()
                    solution_counts.append(len(solutions))
                else:
                    solution = solver.bestfs_one_solution()
                    solution_counts.append(1 if solution else 0)

            end_time = time.time()
            times.append(end_time - start_time)

        return {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_time': statistics.stdev(times) if len(times) > 1 else 0,
            'avg_solutions': statistics.mean(solution_counts),
            'total_iterations': self.iterations
        }

    def run_comprehensive_test(self):
        """运行全面的性能测试"""
        print("=" * 80)
        print("N皇后问题算法性能对比测试")
        print("=" * 80)

        for n in self.n_values:
            print(f"\n测试 N = {n}")
            print("-" * 50)

            solver = NQueensSolver(n)
            n_results = {}

            # 测试所有算法
            algorithms = [
                ("dfs", True, "DFS - 所有解"),
                ("dfs", False, "DFS - 一个解"),
                ("bestfs", True, "BestFS - 所有解"),
                ("bestfs", False, "BestFS - 一个解")
            ]

            for algo_name, all_sols, display_name in algorithms:
                print(f"正在测试: {display_name}")
                try:
                    result = self.time_algorithm(solver, algo_name, all_sols)
                    n_results[display_name] = result

                    print(f"  平均时间: {result['avg_time']:.6f} 秒")
                    print(f"  最短时间: {result['min_time']:.6f} 秒")
                    print(f"  最长时间: {result['max_time']:.6f} 秒")
                    print(f"  标准差: {result['std_time']:.6f} 秒")
                    print(f"  解的数量: {result['avg_solutions']:.1f}")

                except Exception as e:
                    print(f"  错误: {e}")
                    n_results[display_name] = {'error': str(e)}

            self.results[n] = n_results

    def print_summary_table(self):
        """打印结果汇总表格"""
        print("\n" + "=" * 80)
        print("性能对比汇总表")
        print("=" * 80)

        for n in self.n_values:
            if n not in self.results:
                continue

            print(f"\nN = {n}")
            print("-" * 60)
            print(f"{'算法':<20} {'平均时间(秒)':<15} {'解的数量':<10}")
            print("-" * 60)

            results = self.results[n]
            for algo_name, result in results.items():
                if 'error' in result:
                    print(f"{algo_name:<20} {'错误':<15} {result['error']:<10}")
                else:
                    print(f"{algo_name:<20} {result['avg_time']:<15.6f} {result['avg_solutions']:<10.1f}")

    def analyze_algorithm_efficiency(self):
        """分析算法效率差异"""
        print("\n" + "=" * 80)
        print("算法效率分析")
        print("=" * 80)

        for n in self.n_values:
            if n not in self.results:
                continue

            results = self.results[n]
            print(f"\nN = {n} 时各算法比较:")

            # 比较求一个解的效率
            one_solution_algos = {k: v for k, v in results.items()
                                if "一个解" in k and 'error' not in v}
            if len(one_solution_algos) >= 2:
                fastest = min(one_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                slowest = max(one_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                speedup = slowest[1]['avg_time'] / fastest[1]['avg_time']
                print(f"  求一个解: {fastest[0]} 比 {slowest[0]} 快 {speedup:.2f} 倍")

            # 比较求所有解的效率
            all_solution_algos = {k: v for k, v in results.items()
                                if "所有解" in k and 'error' not in v}
            if len(all_solution_algos) >= 2:
                fastest = min(all_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                slowest = max(all_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                speedup = slowest[1]['avg_time'] / fastest[1]['avg_time']
                print(f"  求所有解: {fastest[0]} 比 {slowest[0]} 快 {speedup:.2f} 倍")


if __name__ == "__main__":
    # 运行性能测试
    n_values = [4, 6, 8, 10]  # 可以根据需要调整
    test = PerformanceTest(n_values, iterations=3)

    test.run_comprehensive_test()
    test.print_summary_table()
    test.analyze_algorithm_efficiency()