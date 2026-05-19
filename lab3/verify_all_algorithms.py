#!/usr/bin/env python3
"""
验证所有N皇后算法正确性的脚本
"""

from n_queens_solver import NQueensSolver
from advanced_n_queens import AdvancedNQueensSolver

def is_valid_solution(solution, n):
    """验证解是否有效"""
    if not solution or len(solution) != n:
        return False

    # 检查是否有重复的列
    if len(set(solution)) != n:
        return False

    # 检查对角线冲突
    for i in range(n):
        for j in range(i + 1, n):
            if abs(solution[i] - solution[j]) == abs(i - j):
                return False

    return True

def test_algorithm(name, solver, method_name, n=6):
    """测试单个算法"""
    try:
        method = getattr(solver, method_name)
        result = method()

        if "all" in method_name:
            # 测试求所有解的方法
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    # 验证每个解
                    valid_count = sum(1 for sol in result if is_valid_solution(sol, n))
                    print(f"✅ {name}: 找到 {len(result)} 个解，其中 {valid_count} 个有效")
                    return valid_count == len(result) and len(result) > 0
        else:
            # 测试求一个解的方法
            if result is not None:
                is_valid = is_valid_solution(result, n)
                print(f"✅ {name}: 找到有效解 {result}" if is_valid else f"❌ {name}: 解无效 {result}")
                return is_valid
            else:
                print(f"❌ {name}: 未找到解")
                return False

    except Exception as e:
        print(f"❌ {name}: 执行出错 - {e}")
        return False

def main():
    """主测试函数"""
    print("N皇后算法正确性验证")
    print("=" * 50)

    n = 6  # 使用6皇后进行测试
    print(f"测试N = {n}皇后问题\n")

    # 基础求解器测试
    basic_solver = NQueensSolver(n)
    basic_algorithms = [
        ("DFS - 一个解", "dfs_one_solution"),
        ("DFS - 所有解", "dfs_all_solutions"),
        ("BestFS - 一个解", "bestfs_one_solution"),
        ("BestFS - 所有解", "bestfs_all_solutions")
    ]

    print("基础算法测试:")
    print("-" * 30)
    basic_results = []
    for name, method in basic_algorithms:
        result = test_algorithm(name, basic_solver, method, n)
        basic_results.append(result)

    print()

    # 高级求解器测试
    advanced_solver = AdvancedNQueensSolver(n)
    advanced_algorithms = [
        ("最小攻击启发式 - 一个解", "bestfs_attack_heuristic_one"),
        ("最小攻击启发式 - 所有解", "bestfs_attack_heuristic_all"),
        ("前向检查启发式 - 一个解", "bestfs_forward_checking_one"),
        ("前向检查启发式 - 所有解", "bestfs_forward_checking_all"),
        ("中心优先启发式 - 一个解", "bestfs_center_preference_one"),
        ("中心优先启发式 - 所有解", "bestfs_center_preference_all"),
        ("MRV启发式 - 一个解", "backtracking_with_mrv_one"),
        ("MRV启发式 - 所有解", "backtracking_with_mrv_all")
    ]

    print("高级启发式算法测试:")
    print("-" * 30)
    advanced_results = []
    for name, method in advanced_algorithms:
        result = test_algorithm(name, advanced_solver, method, n)
        advanced_results.append(result)

    print()

    # 总结
    print("验证结果总结:")
    print("-" * 30)
    basic_passed = sum(basic_results)
    advanced_passed = sum(advanced_results)

    print(f"基础算法: {basic_passed}/{len(basic_results)} 通过")
    print(f"高级算法: {advanced_passed}/{len(advanced_results)} 通过")
    print(f"总通过率: {(basic_passed + advanced_passed)/(len(basic_results) + len(advanced_results))*100:.1f}%")

    if basic_passed == len(basic_results) and advanced_passed == len(advanced_results):
        print("\n🎉 所有算法验证通过！")
    else:
        print("\n⚠️  部分算法存在问题，请检查实现。")

if __name__ == "__main__":
    main()