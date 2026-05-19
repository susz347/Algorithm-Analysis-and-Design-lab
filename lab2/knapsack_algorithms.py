#!/usr/bin/env python3
"""
0/1背包问题 - 多种算法实现

该模块实现了多种解决0/1背包问题的算法：
1. 贪心算法
2. 递归动态规划
3. 迭代动态规划
4. 回溯算法

作者: Claude Code
日期: 2026/05/07
"""

import time
import random
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np


class KnapsackItem:
    """
    背包问题中的物品类

    表示背包问题中的一个物品，包含重量、价值和名称属性
    """

    def __init__(self, weight: int, value: int, name: str = ""):
        """
        初始化物品

        Args:
            weight (int): 物品重量
            value (int): 物品价值
            name (str): 物品名称（可选）
        """
        self.weight = weight  # 物品重量
        self.value = value    # 物品价值
        self.name = name      # 物品名称
        # 计算价值重量比（密度），用于贪心算法
        self.ratio = value / weight if weight > 0 else 0

    def __str__(self):
        """返回物品的字符串表示"""
        return f"Item({self.name}, w={self.weight}, v={self.value}, r={self.ratio:.2f})"

    def __repr__(self):
        """返回物品的正式字符串表示（用于调试）"""
        return self.__str__()


class KnapsackSolver:
    """
    背包求解器基类

    所有背包算法求解器的基类，定义了通用的接口和属性
    """

    def __init__(self, items: List[KnapsackItem], capacity: int):
        """
        初始化求解器

        Args:
            items (List[KnapsackItem]): 物品列表
            capacity (int): 背包容量
        """
        self.items = items           # 物品列表
        self.capacity = capacity     # 背包容量
        self.execution_time = 0      # 执行时间（秒）
        self.memory_used = 0         # 内存使用量（本实现中未使用）
        self.comparisons = 0         # 比较操作次数（用于性能分析）

    def solve(self) -> Tuple[List[KnapsackItem], int, int]:
        """
        解决背包问题

        Returns:
            Tuple[List[KnapsackItem], int, int]: 选中的物品列表、总价值、总重量

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError("子类必须实现solve方法")

    def get_stats(self) -> Dict:
        """
        获取求解器统计信息

        Returns:
            Dict: 包含执行时间、内存使用和比较次数的字典
        """
        return {
            'execution_time': self.execution_time,
            'memory_used': self.memory_used,
            'comparisons': self.comparisons
        }


class GreedyKnapsackSolver(KnapsackSolver):
    """
    贪心算法求解器

    基于价值重量比的贪心算法实现。
    将物品按价值重量比降序排列，然后贪心地选择能装入的物品。

    注意：不保证获得最优解，但速度非常快。
    时间复杂度：O(n log n)，主要来自排序操作
    空间复杂度：O(1)
    """

    def solve(self) -> Tuple[List[KnapsackItem], int, int]:
        """
        使用贪心算法解决背包问题

        算法步骤：
        1. 按价值重量比对物品进行降序排序
        2. 遍历排序后的物品，如果物品能装入背包就选择它

        Returns:
            Tuple[List[KnapsackItem], int, int]: 选中的物品、总价值、总重量
        """
        start_time = time.time()

        # 按价值重量比降序排序物品
        sorted_items = sorted(self.items, key=lambda x: x.ratio, reverse=True)

        selected_items = []  # 选中的物品列表
        total_value = 0      # 总价值
        total_weight = 0     # 总重量

        # 贪心地选择物品
        for item in sorted_items:
            self.comparisons += 1  # 增加比较计数
            # 如果当前物品能装入背包，就选择它
            if total_weight + item.weight <= self.capacity:
                selected_items.append(item)
                total_value += item.value
                total_weight += item.weight

        # 记录执行时间
        self.execution_time = time.time() - start_time
        return selected_items, total_value, total_weight


class RecursiveDPKnapsackSolver(KnapsackSolver):
    """
    递归动态规划求解器

    使用记忆化递归的动态规划算法实现。
    通过避免重复计算子问题来提高效率。

    时间复杂度：O(n × W)，其中n为物品数量，W为背包容量
    空间复杂度：O(n × W)，用于记忆化表格
    """

    def __init__(self, items: List[KnapsackItem], capacity: int):
        """初始化递归DP求解器"""
        super().__init__(items, capacity)
        self.memo = {}  # 记忆化字典，存储已计算的子问题结果

    def _recursive_solve(self, n: int, remaining_capacity: int) -> int:
        """
        递归求解子问题（带记忆化）

        Args:
            n (int): 考虑前n个物品
            remaining_capacity (int): 剩余容量

        Returns:
            int: 在前n个物品和剩余容量限制下的最大价值
        """
        # 基础情况：没有物品或容量为0
        if n == 0 or remaining_capacity == 0:
            return 0

        # 如果已经计算过这个子问题，直接返回结果
        if (n, remaining_capacity) in self.memo:
            return self.memo[(n, remaining_capacity)]

        self.comparisons += 1

        # 如果当前物品重量超过剩余容量，无法选择
        if self.items[n-1].weight > remaining_capacity:
            result = self._recursive_solve(n-1, remaining_capacity)
        else:
            # 选择最大值：包含当前物品 或 不包含当前物品
            include = (self.items[n-1].value +
                      self._recursive_solve(n-1, remaining_capacity - self.items[n-1].weight))
            exclude = self._recursive_solve(n-1, remaining_capacity)
            result = max(include, exclude)

        # 记忆化存储结果
        self.memo[(n, remaining_capacity)] = result
        return result

    def solve(self) -> Tuple[List[KnapsackItem], int, int]:
        """
        使用递归动态规划解决背包问题

        算法步骤：
        1. 使用记忆化递归计算最大价值
        2. 通过回溯确定选择了哪些物品

        Returns:
            Tuple[List[KnapsackItem], int, int]: 选中的物品、总价值、总重量
        """
        start_time = time.time()

        # 计算最大价值
        max_value = self._recursive_solve(len(self.items), self.capacity)

        # 回溯找出具体选择了哪些物品
        selected_items = []
        remaining_capacity = self.capacity

        # 从后往前检查每个物品是否被选中
        for i in range(len(self.items) - 1, -1, -1):
            if i == 0:
                # 处理最后一个物品
                if self.items[i].weight <= remaining_capacity:
                    selected_items.append(self.items[i])
                break

            # 检查物品i是否在最优解中
            if remaining_capacity >= self.items[i].weight:
                # 获取包含和不包含当前物品时的价值
                value_with = self.memo.get((i + 1, remaining_capacity), 0)
                value_without = self.memo.get((i, remaining_capacity), 0)
                value_with_item = (self.items[i].value +
                                 self.memo.get((i, remaining_capacity - self.items[i].weight), 0))

                # 如果包含当前物品能得到更大价值，则选择该物品
                if value_with == value_with_item:
                    selected_items.append(self.items[i])
                    remaining_capacity -= self.items[i].weight

        # 因为我们是从后往前遍历的，需要反转结果
        selected_items.reverse()
        total_weight = sum(item.weight for item in selected_items)

        self.execution_time = time.time() - start_time
        return selected_items, max_value, total_weight


class IterativeDPKnapsackSolver(KnapsackSolver):
    """
    迭代动态规划求解器

    使用自底向上的迭代方法构建动态规划表格。
    避免了递归调用的开销，但需要填充整个DP表格。

    时间复杂度：O(n × W)
    空间复杂度：O(n × W)
    """

    def solve(self) -> Tuple[List[KnapsackItem], int, int]:
        """
        使用迭代动态规划解决背包问题

        算法步骤：
        1. 创建并填充DP表格
        2. 通过回溯确定选择了哪些物品

        Returns:
            Tuple[List[KnapsackItem], int, int]: 选中的物品、总价值、总重量
        """
        start_time = time.time()
        n = len(self.items)

        # 创建DP表格，dp[i][w]表示前i个物品在容量w下的最大价值
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]

        # 填充DP表格
        for i in range(1, n + 1):
            for w in range(self.capacity + 1):
                self.comparisons += 1

                # 如果当前物品能装入
                if self.items[i-1].weight <= w:
                    # 选择最大值：不装入物品i-1 或 装入物品i-1
                    dp[i][w] = max(
                        dp[i-1][w],  # 不装入物品i-1
                        dp[i-1][w - self.items[i-1].weight] + self.items[i-1].value  # 装入物品i-1
                    )
                else:
                    # 当前物品太重，无法装入
                    dp[i][w] = dp[i-1][w]

        # 回溯找出选择了哪些物品
        selected_items = []
        w = self.capacity

        # 从表格右下角开始回溯
        for i in range(n, 0, -1):
            # 如果当前单元格的值与上一行不同，说明选择了该物品
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(self.items[i-1])
                w -= self.items[i-1].weight

        selected_items.reverse()  # 反转以得到正确的顺序
        total_value = dp[n][self.capacity]  # 最大价值
        total_weight = sum(item.weight for item in selected_items)

        self.execution_time = time.time() - start_time
        return selected_items, total_value, total_weight


class BacktrackingKnapsackSolver(KnapsackSolver):
    """
    回溯算法求解器

    使用带剪枝的回溯算法探索所有可能的组合。
    通过剪枝技术减少不必要的搜索，提高效率。

    时间复杂度：最坏情况O(2^n)，但剪枝会显著减少实际运行时间
    空间复杂度：O(n)，递归栈空间
    """

    def __init__(self, items: List[KnapsackItem], capacity: int):
        """初始化回溯求解器"""
        super().__init__(items, capacity)
        self.best_value = 0          # 当前找到的最佳价值
        self.best_solution = []      # 当前找到的最佳解决方案

    def _backtrack(self, index: int, current_weight: int, current_value: int, current_solution: List[bool]):
        """
        递归回溯函数

        Args:
            index (int): 当前考虑的物品索引
            current_weight (int): 当前总重量
            current_value (int): 当前总价值
            current_solution (List[bool]): 当前解决方案（每个物品是否被选中）
        """
        # 基础情况：已处理完所有物品
        if index == len(self.items):
            if current_value > self.best_value:
                self.best_value = current_value
                self.best_solution = current_solution[:]  # 复制当前解决方案
            return

        # 剪枝：如果即使选择所有剩余物品也无法超过当前最佳解，则跳过
        remaining_value = sum(self.items[i].value for i in range(index, len(self.items)))
        if current_value + remaining_value <= self.best_value:
            return

        self.comparisons += 1

        # 尝试不选择当前物品
        current_solution.append(False)
        self._backtrack(index + 1, current_weight, current_value, current_solution)
        current_solution.pop()

        # 尝试选择当前物品（如果能装入）
        if current_weight + self.items[index].weight <= self.capacity:
            current_solution.append(True)
            self._backtrack(
                index + 1,
                current_weight + self.items[index].weight,
                current_value + self.items[index].value,
                current_solution
            )
            current_solution.pop()

    def solve(self) -> Tuple[List[KnapsackItem], int, int]:
        """
        使用回溯算法解决背包问题

        算法步骤：
        1. 从第一个物品开始递归搜索
        2. 对每个物品尝试选择和不选择两种情况
        3. 使用剪枝避免无效搜索

        Returns:
            Tuple[List[KnapsackItem], int, int]: 选中的物品、总价值、总重量
        """
        start_time = time.time()

        # 从第一个物品开始回溯搜索
        self._backtrack(0, 0, 0, [])

        # 从最佳解决方案中提取选中的物品
        selected_items = []
        for i, selected in enumerate(self.best_solution):
            if selected:
                selected_items.append(self.items[i])

        total_weight = sum(item.weight for item in selected_items)

        self.execution_time = time.time() - start_time
        return selected_items, self.best_value, total_weight


class KnapsackBenchmark:
    """
    背包算法基准测试类

    用于比较不同背包算法的性能和结果
    """

    def __init__(self):
        """初始化基准测试器"""
        self.solvers = {
            'Greedy': GreedyKnapsackSolver,              # 贪心算法
            'Recursive DP': RecursiveDPKnapsackSolver,  # 递归动态规划
            'Iterative DP': IterativeDPKnapsackSolver,  # 迭代动态规划
            'Backtracking': BacktrackingKnapsackSolver  # 回溯算法
        }

    def run_benchmark(self, items: List[KnapsackItem], capacity: int) -> Dict:
        """
        运行所有算法的基准测试

        Args:
            items (List[KnapsackItem]): 物品列表
            capacity (int): 背包容量

        Returns:
            Dict: 包含每个算法的结果和性能数据的字典
        """
        results = {}

        # 对每个算法运行测试
        for name, solver_class in self.solvers.items():
            try:
                # 创建求解器实例并求解
                solver = solver_class(items, capacity)
                selected_items, total_value, total_weight = solver.solve()

                # 存储结果
                results[name] = {
                    'selected_items': selected_items,
                    'total_value': total_value,
                    'total_weight': total_weight,
                    'execution_time': solver.execution_time,
                    'comparisons': solver.comparisons,
                    'stats': solver.get_stats()
                }

            except Exception as e:
                # 如果算法出现错误，记录错误信息
                results[name] = {
                    'error': str(e),
                    'execution_time': 0,
                    'comparisons': 0
                }

        return results

    def print_results(self, results: Dict, dataset_name: str = "未知"):
        """
        以格式化方式打印基准测试结果

        Args:
            results (Dict): 基准测试结果
            dataset_name (str): 数据集名称
        """
        print(f"\n{'='*60}")
        print(f"背包算法比较 - {dataset_name}")
        print(f"{'='*60}")

        # 找到最优值（所有算法中的最大值）
        optimal_value = 0
        for result in results.values():
            if 'total_value' in result:
                optimal_value = max(optimal_value, result['total_value'])

        # 打印每个算法的结果
        for algorithm, result in results.items():
            print(f"\n{algorithm}:")
            print(f"  {'-' * 40}")

            if 'error' in result:
                print(f"  错误: {result['error']}")
                continue

            # 计算准确度（相对于最优解的百分比）
            accuracy = (result['total_value'] / optimal_value * 100) if optimal_value > 0 else 0
            print(f"  总价值: {result['total_value']}")
            print(f"  总重量: {result['total_weight']}")
            print(f"  执行时间: {result['execution_time']:.6f} 秒")
            print(f"  比较次数: {result['comparisons']}")
            print(f"  准确度: {accuracy:.2f}%")
            print(f"  选中物品: {len(result['selected_items'])}")


def create_test_datasets():
    """
    创建用于基准测试的各种数据集

    Returns:
        Dict: 包含不同规模数据集的字典
    """
    datasets = {}

    # 小数据集（用于验证）
    datasets['Small'] = {
        'items': [
            KnapsackItem(10, 60, "Item1"),
            KnapsackItem(20, 100, "Item2"),
            KnapsackItem(30, 120, "Item3")
        ],
        'capacity': 50
    }

    # 中等数据集
    datasets['Medium'] = {
        'items': [
            KnapsackItem(12, 78, "Item1"), KnapsackItem(15, 80, "Item2"),
            KnapsackItem(18, 70, "Item3"), KnapsackItem(22, 95, "Item4"),
            KnapsackItem(25, 110, "Item5"), KnapsackItem(28, 125, "Item6"),
            KnapsackItem(32, 140, "Item7"), KnapsackItem(35, 150, "Item8"),
            KnapsackItem(38, 160, "Item9"), KnapsackItem(42, 170, "Item10")
        ],
        'capacity': 100
    }

    # 大数据集（随机生成）
    datasets['Large'] = {
        'items': [KnapsackItem(random.randint(1, 50), random.randint(10, 200), f"Item{i}")
                 for i in range(20)],
        'capacity': 200
    }

    return datasets


if __name__ == "__main__":
    # 测试实现
    benchmark = KnapsackBenchmark()
    datasets = create_test_datasets()

    for dataset_name, data in datasets.items():
        print(f"\n测试 {dataset_name} 数据集...")
        results = benchmark.run_benchmark(data['items'], data['capacity'])
        benchmark.print_results(results, dataset_name)