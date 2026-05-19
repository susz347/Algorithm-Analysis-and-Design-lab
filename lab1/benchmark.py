#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法性能测试和比较程序
测试不同数据场景下的算法效率
"""

import random
import time
from typing import List, Dict, Tuple
from sort_algorithms import SortAlgorithms

# 尝试导入可选依赖
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # 提供简单的替代实现
    class np:
        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0

        @staticmethod
        def std(data):
            if not data:
                return 0
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val) ** 2 for x in data) / len(data)
            return variance ** 0.5


class Benchmark:
    """性能测试类"""

    def __init__(self):
        self.results = {}
        self.test_cases = {
            '随机数据': self._generate_random_data,
            '已排序数据': self._generate_sorted_data,
            '逆序数据': self._generate_reverse_sorted_data,
            '部分有序': self._generate_partially_sorted_data,
            '重复数据': self._generate_duplicate_data
        }

    def _generate_random_data(self, size: int) -> List[int]:
        """生成随机数据"""
        return [random.randint(1, size) for _ in range(size)]

    def _generate_sorted_data(self, size: int) -> List[int]:
        """生成已排序数据"""
        return list(range(1, size + 1))

    def _generate_reverse_sorted_data(self, size: int) -> List[int]:
        """生成逆序数据"""
        return list(range(size, 0, -1))

    def _generate_partially_sorted_data(self, size: int) -> List[int]:
        """生成部分有序数据"""
        arr = list(range(1, size + 1))
        # 随机交换10%的元素
        swaps = size // 10
        for _ in range(swaps):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def _generate_duplicate_data(self, size: int) -> List[int]:
        """生成包含重复元素的数据"""
        return [random.randint(1, size//10) for _ in range(size)]

    def run_single_test(self, algorithm_func, data: List[int], name: str) -> float:
        """运行单次测试"""
        start_time = time.perf_counter()
        result = algorithm_func(data.copy())
        end_time = time.perf_counter()

        # 验证结果
        is_correct = all(result[i] <= result[i+1] for i in range(len(result)-1))
        if not is_correct:
            raise ValueError(f"{name} 排序结果错误!")

        return (end_time - start_time) * 1000  # 转换为毫秒

    def run_benchmark(self, sizes: List[int] = None, iterations: int = 5):
        """运行完整的性能测试"""
        if sizes is None:
            sizes = [100, 500, 1000, 2000, 5000]

        algorithms = [
            (SortAlgorithms.merge_sort, "归并排序(递归)"),
            (SortAlgorithms.merge_sort_iterative, "归并排序(迭代)"),
            (SortAlgorithms.quick_sort, "快速排序(递归)"),
            (SortAlgorithms.quick_sort_iterative, "快速排序(迭代)"),
            (SortAlgorithms.heap_sort, "堆排序")
        ]

        print("开始性能测试...")
        print("=" * 80)

        for case_name, data_generator in self.test_cases.items():
            print(f"\n测试场景: {case_name}")
            print("-" * 50)

            self.results[case_name] = {}

            for size in sizes:
                print(f"\n数据规模: {size}")

                # 生成测试数据
                test_data = data_generator(size)

                for algorithm_func, algo_name in algorithms:
                    times = []

                    # 多次运行取平均值
                    for _ in range(iterations):
                        try:
                            elapsed_time = self.run_single_test(algorithm_func, test_data, algo_name)
                            times.append(elapsed_time)
                        except Exception as e:
                            print(f"  {algo_name}: 错误 - {e}")
                            continue

                    if times:
                        avg_time = np.mean(times)
                        std_time = np.std(times)

                        if algo_name not in self.results[case_name]:
                            self.results[case_name][algo_name] = {}

                        self.results[case_name][algo_name][size] = {
                            'avg_time': avg_time,
                            'std_time': std_time
                        }

                        print(f"  {algo_name}: {avg_time:.2f}ms ± {std_time:.2f}ms")

    def print_results_table(self):
        """打印结果表格"""
        print("\n" + "=" * 80)
        print("性能测试结果汇总")
        print("=" * 80)

        for case_name, case_results in self.results.items():
            print(f"\n测试场景: {case_name}")
            print("-" * 50)

            # 获取所有算法和规模
            algorithms = list(case_results.keys())
            if not algorithms:
                continue

            sizes = sorted(case_results[algorithms[0]].keys())

            # 打印表头
            header = "算法名称".ljust(20)
            for size in sizes:
                header += f"{size}个元素".ljust(12)
            print(header)
            print("-" * len(header))

            # 打印每行数据
            for algo_name in algorithms:
                row = algo_name.ljust(20)
                for size in sizes:
                    if size in case_results[algo_name]:
                        avg_time = case_results[algo_name][size]['avg_time']
                        row += f"{avg_time:.1f}ms".ljust(12)
                    else:
                        row += "N/A".ljust(12)
                print(row)

    def plot_results(self):
        """绘制性能比较图表"""
        if not HAS_MATPLOTLIB:
            print("\n未安装matplotlib，无法生成图表")
            print("可以使用以下命令安装: pip install matplotlib")
            return

        try:
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False

            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle('排序算法性能比较', fontsize=16)

            case_names = list(self.test_cases.keys())

            for idx, case_name in enumerate(case_names):
                if case_name not in self.results:
                    continue

                row = idx // 3
                col = idx % 3
                ax = axes[row, col]

                case_results = self.results[case_name]
                algorithms = list(case_results.keys())

                if not algorithms:
                    continue

                sizes = sorted(case_results[algorithms[0]].keys())

                for algo_name in algorithms:
                    times = []
                    for size in sizes:
                        if size in case_results[algo_name]:
                            times.append(case_results[algo_name][size]['avg_time'])
                        else:
                            times.append(0)

                    ax.plot(sizes, times, marker='o', label=algo_name, linewidth=2)

                ax.set_title(case_name)
                ax.set_xlabel('数据规模')
                ax.set_ylabel('耗时 (ms)')
                ax.legend()
                ax.grid(True, alpha=0.3)

            # 隐藏多余的子图
            for idx in range(len(case_names), 6):
                row = idx // 3
                col = idx % 3
                axes[row, col].set_visible(False)

            plt.tight_layout()
            plt.savefig('sort_performance_comparison.png', dpi=300, bbox_inches='tight')
            print("\n性能图表已保存为: sort_performance_comparison.png")

        except Exception as e:
            print(f"\n生成图表时出错: {e}")
            print("请确保已安装matplotlib: pip install matplotlib")

    def analyze_results(self):
        """分析测试结果"""
        print("\n" + "=" * 80)
        print("性能分析")
        print("=" * 80)

        for case_name, case_results in self.results.items():
            print(f"\n场景: {case_name}")
            print("-" * 30)

            if not case_results:
                continue

            # 找出每个规模下的最快算法
            sizes = sorted(next(iter(case_results.values())).keys())

            for size in sizes:
                fastest_time = float('inf')
                fastest_algo = ""

                for algo_name, size_results in case_results.items():
                    if size in size_results:
                        time_taken = size_results[size]['avg_time']
                        if time_taken < fastest_time:
                            fastest_time = time_taken
                            fastest_algo = algo_name

                if fastest_algo:
                    print(f"  {size}个元素: {fastest_algo} 最快 ({fastest_time:.2f}ms)")


def main():
    """主函数"""
    benchmark = Benchmark()

    # 运行性能测试
    sizes = [100, 500, 1000, 2000]
    benchmark.run_benchmark(sizes=sizes, iterations=3)

    # 打印结果
    benchmark.print_results_table()

    # 分析结果
    benchmark.analyze_results()

    # 绘制图表
    benchmark.plot_results()

    print("\n性能测试完成!")


if __name__ == "__main__":
    main()