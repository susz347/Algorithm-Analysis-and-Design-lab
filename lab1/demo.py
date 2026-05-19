#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法大比拼 - 快速演示脚本
展示项目核心功能
"""

import os
import sys
from sort_algorithms import SortAlgorithms, test_sort_algorithm
from benchmark import Benchmark


def quick_demo():
    """快速演示"""
    print("=" * 60)
    print("排序算法大比拼 - 快速演示")
    print("=" * 60)

    # 1. 算法正确性验证
    print("\n1. 算法正确性验证")
    print("-" * 30)

    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"测试数组: {test_array}")

    algorithms = [
        (SortAlgorithms.merge_sort, "归并排序(递归)"),
        (SortAlgorithms.quick_sort, "快速排序(递归)"),
        (SortAlgorithms.heap_sort, "堆排序")
    ]

    for algorithm_func, algo_name in algorithms:
        test_sort_algorithm(algorithm_func, test_array, algo_name)

    # 2. 简单性能测试
    print("\n2. 简单性能测试 (1000个随机数)")
    print("-" * 30)

    import random
    test_data = [random.randint(1, 1000) for _ in range(1000)]

    for algorithm_func, algo_name in algorithms:
        test_sort_algorithm(algorithm_func, test_data, algo_name)

    # 3. 不同场景下的性能比较
    print("\n3. 不同场景性能分析")
    print("-" * 30)

    scenarios = {
        "随机数据": [random.randint(1, 100) for _ in range(500)],
        "已排序": list(range(1, 501)),
        "逆序": list(range(500, 0, -1)),
        "重复数据": [random.randint(1, 50) for _ in range(500)]
    }

    for scenario_name, data in scenarios.items():
        print(f"\n{scenario_name}:")
        best_time = float('inf')
        best_algo = ""

        for algorithm_func, algo_name in algorithms:
            elapsed_time = test_sort_algorithm(algorithm_func, data, algo_name)
            if elapsed_time < best_time:
                best_time = elapsed_time
                best_algo = algo_name

        print(f"  最优算法: {best_algo} ({best_time*1000:.2f}ms)")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)

    print("\n使用建议:")
    print("- 对于随机数据，快速排序通常最快")
    print("- 对于已排序数据，归并排序性能稳定")
    print("- 对于内存受限场景，堆排序空间效率最高")
    print("- 对于稳定性要求，选择归并排序")

    print("\n运行完整程序: python main.py")
    print("查看详细文档: 查看 README.md")


if __name__ == "__main__":
    quick_demo()