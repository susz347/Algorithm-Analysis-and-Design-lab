#!/usr/bin/env python3
"""
Comprehensive benchmark runner for 0/1 Knapsack algorithms.

This module provides a complete testing framework to compare the performance
of different knapsack algorithms across various datasets and scenarios.
"""

import time
import json
import csv
import random
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from knapsack_algorithms import (
    KnapsackBenchmark, KnapsackItem,
    GreedyKnapsackSolver, RecursiveDPKnapsackSolver,
    IterativeDPKnapsackSolver, BacktrackingKnapsackSolver
)
from real_world_datasets import RealWorldDatasets


class ComprehensiveBenchmark:
    """
    Comprehensive benchmarking system for knapsack algorithms.
    """

    def __init__(self):
        self.benchmark = KnapsackBenchmark()
        self.results = {}

    def create_scalability_test_datasets(self) -> Dict:
        """
        Create datasets of different sizes to test algorithm scalability.
        """
        datasets = {}

        # Small datasets (5-15 items)
        for n in [5, 10, 15]:
            items = [KnapsackItem(
                weight=random.randint(1, 50),
                value=random.randint(10, 200),
                name=f"Item_{i}"
            ) for i in range(n)]
            datasets[f'Size_{n}'] = {
                'items': items,
                'capacity': n * 20,
                'description': f'Random dataset with {n} items'
            }

        # Medium datasets (20-50 items)
        for n in [20, 30, 40, 50]:
            items = [KnapsackItem(
                weight=random.randint(1, 100),
                value=random.randint(10, 500),
                name=f"Item_{i}"
            ) for i in range(n)]
            datasets[f'Size_{n}'] = {
                'items': items,
                'capacity': n * 25,
                'description': f'Random dataset with {n} items'
            }

        return datasets

    def create_worst_case_datasets(self) -> Dict:
        """
        Create worst-case scenarios for different algorithms.
        """
        datasets = {}

        # Worst case for greedy: items with similar ratios but different optimal combinations
        items = [
            KnapsackItem(10, 100, "High Value Item 1"),    # ratio: 10.0
            KnapsackItem(11, 109, "High Value Item 2"),    # ratio: 9.9
            KnapsackItem(12, 118, "High Value Item 3"),    # ratio: 9.8
            KnapsackItem(30, 295, "Bulk Item 1"),          # ratio: 9.8
            KnapsackItem(31, 304, "Bulk Item 2"),          # ratio: 9.8
            KnapsackItem(32, 313, "Bulk Item 3"),          # ratio: 9.8
        ]
        datasets['Greedy_Worst_Case'] = {
            'items': items,
            'capacity': 60,
            'description': 'Items with very similar value-to-weight ratios'
        }

        # Worst case for backtracking: many items with good value-to-weight ratios
        items = [KnapsackItem(
            weight=random.randint(1, 10),
            value=random.randint(8, 15),
            name=f"Item_{i}"
        ) for i in range(25)]
        datasets['Backtracking_Worst_Case'] = {
            'items': items,
            'capacity': 100,
            'description': 'Many items with good ratios (exponential complexity)'
        }

        return datasets

    def run_comprehensive_benchmark(self) -> Dict:
        """
        在所有数据集类型上运行综合基准测试。
        """
        all_results = {}

        # 1. 基础测试数据集
        print("运行基础测试数据集...")
        basic_datasets = {
            'Small': {
                'items': [
                    KnapsackItem(10, 60, "Item1"),
                    KnapsackItem(20, 100, "Item2"),
                    KnapsackItem(30, 120, "Item3")
                ],
                'capacity': 50
            },
            'Medium': {
                'items': [KnapsackItem(random.randint(1, 50), random.randint(10, 200), f"Item{i}")
                         for i in range(15)],
                'capacity': 200
            }
        }

        for name, data in basic_datasets.items():
            results = self.benchmark.run_benchmark(data['items'], data['capacity'])
            all_results[name] = {
                'results': results,
                'dataset_info': {
                    'num_items': len(data['items']),
                    'capacity': data['capacity'],
                    'type': 'basic'
                }
            }

        # 2. 真实世界数据集
        print("运行真实世界数据集...")
        real_world_datasets = RealWorldDatasets.get_all_real_world_datasets()
        for name, data in real_world_datasets.items():
            results = self.benchmark.run_benchmark(data['items'], data['capacity'])
            all_results[name] = {
                'results': results,
                'dataset_info': {
                    'num_items': len(data['items']),
                    'capacity': data['capacity'],
                    'type': 'real_world',
                    'source': data['source']
                }
            }

        # 3. 可扩展性数据集
        print("运行可扩展性测试...")
        scalability_datasets = self.create_scalability_test_datasets()
        for name, data in scalability_datasets.items():
            # Skip backtracking for large datasets due to exponential complexity
            if int(name.split('_')[1]) > 20:
                try:
                    results = self.benchmark.run_benchmark(data['items'], data['capacity'])
                    # Remove backtracking results if they're too slow
                    if 'Backtracking' in results and results['Backtracking']['execution_time'] > 10:
                        del results['Backtracking']
                except:
                    results = self.benchmark.run_benchmark(data['items'], data['capacity'])
                    if 'Backtracking' in results:
                        del results['Backtracking']
            else:
                results = self.benchmark.run_benchmark(data['items'], data['capacity'])

            all_results[name] = {
                'results': results,
                'dataset_info': {
                    'num_items': len(data['items']),
                    'capacity': data['capacity'],
                    'type': 'scalability'
                }
            }

        # 4. 最坏情况数据集
        print("运行最坏情况场景...")
        worst_case_datasets = self.create_worst_case_datasets()
        for name, data in worst_case_datasets.items():
            results = self.benchmark.run_benchmark(data['items'], data['capacity'])
            all_results[name] = {
                'results': results,
                'dataset_info': {
                    'num_items': len(data['items']),
                    'capacity': data['capacity'],
                    'type': 'worst_case',
                    'description': data['description']
                }
            }

        self.results = all_results
        return all_results

    def generate_performance_report(self) -> Dict:
        """
        生成综合性能报告。
        """
        if not self.results:
            print("无基准测试结果可用。请先运行基准测试。")
            return {}

        report = {
            'summary': {},
            'algorithm_performance': {},
            'dataset_analysis': {},
            'recommendations': {}
        }

        # Analyze algorithm performance
        algorithms = ['Greedy', 'Recursive DP', 'Iterative DP', 'Backtracking']
        algorithm_stats = {alg: {'total_time': 0, 'total_comparisons': 0, 'datasets_run': 0, 'avg_accuracy': 0}
                          for alg in algorithms}

        total_accuracy = {alg: 0 for alg in algorithms}

        for dataset_name, data in self.results.items():
            results = data['results']

            # Find optimal value for this dataset
            optimal_value = 0
            for result in results.values():
                if 'total_value' in result:
                    optimal_value = max(optimal_value, result['total_value'])

            for algorithm in algorithms:
                if algorithm in results and 'total_value' in results[algorithm]:
                    algorithm_stats[algorithm]['datasets_run'] += 1
                    algorithm_stats[algorithm]['total_time'] += results[algorithm]['execution_time']
                    algorithm_stats[algorithm]['total_comparisons'] += results[algorithm]['comparisons']

                    if optimal_value > 0:
                        accuracy = (results[algorithm]['total_value'] / optimal_value) * 100
                        total_accuracy[algorithm] += accuracy

        # Calculate averages
        for algorithm in algorithms:
            if algorithm_stats[algorithm]['datasets_run'] > 0:
                algorithm_stats[algorithm]['avg_time'] = (
                    algorithm_stats[algorithm]['total_time'] /
                    algorithm_stats[algorithm]['datasets_run']
                )
                algorithm_stats[algorithm]['avg_comparisons'] = (
                    algorithm_stats[algorithm]['total_comparisons'] /
                    algorithm_stats[algorithm]['datasets_run']
                )
                algorithm_stats[algorithm]['avg_accuracy'] = (
                    total_accuracy[algorithm] /
                    algorithm_stats[algorithm]['datasets_run']
                )

        report['algorithm_performance'] = algorithm_stats

        # Generate recommendations
        recommendations = {}

        # Speed recommendation
        fastest_algo = min(algorithm_stats.keys(),
                          key=lambda x: algorithm_stats[x]['avg_time'] if algorithm_stats[x]['avg_time'] > 0 else float('inf'))
        recommendations['speed'] = fastest_algo

        # Accuracy recommendation
        most_accurate_algo = max(algorithm_stats.keys(),
                                key=lambda x: algorithm_stats[x]['avg_accuracy'])
        recommendations['accuracy'] = most_accurate_algo

        # Best overall (balance of speed and accuracy)
        best_overall = max(algorithm_stats.keys(),
                          key=lambda x: algorithm_stats[x]['avg_accuracy'] - algorithm_stats[x]['avg_time'])
        recommendations['best_overall'] = best_overall

        report['recommendations'] = recommendations

        return report

    def create_visualizations(self):
        """
        创建基准测试结果的可视化。
        """
        if not self.results:
            print("无基准测试结果可用。请先运行基准测试。")
            return

        # 性能比较图表
        plt.figure(figsize=(12, 8))

        algorithms = ['Greedy', 'Recursive DP', 'Iterative DP', 'Backtracking']
        datasets_to_plot = [name for name in self.results.keys() if self.results[name]['dataset_info']['num_items'] <= 20]

        x = np.arange(len(datasets_to_plot))
        width = 0.2

        execution_times = []
        for algorithm in algorithms:
            times = []
            for dataset_name in datasets_to_plot:
                if algorithm in self.results[dataset_name]['results']:
                    times.append(self.results[dataset_name]['results'][algorithm]['execution_time'])
                else:
                    times.append(0)
            execution_times.append(times)

        fig, ax = plt.subplots(figsize=(12, 6))
        for i, (algorithm, times) in enumerate(zip(algorithms, execution_times)):
            ax.bar(x + i*width, times, width, label=algorithm)

        ax.set_xlabel('Datasets')
        ax.set_ylabel('Execution Time (seconds)')
        ax.set_title('Algorithm Performance Comparison')
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(datasets_to_plot, rotation=45)
        ax.legend()

        plt.tight_layout()
        plt.savefig('algorithm_performance.png')
        plt.close()

        print("可视化已保存为 'algorithm_performance.png'")

    def save_results(self, filename: str = 'knapsack_benchmark_results.json'):
        """
        将基准测试结果保存到JSON文件。
        """
        # 将结果转换为JSON可序列化格式
        serializable_results = {}
        for dataset_name, data in self.results.items():
            serializable_results[dataset_name] = {
                'dataset_info': data['dataset_info'],
                'results': {}
            }

            for algorithm, result in data['results'].items():
                if 'error' not in result:
                    serializable_results[dataset_name]['results'][algorithm] = {
                        'total_value': result['total_value'],
                        'total_weight': result['total_weight'],
                        'execution_time': result['execution_time'],
                        'comparisons': result['comparisons'],
                        'num_selected_items': len(result['selected_items'])
                    }
                else:
                    serializable_results[dataset_name]['results'][algorithm] = {
                        'error': result['error'],
                        'execution_time': result['execution_time'],
                        'comparisons': result['comparisons']
                    }

        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)

        print(f"结果已保存到 {filename}")


