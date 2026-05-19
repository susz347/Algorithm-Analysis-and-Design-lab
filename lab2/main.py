#!/usr/bin/env python3
"""
0/1背包算法比较主执行脚本

此脚本演示所有实现的算法，并使用合成数据集和真实世界数据集运行综合基准测试。
"""

import sys
from knapsack_algorithms import (
    KnapsackBenchmark, KnapsackItem,
    GreedyKnapsackSolver, RecursiveDPKnapsackSolver,
    IterativeDPKnapsackSolver, BacktrackingKnapsackSolver
)
from real_world_datasets import RealWorldDatasets, demonstrate_real_world_usage
from benchmark_runner import ComprehensiveBenchmark


def run_basic_demonstration():
    """
    使用简单示例运行基础演示。
    """
    print("=" * 60)
    print("0/1背包算法演示")
    print("=" * 60)

    # 教科书中的经典示例
    items = [
        KnapsackItem(10, 60, "物品A"),
        KnapsackItem(20, 100, "物品B"),
        KnapsackItem(30, 120, "物品C")
    ]
    capacity = 50

    print(f"\n问题设置:")
    print(f"容量: {capacity}")
    print("物品:")
    for item in items:
        print(f"  {item}")

    benchmark = KnapsackBenchmark()
    results = benchmark.run_benchmark(items, capacity)
    benchmark.print_results(results, "基础示例")

    # 显示详细解决方案
    print("\n详细解决方案比较:")
    print("-" * 40)

    optimal_algorithm = max(
        [(name, result) for name, result in results.items() if 'total_value' in result],
        key=lambda x: x[1]['total_value']
    )

    print(f"{optimal_algorithm[0]}找到的最优解:")
    for item in optimal_algorithm[1]['selected_items']:
        print(f"  + {item.name} (重量: {item.weight}, 价值: {item.value})")
    print(f"总价值: {optimal_algorithm[1]['total_value']}")
    print(f"总重量: {optimal_algorithm[1]['total_weight']}/{capacity}")


def run_real_world_demonstration():
    """
    使用真实世界数据集运行演示。
    """
    print("\n" + "=" * 60)
    print("真实世界数据集演示")
    print("=" * 60)

    demonstrate_real_world_usage()


def run_comprehensive_benchmark():
    """
    在所有场景下运行综合基准测试。
    """
    print("\n" + "=" * 60)
    print("综合基准测试")
    print("=" * 60)

    benchmark = ComprehensiveBenchmark()
    results = benchmark.run_comprehensive_benchmark()

    # 生成并显示摘要
    report = benchmark.generate_performance_report()

    print("\n算法性能摘要:")
    print("-" * 40)

    for algorithm, stats in report['algorithm_performance'].items():
        if stats['datasets_run'] > 0:
            print(f"\n{algorithm}:")
            print(f"  平均执行时间: {stats['avg_time']:.6f} 秒")
            print(f"  平均比较次数: {stats['avg_comparisons']:.0f}")
            print(f"  平均准确度: {stats['avg_accuracy']:.2f}%")
            print(f"  完成数据集: {stats['datasets_run']}")

    print("\n推荐:")
    print("-" * 20)
    print(f"最快算法: {report['recommendations']['speed']}")
    print(f"最准确算法: {report['recommendations']['accuracy']}")
    print(f"综合最佳算法: {report['recommendations']['best_overall']}")

    # 创建可视化
    benchmark.create_visualizations()
    benchmark.save_results()

    print("\n基准测试产物已保存:")
    print("  - algorithm_performance.png (性能可视化)")
    print("  - knapsack_benchmark_results.json (详细结果)")


def compare_algorithm_characteristics():
    """
    比较每个算法的理论特性。
    """
    print("\n" + "=" * 60)
    print("算法特性比较")
    print("=" * 60)

    characteristics = {
        'Greedy': {
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(1)',
            'optimality': '不保证最优 (最优解的60-100%)',
            'best_for': '大数据集，快速近似',
            'worst_case': '具有相似价值重量比的物品',
            'advantages': '快速，简单，低内存使用',
            'disadvantages': '无最优性保证'
        },
        'Recursive DP': {
            'time_complexity': 'O(n × W)',
            'space_complexity': 'O(n × W)',
            'optimality': '始终最优',
            'best_for': '中等数据集且容量合理',
            'worst_case': '大容量值',
            'advantages': '最优解，处理所有情况',
            'disadvantages': '大问题内存使用高'
        },
        'Iterative DP': {
            'time_complexity': 'O(n × W)',
            'space_complexity': 'O(n × W)',
            'optimality': '始终最优',
            'best_for': '中等数据集，教学目的',
            'worst_case': '大容量值',
            'advantages': '最优解，无递归开销',
            'disadvantages': '高内存使用，填充整个表格'
        },
        'Backtracking': {
            'time_complexity': 'O(2^n)',
            'space_complexity': 'O(n)',
            'optimality': '始终最优',
            'best_for': '小数据集，内存有限时',
            'worst_case': '许多具有良好价值重量比的物品',
            'advantages': '最优解，低内存使用',
            'disadvantages': '指数时间复杂度'
        }
    }

    for algorithm, props in characteristics.items():
        print(f"\n{algorithm}:")
        print(f"  {'-' * len(algorithm)}")
        print(f"  时间复杂度: {props['time_complexity']}")
        print(f"  空间复杂度: {props['space_complexity']}")
        print(f"  最优性: {props['optimality']}")
        print(f"  最佳适用: {props['best_for']}")
        print(f"  最坏情况: {props['worst_case']}")
        print(f"  优点: {props['advantages']}")
        print(f"  缺点: {props['disadvantages']}")


def main():
    """
    主执行函数。
    """
    print("0/1背包算法综合比较")
    print("实现包含4种不同算法及真实世界测试")
    print("=" * 70)

    try:
        # 运行基础演示
        run_basic_demonstration()

        # 运行真实世界演示
        run_real_world_demonstration()

        # 比较算法特性
        compare_algorithm_characteristics()

        # 运行综合基准测试
        run_comprehensive_benchmark()

        print("\n" + "=" * 70)
        print("所有测试成功完成!")
        print("=" * 70)

        print("\n实现算法总结:")
        print("✓ 贪心算法 - 快速近似")
        print("✓ 递归动态规划 - 带记忆化的最优解")
        print("✓ 迭代动态规划 - 自底向上最优解")
        print("✓ 回溯算法 - 带剪枝的最优解")

        print("\n真实世界数据集测试:")
        print("✓ 投资组合优化")
        print("✓ 软件项目选择")
        print("✓ 营养优化")
        print("✓ 物流和运输")

        print("\n算法展示了不同的权衡:")
        print("- 贪心: 速度 vs 准确性")
        print("- 动态规划: 最优性 vs 内存使用")
        print("- 回溯: 最优性 vs 时间复杂度")

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())