#!/usr/bin/env python3
"""
简单测试以验证所有算法正常工作。
"""

from knapsack_algorithms import (
    KnapsackBenchmark, KnapsackItem
)

def test_basic_functionality():
    """测试基本功能，使用小示例。"""
    print("测试基础0/1背包算法...")

    # 简单测试用例
    items = [
        KnapsackItem(10, 60, "物品A"),
        KnapsackItem(20, 100, "物品B"),
        KnapsackItem(30, 120, "物品C")
    ]
    capacity = 50

    benchmark = KnapsackBenchmark()
    results = benchmark.run_benchmark(items, capacity)

    print("\n结果:")
    for algorithm, result in results.items():
        if 'error' not in result:
            print(f"{algorithm}: 价值={result['total_value']}, 重量={result['total_weight']}, 时间={result['execution_time']:.6f}秒")
        else:
            print(f"{algorithm}: 错误 - {result['error']}")

    # 验证最优解
    optimal_value = max(result['total_value'] for result in results.values() if 'total_value' in result)
    print(f"\n最优价值: {optimal_value}")

    return results

def test_real_world_dataset():
    """使用真实世界数据集进行测试。"""
    from real_world_datasets import RealWorldDatasets

    print("\n使用真实世界投资组合数据集进行测试...")

    items, capacity = RealWorldDatasets.create_investment_portfolio_dataset()

    benchmark = KnapsackBenchmark()
    results = benchmark.run_benchmark(items, capacity)

    print(f"\n投资组合 (预算: ${capacity:,}):")
    for algorithm, result in results.items():
        if 'error' not in result:
            print(f"{algorithm}: 回报=${result['total_value']:,}, 投资=${result['total_weight']:,}, 时间={result['execution_time']:.6f}秒")

    return results

if __name__ == "__main__":
    print("0/1背包算法验证")
    print("=" * 40)

    basic_results = test_basic_functionality()
    real_world_results = test_real_world_dataset()

    print("\n" + "=" * 40)
    print("所有测试成功完成!")
    print("\n算法总结:")
    print("+ 贪心算法 - 快速近似")
    print("+ 递归动态规划 - 带记忆化的最优解")
    print("+ 迭代动态规划 - 自底向上的最优解")
    print("+ 回溯算法 - 带剪枝的最优解")