def main():
    """
    运行综合基准测试的主函数。
    """
    print("开始综合0/1背包算法基准测试...")
    print("=" * 60)

    benchmark = ComprehensiveBenchmark()

    # 运行综合基准测试
    results = benchmark.run_comprehensive_benchmark()

    # 生成并显示报告
    report = benchmark.generate_performance_report()

    print("\n" + "=" * 60)
    print("综合基准测试报告")
    print("=" * 60)

    print("\n算法性能摘要:")
    for algorithm, stats in report['algorithm_performance'].items():
        if stats['datasets_run'] > 0:
            print(f"\n{algorithm}:")
            print(f"  平均执行时间: {stats['avg_time']:.6f} 秒")
            print(f"  平均比较次数: {stats['avg_comparisons']:.0f}")
            print(f"  平均准确度: {stats['avg_accuracy']:.2f}%")
            print(f"  完成数据集: {stats['datasets_run']}")

    print("\n推荐:")
    print(f"  最快算法: {report['recommendations']['speed']}")
    print(f"  最准确算法: {report['recommendations']['accuracy']}")
    print(f"  综合最佳算法: {report['recommendations']['best_overall']}")

    # 创建可视化
    benchmark.create_visualizations()

    # 保存结果
    benchmark.save_results()

    print("\n基准测试成功完成!")
    print("查看 'algorithm_performance.png' 获取可视化结果。")
    print("查看 'knapsack_benchmark_results.json' 获取详细结果。")


if __name__ == "__main__":
    main()