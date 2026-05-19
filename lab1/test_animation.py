#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试动画生成功能
"""

from visualization import SortVisualizer
import random

def test_all_animations():
    """测试所有排序算法的动画生成"""
    print("排序算法动画测试")
    print("=" * 40)

    # 创建测试数据（小数据集以便快速生成）
    data = [64, 34, 25, 12, 22, 11, 90, 45, 78, 2, 50, 33]
    print(f"测试数据: {data}")

    # 创建可视化器
    visualizer = SortVisualizer(data, "排序算法演示")

    # 测试归并排序动画
    print("\n1. 生成归并排序动画...")
    try:
        anim1 = visualizer.animate_merge_sort()
        if anim1:
            visualizer.save_animation(anim1, "merge_sort_demo.gif")
            print("   [OK] 归并排序动画保存成功: merge_sort_demo.gif")
        else:
            print("   [FAIL] 归并排序动画生成失败")
    except Exception as e:
        print(f"   [ERROR] 归并排序动画错误: {e}")

    # 测试快速排序动画
    print("\n2. 生成快速排序动画...")
    try:
        anim2 = visualizer.animate_quick_sort()
        if anim2:
            visualizer.save_animation(anim2, "quick_sort_demo.gif")
            print("   [OK] 快速排序动画保存成功: quick_sort_demo.gif")
        else:
            print("   [FAIL] 快速排序动画生成失败")
    except Exception as e:
        print(f"   [ERROR] 快速排序动画错误: {e}")

    # 测试堆排序动画
    print("\n3. 生成堆排序动画...")
    try:
        anim3 = visualizer.animate_heap_sort()
        if anim3:
            visualizer.save_animation(anim3, "heap_sort_demo.gif")
            print("   [OK] 堆排序动画保存成功: heap_sort_demo.gif")
        else:
            print("   [FAIL] 堆排序动画生成失败")
    except Exception as e:
        print(f"   [ERROR] 堆排序动画错误: {e}")

    print("\n" + "=" * 40)
    print("动画生成测试完成!")
    print("请查看当前目录下的GIF文件:")
    print("- merge_sort_demo.gif")
    print("- quick_sort_demo.gif")
    print("- heap_sort_demo.gif")

if __name__ == "__main__":
    test_all_animations()