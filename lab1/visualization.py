#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法可视化程序
动态展示排序过程
"""

import random
import time
from typing import List, Generator
from sort_algorithms import SortAlgorithms

# 尝试导入matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class SortVisualizer:
    """排序算法可视化类"""

    def __init__(self, data: List[int], title: str = "排序算法可视化"):
        self.original_data = data.copy()
        self.title = title

        if HAS_MATPLOTLIB:
            self.fig, self.ax = plt.subplots(figsize=(12, 8))
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        else:
            self.fig = self.ax = None

    def _merge_sort_generator(self, arr: List[int]) -> Generator:
        """归并排序生成器，用于可视化"""
        if len(arr) <= 1:
            yield arr.copy()
            return

        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        # 递归处理左半部分
        left_gen = self._merge_sort_generator(left)
        for left_state in left_gen:
            yield left_state + [0] * len(right)

        # 递归处理右半部分
        right_gen = self._merge_sort_generator(right)
        for right_state in right_gen:
            yield [0] * len(left) + right_state

        # 合并过程
        merged = self._merge_with_yield(left, right)
        for state in merged:
            yield state

    def _merge_with_yield(self, left: List[int], right: List[int]) -> Generator:
        """带yield的合并过程"""
        result = []
        i = j = 0
        temp_arr = left + right

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

            # 显示当前合并状态
            current_state = result + left[i:] + right[j:]
            if len(current_state) < len(temp_arr):
                current_state.extend([0] * (len(temp_arr) - len(current_state)))
            yield current_state

        # 添加剩余元素
        result.extend(left[i:])
        result.extend(right[j:])
        yield result

    def _quick_sort_generator(self, arr: List[int]) -> Generator:
        """快速排序生成器"""
        if len(arr) <= 1:
            yield arr.copy()
            return

        pivot = arr[len(arr) // 2]
        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

        # 显示分区状态
        partition_state = less + equal + greater
        yield partition_state

        # 递归处理小于部分
        if less:
            less_gen = self._quick_sort_generator(less)
            for less_state in less_gen:
                yield less_state + equal + greater

        # 递归处理大于部分
        if greater:
            greater_gen = self._quick_sort_generator(greater)
            for greater_state in greater_gen:
                yield less + equal + greater_state

        # 最终状态
        final_result = (
            (less if not less else self._quick_sort_generator(less).__next__()) +
            equal +
            (greater if not greater else self._quick_sort_generator(greater).__next__())
        )
        yield final_result

    def _heap_sort_generator(self, arr: List[int]) -> Generator:
        """堆排序生成器"""
        result = arr.copy()
        n = len(result)

        # 构建最大堆
        for i in range(n // 2 - 1, -1, -1):
            yield from self._heapify_generator(result, n, i)

        # 逐个提取元素
        for i in range(n - 1, 0, -1):
            # 交换根节点和最后一个元素
            result[0], result[i] = result[i], result[0]
            yield result.copy()

            # 重新堆化
            yield from self._heapify_generator(result, i, 0)

        yield result

    def _heapify_generator(self, arr: List[int], n: int, i: int) -> Generator:
        """堆化过程的生成器"""
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[left] > arr[largest]:
                largest = left

            if right < n and arr[right] > arr[largest]:
                largest = right

            if largest == i:
                break

            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr.copy()
            i = largest

    def animate_merge_sort(self):
        """归并排序动画"""
        generator = self._merge_sort_generator(self.original_data.copy())
        return self._create_animation(generator, "归并排序可视化")

    def animate_quick_sort(self):
        """快速排序动画"""
        generator = self._quick_sort_generator(self.original_data.copy())
        return self._create_animation(generator, "快速排序可视化")

    def animate_heap_sort(self):
        """堆排序动画"""
        generator = self._heap_sort_generator(self.original_data.copy())
        return self._create_animation(generator, "堆排序可视化")

    def _create_animation(self, generator, title: str):
        """创建动画"""
        self.ax.clear()
        self.ax.set_title(title, fontsize=16, fontweight='bold')

        # 获取第一个状态
        try:
            first_state = next(generator)
        except StopIteration:
            return None

        bars = self.ax.bar(range(len(first_state)), first_state, color='skyblue')
        self.ax.set_xlabel('索引')
        self.ax.set_ylabel('值')
        self.ax.set_xticks(range(len(first_state)))

        def update(frame):
            self.ax.clear()
            self.ax.set_title(title, fontsize=16, fontweight='bold')
            self.ax.set_xlabel('索引')
            self.ax.set_ylabel('值')
            self.ax.set_xticks(range(len(frame)))

            colors = ['lightcoral' if i == min(len(frame)-1, 5) else 'skyblue' for i in range(len(frame))]
            bars = self.ax.bar(range(len(frame)), frame, color=colors)
            return bars

        # 收集所有帧
        frames = [first_state]
        for state in generator:
            frames.append(state)
            if len(frames) > 200:  # 限制帧数避免内存问题
                break

        if len(frames) <= 1:
            return None

        anim = animation.FuncAnimation(
            self.fig, update, frames=frames,
            interval=500, repeat=False, blit=False
        )

        return anim

    def show_animation(self, anim):
        """显示动画"""
        if not HAS_MATPLOTLIB:
            print("未安装matplotlib，无法显示动画")
            return

        if anim is None:
            print("无法创建动画")
            return

        plt.show()

    def save_animation(self, anim, filename: str):
        """保存动画"""
        if not HAS_MATPLOTLIB:
            print("未安装matplotlib，无法保存动画")
            return

        if anim is None:
            print("无法保存动画")
            return

        try:
            anim.save(filename, writer='pillow', fps=2)
            print(f"动画已保存为: {filename}")
        except Exception as e:
            print(f"保存动画失败: {e}")


def demonstrate_sorting_visualization():
    """演示排序可视化"""
    # 生成测试数据
    data = random.sample(range(1, 21), 15)  # 15个不重复的数字
    print("原始数据:", data)

    visualizer = SortVisualizer(data)

    # 选择要演示的算法
    algorithms = {
        '1': ('归并排序', visualizer.animate_merge_sort),
        '2': ('快速排序', visualizer.animate_quick_sort),
        '3': ('堆排序', visualizer.animate_heap_sort)
    }

    print("\n选择要可视化的排序算法:")
    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")

    choice = input("\n请输入选择 (1-3, 或 'all' 显示所有): ").strip()

    if choice == 'all':
        # 保存所有算法的动画
        for key, (name, func) in algorithms.items():
            print(f"\n生成 {name} 动画...")
            anim = func()
            if anim:
                visualizer.save_animation(anim, f"{name.replace('排序', '_sort')}.gif")
    elif choice in algorithms:
        name, func = algorithms[choice]
        print(f"\n运行 {name} 可视化...")
        anim = func()
        visualizer.show_animation(anim)
    else:
        print("无效选择")


def create_comparison_chart():
    """创建算法比较图表"""
    # 运行性能测试
    from benchmark import Benchmark

    print("运行性能测试以生成比较图表...")
    benchmark = Benchmark()

    # 使用较小的数据集进行快速测试
    sizes = [100, 200, 300, 400, 500]
    benchmark.run_benchmark(sizes=sizes, iterations=3)

    # 生成图表
    benchmark.plot_results()

    print("\n比较图表已生成!")


if __name__ == "__main__":
    print("排序算法可视化程序")
    print("=" * 50)

    while True:
        print("\n选择功能:")
        print("1. 排序过程可视化")
        print("2. 性能比较图表")
        print("3. 退出")

        choice = input("\n请输入选择 (1-3): ").strip()

        if choice == '1':
            demonstrate_sorting_visualization()
        elif choice == '2':
            create_comparison_chart()
        elif choice == '3':
            print("再见!")
            break
        else:
            print("无效选择，请重新输入")