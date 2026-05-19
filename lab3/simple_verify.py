#!/usr/bin/env python3
"""
简单验证N皇后算法的脚本
"""

from n_queens_solver import NQueensSolver
from advanced_n_queens import AdvancedNQueensSolver

def main():
    """主测试函数"""
    print("N皇后算法简单验证")
    print("=" * 40)

    # 测试4皇后问题（已知有2个解）
    print("\n测试4皇后问题:")
    solver4 = NQueensSolver(4)

    # 测试DFS
    solution = solver4.dfs_one_solution()
    print(f"DFS找到一个解: {solution}")

    solutions = solver4.dfs_all_solutions()
    print(f"DFS找到所有解: {len(solutions)} 个")

    # 测试BestFS
    solution = solver4.bestfs_one_solution()
    print(f"BestFS找到一个解: {solution}")

    solutions = solver4.bestfs_all_solutions()
    print(f"BestFS找到所有解: {len(solutions)} 个")

    # 测试高级算法
    print("\n测试高级启发式算法:")
    advanced_solver = AdvancedNQueensSolver(4)

    algorithms = [
        "最小攻击启发式",
        "前向检查启发式",
        "中心优先启发式",
        "MRV启发式"
    ]

    methods = [
        "bestfs_attack_heuristic_one",
        "bestfs_forward_checking_one",
        "bestfs_center_preference_one",
        "backtracking_with_mrv_one"
    ]

    for algo, method in zip(algorithms, methods):
        try:
            method_func = getattr(advanced_solver, method)
            solution = method_func()
            print(f"{algo}: {solution}")
        except Exception as e:
            print(f"{algo}: 错误 - {e}")

    print("\n所有算法测试完成!")

if __name__ == "__main__":
    main()