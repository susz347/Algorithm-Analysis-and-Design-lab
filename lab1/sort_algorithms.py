#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法大比拼 - 基于分治策略的排序算法实现
包含：归并排序、快速排序、堆排序
"""

import random
import time
import sys
from typing import List, Callable


class SortAlgorithms:
    """排序算法类"""

    @staticmethod
    def merge_sort(arr: List[int]) -> List[int]:
        """
        归并排序 - 递归实现
        时间复杂度: O(n log n)
        空间复杂度: O(n)
        稳定性: 稳定
        """
        if len(arr) <= 1:
            return arr

        # 分割数组
        mid = len(arr) // 2
        left = SortAlgorithms.merge_sort(arr[:mid])
        right = SortAlgorithms.merge_sort(arr[mid:])

        # 合并有序数组
        return SortAlgorithms._merge(left, right)

    @staticmethod
    def _merge(left: List[int], right: List[int]) -> List[int]:
        """合并两个有序数组"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # 添加剩余元素
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def merge_sort_iterative(arr: List[int]) -> List[int]:
        """
        归并排序 - 迭代实现
        避免递归调用栈溢出
        """
        if len(arr) <= 1:
            return arr

        # 创建数组副本
        result = arr.copy()
        n = len(result)

        # 从大小为1的子数组开始，逐步增加
        size = 1
        while size < n:
            for start in range(0, n - size, 2 * size):
                mid = start + size
                end = min(start + 2 * size, n)

                # 合并两个子数组
                left = result[start:mid]
                right = result[mid:end]
                merged = SortAlgorithms._merge(left, right)
                result[start:start + len(merged)] = merged

            size *= 2

        return result

    @staticmethod
    def quick_sort(arr: List[int]) -> List[int]:
        """
        快速排序 - 递归实现
        时间复杂度: 平均 O(n log n)，最坏 O(n²)
        空间复杂度: O(log n)
        稳定性: 不稳定
        """
        if len(arr) <= 1:
            return arr

        # 三数取中选择基准
        pivot = SortAlgorithms._median_of_three(arr[0], arr[len(arr)//2], arr[-1])

        # 分割数组
        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

        # 递归排序并合并
        return (SortAlgorithms.quick_sort(less) +
                equal +
                SortAlgorithms.quick_sort(greater))

    @staticmethod
    def quick_sort_iterative(arr: List[int]) -> List[int]:
        """
        快速排序 - 迭代实现
        使用栈模拟递归
        """
        if len(arr) <= 1:
            return arr

        result = arr.copy()
        stack = [(0, len(result) - 1)]

        while stack:
            low, high = stack.pop()
            if low < high:
                # 分区操作
                pivot_index = SortAlgorithms._partition(result, low, high)

                # 将子数组边界压入栈
                if pivot_index - 1 > low:
                    stack.append((low, pivot_index - 1))
                if pivot_index + 1 < high:
                    stack.append((pivot_index + 1, high))

        return result

    @staticmethod
    def _partition(arr: List[int], low: int, high: int) -> int:
        """快速排序的分区函数"""
        # 选择最后一个元素作为基准
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    @staticmethod
    def _median_of_three(a: int, b: int, c: int) -> int:
        """三数取中"""
        if a <= b <= c or c <= b <= a:
            return b
        elif b <= a <= c or c <= a <= b:
            return a
        else:
            return c

    @staticmethod
    def heap_sort(arr: List[int]) -> List[int]:
        """
        堆排序 - 基于二叉堆
        时间复杂度: O(n log n)
        空间复杂度: O(1)
        稳定性: 不稳定
        """
        result = arr.copy()
        n = len(result)

        # 构建最大堆
        for i in range(n // 2 - 1, -1, -1):
            SortAlgorithms._heapify(result, n, i)

        # 逐个提取元素
        for i in range(n - 1, 0, -1):
            # 将当前根移动到末尾
            result[0], result[i] = result[i], result[0]
            # 对剩余堆进行调整
            SortAlgorithms._heapify(result, i, 0)

        return result

    @staticmethod
    def _heapify(arr: List[int], n: int, i: int):
        """堆化函数"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            SortAlgorithms._heapify(arr, n, largest)


# 测试函数
def test_sort_algorithm(algorithm_func: Callable, arr: List[int], name: str) -> float:
    """测试排序算法并返回执行时间"""
    start_time = time.time()
    sorted_arr = algorithm_func(arr.copy())
    end_time = time.time()

    # 验证排序结果
    is_sorted = all(sorted_arr[i] <= sorted_arr[i+1] for i in range(len(sorted_arr)-1))
    status = "正确" if is_sorted else "错误"
    print(f"{name}: {status} - 耗时: {(end_time - start_time)*1000:.2f}ms")

    return end_time - start_time


if __name__ == "__main__":
    # 简单的功能测试
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", test_array)
    print("归并排序:", SortAlgorithms.merge_sort(test_array))
    print("快速排序:", SortAlgorithms.quick_sort(test_array))
    print("堆排序:", SortAlgorithms.heap_sort(test_array))