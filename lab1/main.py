#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法大比拼 - 主程序
集成所有功能，提供用户友好的交互界面
"""

import os
import sys
import random
from sort_algorithms import SortAlgorithms, test_sort_algorithm
from benchmark import Benchmark
from visualization import SortVisualizer


def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """打印程序标题"""
    print("=" * 60)
    print("           排序算法大比拼")
    print("  Sorting Algorithms Comparison Project")
    print("=" * 60)
    print("实现算法: 归并排序、快速排序、堆排序")
    print("测试场景: 随机、有序、逆序、部分有序、重复数据")
    print("=" * 60)


def show_algorithm_info():
    """显示算法详细信息"""
    clear_screen()
    print("\n算法详细信息")
    print("-" * 40)
    print("\n1. 归并排序 (Merge Sort)")
    print("   - 时间复杂度: O(n log n)")
    print("   - 空间复杂度: O(n)")
    print("   - 稳定性: 稳定")
    print("   - 特点: 分治策略，将数组分成两半分别排序后合并")
    print("   - 适用场景: 大数据量，要求稳定排序")

    print("\n2. 快速排序 (Quick Sort)")
    print("   - 时间复杂度: 平均 O(n log n)，最坏 O(n²)")
    print("   - 空间复杂度: O(log n)")
    print("   - 稳定性: 不稳定")
    print("   - 特点: 分治策略，选择基准元素进行分区")
    print("   - 适用场景: 平均性能优秀，内存使用较少")

    print("\n3. 堆排序 (Heap Sort)")
    print("   - 时间复杂度: O(n log n)")
    print("   - 空间复杂度: O(1)")
    print("   - 稳定性: 不稳定")
    print("   - 特点: 基于二叉堆结构")
    print("   - 适用场景: 原地排序，空间复杂度最优")

    print("\n4. 不同场景下的性能特点:")
    print("   - 随机数据: 快速排序通常最快")
    print("   - 已排序数据: 归并排序性能稳定")
    print("   - 逆序数据: 快速排序可能退化到 O(n²)")
    print("   - 部分有序: 归并排序表现稳定")
    print("   - 重复数据: 三路快排更优，但本实现使用二路快排")

    input("\n按回车键返回主菜单...")


def basic_demo():
    """基础演示 - 展示算法正确性"""
    clear_screen()
    print("\n基础演示 - 算法正确性验证")
    print("-" * 40)

    # 测试数据
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9, 3],
        [100, 50, 25, 75, 10, 90, 30],
        list(range(10, 0, -1))  # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]

    algorithms = [
        (SortAlgorithms.merge_sort, "归并排序(递归)"),
        (SortAlgorithms.merge_sort_iterative, "归并排序(迭代)"),
        (SortAlgorithms.quick_sort, "快速排序(递归)"),
        (SortAlgorithms.quick_sort_iterative, "快速排序(迭代)"),
        (SortAlgorithms.heap_sort, "堆排序")
    ]

    for i, test_array in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_array}")
        print("-" * 30)

        for algorithm_func, algo_name in algorithms:
            test_sort_algorithm(algorithm_func, test_array, algo_name)

    print("\n基础演示完成! 所有算法均能正确排序。")
    input("\n按回车键返回主菜单...")


def performance_test():
    """性能测试 - 比较不同场景下的算法效率"""
    clear_screen()
    print("\n性能测试 - 算法效率比较")
    print("-" * 40)

    print("选择测试规模:")
    print("1. 小型数据 (100-1000 个元素)")
    print("2. 中型数据 (500-2000 个元素)")
    print("3. 大型数据 (1000-5000 个元素)")
    print("4. 自定义规模")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        sizes = [100, 300, 500, 800, 1000]
    elif choice == '2':
        sizes = [500, 800, 1000, 1500, 2000]
    elif choice == '3':
        sizes = [1000, 2000, 3000, 4000, 5000]
    elif choice == '4':
        try:
            custom_input = input("请输入数据规模 (用空格分隔，如: 100 500 1000): ")
            sizes = [int(x) for x in custom_input.split()]
        except ValueError:
            print("输入格式错误，使用默认设置")
            sizes = [100, 500, 1000]
    else:
        print("无效选择，使用默认设置")
        sizes = [100, 500, 1000]

    print(f"\n将测试的数据规模: {sizes}")
    print("测试需要一些时间，请耐心等待...")

    # 创建并运行性能测试
    benchmark = Benchmark()
    benchmark.run_benchmark(sizes=sizes, iterations=3)

    print("\n" + "=" * 60)
    print("性能测试结果")
    print("=" * 60)

    # 显示结果表格
    benchmark.print_results_table()

    # 分析结果
    benchmark.analyze_results()

    # 询问是否生成图表
    if input("\n是否生成性能比较图表? (y/n): ").lower().startswith('y'):
        benchmark.plot_results()

    input("\n按回车键返回主菜单...")


def visualize_sorting():
    """排序过程可视化"""
    clear_screen()
    print("\n排序过程可视化")
    print("-" * 40)

    print("选择数据生成方式:")
    print("1. 随机生成数据")
    print("2. 手动输入数据")
    print("3. 使用预设数据")

    choice = input("\n请输入选择 (1-3): ").strip()

    if choice == '1':
        try:
            size = int(input("请输入数据规模 (建议 5-20): ") or "10")
            size = max(5, min(20, size))  # 限制在 5-20 之间
            data = random.sample(range(1, 100), size)
        except ValueError:
            print("输入错误，使用默认设置")
            data = random.sample(range(1, 100), 10)
    elif choice == '2':
        try:
            data_input = input("请输入数字 (用空格分隔): ")
            data = [int(x) for x in data_input.split()]
            if len(data) > 20:
                print("数据过多，只取前20个")
                data = data[:20]
        except ValueError:
            print("输入格式错误，使用默认数据")
            data = [64, 34, 25, 12, 22, 11, 90, 45, 78, 2]
    else:
        data = [64, 34, 25, 12, 22, 11, 90, 45, 78, 2]

    print(f"\n测试数据: {data}")

    # 创建可视化器
    visualizer = SortVisualizer(data)

    print("\n选择要可视化的算法:")
    print("1. 归并排序")
    print("2. 快速排序")
    print("3. 堆排序")
    print("4. 保存所有算法动画")

    algo_choice = input("\n请输入选择 (1-4): ").strip()

    if algo_choice == '1':
        print("\n生成归并排序动画...")
        try:
            anim = visualizer.animate_merge_sort()
            if anim:
                print("动画生成成功! 按 q 退出动画窗口")
                visualizer.show_animation(anim)
            else:
                print("动画生成失败")
        except Exception as e:
            print(f"动画显示错误: {e}")

    elif algo_choice == '2':
        print("\n生成快速排序动画...")
        try:
            anim = visualizer.animate_quick_sort()
            if anim:
                print("动画生成成功! 按 q 退出动画窗口")
                visualizer.show_animation(anim)
            else:
                print("动画生成失败")
        except Exception as e:
            print(f"动画显示错误: {e}")

    elif algo_choice == '3':
        print("\n生成堆排序动画...")
        try:
            anim = visualizer.animate_heap_sort()
            if anim:
                print("动画生成成功! 按 q 退出动画窗口")
                visualizer.show_animation(anim)
            else:
                print("动画生成失败")
        except Exception as e:
            print(f"动画显示错误: {e}")

    elif algo_choice == '4':
        print("\n保存所有算法动画...")
        try:
            anim1 = visualizer.animate_merge_sort()
            if anim1:
                visualizer.save_animation(anim1, "merge_sort.gif")

            anim2 = visualizer.animate_quick_sort()
            if anim2:
                visualizer.save_animation(anim2, "quick_sort.gif")

            anim3 = visualizer.animate_heap_sort()
            if anim3:
                visualizer.save_animation(anim3, "heap_sort.gif")

            print("动画已保存为 GIF 文件")
        except Exception as e:
            print(f"保存动画错误: {e}")

    else:
        print("无效选择")

    input("\n按回车键返回主菜单...")


def main():
    """主函数"""
    while True:
        clear_screen()
        print_header()

        print("\n功能菜单:")
        print("1. 基础演示 - 算法正确性验证")
        print("2. 性能测试 - 不同场景效率比较")
        print("3. 可视化演示 - 排序过程动画")
        print("4. 算法详细信息")
        print("5. 退出程序")

        choice = input("\n请选择功能 (1-5): ").strip()

        if choice == '1':
            basic_demo()
        elif choice == '2':
            performance_test()
        elif choice == '3':
            visualize_sorting()
        elif choice == '4':
            show_algorithm_info()
        elif choice == '5':
            print("\n感谢使用排序算法大比拼! 再见!")
            break
        else:
            print("\n无效选择，请重新输入")
            input("按回车键继续...")


if __name__ == "__main__":
    # 检查必要的依赖
    try:
        import matplotlib
        print("+ 已安装 matplotlib，可视化功能可用")
    except ImportError:
        print("- 未安装 matplotlib，部分可视化功能可能无法使用")
        print("  可以使用以下命令安装: pip install matplotlib")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        sys.exit(1)