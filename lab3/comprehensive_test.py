import time
import statistics
from typing import Dict, List, Tuple, Callable
from n_queens_solver import NQueensSolver
from advanced_n_queens import AdvancedNQueensSolver


class ComprehensiveTest:
    """全面的N皇后问题算法性能测试"""

    def __init__(self, n_values: List[int], iterations: int = 3):
        self.n_values = n_values
        self.iterations = iterations
        self.results = {}

        # 定义所有要测试的算法
        self.algorithms = {
            # 基础算法
            "DFS - 所有解": lambda s: s.dfs_all_solutions(),
            "DFS - 一个解": lambda s: s.dfs_one_solution(),
            "BestFS - 所有解": lambda s: s.bestfs_all_solutions(),
            "BestFS - 一个解": lambda s: s.bestfs_one_solution(),

            # 增强算法
            "最小攻击启发式 - 所有解": lambda s: s.bestfs_attack_heuristic_all(),
            "最小攻击启发式 - 一个解": lambda s: s.bestfs_attack_heuristic_one(),
            "前向检查启发式 - 所有解": lambda s: s.bestfs_forward_checking_all(),
            "前向检查启发式 - 一个解": lambda s: s.bestfs_forward_checking_one(),
            "中心优先启发式 - 所有解": lambda s: s.bestfs_center_preference_all(),
            "中心优先启发式 - 一个解": lambda s: s.bestfs_center_preference_one(),
            "MRV启发式 - 所有解": lambda s: s.backtracking_with_mrv_all(),
            "MRV启发式 - 一个解": lambda s: s.backtracking_with_mrv_one(),
        }

    def time_algorithm(self, solver, algorithm_func: Callable, algo_name: str) -> Dict:
        """测试特定算法的执行时间"""
        times = []
        solution_counts = []

        for _ in range(self.iterations):
            start_time = time.time()

            try:
                result = algorithm_func(solver)

                # 计算解的数量
                if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                    # 多个解的情况
                    solution_counts.append(len(result))
                elif result is not None:
                    # 单个解的情况
                    solution_counts.append(1)
                else:
                    solution_counts.append(0)

                end_time = time.time()
                times.append(end_time - start_time)

            except Exception as e:
                print(f"    算法执行错误: {e}")
                return {'error': str(e)}

        if not times:
            return {'error': 'No successful runs'}

        return {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_time': statistics.stdev(times) if len(times) > 1 else 0,
            'avg_solutions': statistics.mean(solution_counts),
            'total_iterations': self.iterations
        }

    def run_test_for_n(self, n: int):
        """对指定的N值运行所有算法测试"""
        print(f"\n{'='*60}")
        print(f"测试 N = {n}")
        print(f"{'='*60}")

        # 创建求解器
        basic_solver = NQueensSolver(n)
        advanced_solver = AdvancedNQueensSolver(n)

        n_results = {}

        for algo_name, algo_func in self.algorithms.items():
            print(f"\n测试: {algo_name}")
            print("-" * 40)

            # 选择合适的求解器
            solver = advanced_solver if "启发式" in algo_name or "MRV" in algo_name else basic_solver

            result = self.time_algorithm(solver, algo_func, algo_name)
            n_results[algo_name] = result

            if 'error' in result:
                print(f"  错误: {result['error']}")
            else:
                print(f"  平均时间: {result['avg_time']:.6f} 秒")
                print(f"  最短时间: {result['min_time']:.6f} 秒")
                print(f"  最长时间: {result['max_time']:.6f} 秒")
                print(f"  标准差: {result['std_time']:.6f} 秒")
                print(f"  解的数量: {result['avg_solutions']:.1f}")

        return n_results

    def run_comprehensive_test(self):
        """运行全面的性能测试"""
        print("N皇后问题算法大比拼 - 全面性能测试")
        print("=" * 80)

        for n in self.n_values:
            n_results = self.run_test_for_n(n)
            self.results[n] = n_results

    def print_comparison_tables(self):
        """打印算法比较表格"""
        print("\n" + "=" * 100)
        print("算法性能对比汇总")
        print("=" * 100)

        for n in self.n_values:
            if n not in self.results:
                continue

            print(f"\nN = {n}")
            print("-" * 100)

            # 分组显示：求一个解和求所有解
            one_solution_algos = [(k, v) for k, v in self.results[n].items()
                                if "一个解" in k and 'error' not in v]
            all_solution_algos = [(k, v) for k, v in self.results[n].items()
                                if "所有解" in k and 'error' not in v]

            print("\n求一个解的算法:")
            print(f"{'算法名称':<25} {'平均时间(秒)':<15} {'解的数量':<10}")
            print("-" * 50)
            for algo_name, result in sorted(one_solution_algos, key=lambda x: x[1]['avg_time']):
                print(f"{algo_name:<25} {result['avg_time']:<15.6f} {result['avg_solutions']:<10.1f}")

            print("\n求所有解的算法:")
            print(f"{'算法名称':<25} {'平均时间(秒)':<15} {'解的数量':<10}")
            print("-" * 50)
            for algo_name, result in sorted(all_solution_algos, key=lambda x: x[1]['avg_time']):
                print(f"{algo_name:<25} {result['avg_time']:<15.6f} {result['avg_solutions']:<10.1f}")

    def analyze_algorithm_categories(self):
        """分析不同类别算法的性能差异"""
        print("\n" + "=" * 100)
        print("算法类别性能分析")
        print("=" * 100)

        for n in self.n_values:
            if n not in self.results:
                continue

            results = self.results[n]
            print(f"\nN = {n} 时的算法类别比较:")

            # 定义算法类别
            categories = {
                "基础DFS": [k for k in results.keys() if k.startswith("DFS") and 'error' not in results[k]],
                "基础BestFS": [k for k in results.keys() if k.startswith("BestFS") and 'error' not in results[k]],
                "启发式算法": [k for k in results.keys() if "启发式" in k and 'error' not in results[k]],
                "MRV算法": [k for k in results.keys() if "MRV" in k and 'error' not in results[k]]
            }

            for category, algos in categories.items():
                if not algos:
                    continue

                avg_times = []
                for algo in algos:
                    if 'error' not in results[algo]:
                        avg_times.append(results[algo]['avg_time'])

                if avg_times:
                    avg_time = statistics.mean(avg_times)
                    print(f"  {category}: 平均时间 {avg_time:.6f} 秒 ({len(algos)} 个算法)")

    def find_best_algorithms(self):
        """找出每个场景下的最佳算法"""
        print("\n" + "=" * 100)
        print("最佳算法推荐")
        print("=" * 100)

        for n in self.n_values:
            if n not in self.results:
                continue

            results = self.results[n]
            print(f"\nN = {n}:")

            # 求一个解的最佳算法
            one_solution_algos = {k: v for k, v in results.items()
                                if "一个解" in k and 'error' not in v}
            if one_solution_algos:
                best_one = min(one_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                print(f"  求一个解的最佳算法: {best_one[0]}")
                print(f"    平均时间: {best_one[1]['avg_time']:.6f} 秒")

            # 求所有解的最佳算法
            all_solution_algos = {k: v for k, v in results.items()
                                if "所有解" in k and 'error' not in v}
            if all_solution_algos:
                best_all = min(all_solution_algos.items(), key=lambda x: x[1]['avg_time'])
                print(f"  求所有解的最佳算法: {best_all[0]}")
                print(f"    平均时间: {best_all[1]['avg_time']:.6f} 秒")


if __name__ == "__main__":
    # 运行全面测试
    n_values = [4, 6, 8, 10]  # 测试的N值
    test = ComprehensiveTest(n_values, iterations=3)

    test.run_comprehensive_test()
    test.print_comparison_tables()
    test.analyze_algorithm_categories()
    test.find_best_algorithms()