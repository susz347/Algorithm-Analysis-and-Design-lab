import time
from n_queens_solver import NQueensSolver
from advanced_n_queens import AdvancedNQueensSolver


def print_board(board: list, title: str = ""):
    """美观地打印棋盘"""
    if title:
        print(title)
        print("=" * len(title))

    n = len(board)
    if n == 0:
        print("空棋盘")
        return

    # 打印列号
    print("   " + " ".join(f"{i:2}" for i in range(n)))
    print("  +" + "--" * n + "+")

    for i, queen_col in enumerate(board):
        row = ['.'] * n
        if queen_col != -1:
            row[queen_col] = 'Q'
        print(f"{i:2}| {' '.join(f'{cell:2}' for cell in row)} |")

    print("  +" + "--" * n + "+")
    print()


def demonstrate_basic_algorithms():
    """演示基础算法"""
    print("N皇后问题求解算法演示")
    print("=" * 50)

    n = 8  # 使用8皇后问题进行演示
    solver = NQueensSolver(n)

    print(f"求解 {n}皇后问题\n")

    # DFS算法演示
    print("1. DFS算法 - 求一个解")
    start_time = time.time()
    solution = solver.dfs_one_solution()
    dfs_time = time.time() - start_time

    if solution:
        print_board(solution, f"DFS找到的解 (耗时: {dfs_time:.4f}秒)")
    else:
        print("未找到解")

    # BestFS算法演示
    print("2. BestFS算法 - 求一个解")
    start_time = time.time()
    solution = solver.bestfs_one_solution()
    bestfs_time = time.time() - start_time

    if solution:
        print_board(solution, f"BestFS找到的解 (耗时: {bestfs_time:.4f}秒)")
    else:
        print("未找到解")

    print(f"算法比较: BestFS比DFS {'快' if bestfs_time < dfs_time else '慢'} "
          f"{abs(bestfs_time - dfs_time):.4f}秒")


def demonstrate_advanced_algorithms():
    """演示高级算法"""
    print("\n高级启发式算法演示")
    print("=" * 50)

    n = 8
    solver = AdvancedNQueensSolver(n)

    algorithms = [
        ("最小攻击启发式", solver.bestfs_attack_heuristic_one),
        ("前向检查启发式", solver.bestfs_forward_checking_one),
        ("中心优先启发式", solver.bestfs_center_preference_one),
        ("MRV启发式", solver.backtracking_with_mrv_one)
    ]

    results = []

    for algo_name, algo_func in algorithms:
        print(f"\n{algo_name}:")
        start_time = time.time()
        solution = algo_func()
        elapsed_time = time.time() - start_time

        if solution:
            print_board(solution, f"解 (耗时: {elapsed_time:.4f}秒)")
            results.append((algo_name, elapsed_time))
        else:
            print("未找到解")
            results.append((algo_name, float('inf')))

    # 比较结果
    if results:
        print("\n算法性能排名:")
        print("-" * 30)
        sorted_results = sorted([r for r in results if r[1] != float('inf')],
                              key=lambda x: x[1])
        for i, (name, time_taken) in enumerate(sorted_results, 1):
            print(f"{i}. {name}: {time_taken:.4f}秒")


def demonstrate_solution_count():
    """演示求解所有解的情况"""
    print("\n求解所有可行解演示")
    print("=" * 50)

    # 使用较小的N值来演示所有解
    n = 6
    solver = NQueensSolver(n)

    print(f"求解 {n}皇后问题的所有解\n")

    # DFS求所有解
    print("DFS算法 - 求所有解:")
    start_time = time.time()
    solutions = solver.dfs_all_solutions()
    dfs_time = time.time() - start_time

    print(f"找到 {len(solutions)} 个解 (耗时: {dfs_time:.4f}秒)")

    # 显示前几个解
    for i, solution in enumerate(solutions[:3]):
        print_board(solution, f"解 {i+1}")

    if len(solutions) > 3:
        print(f"... 还有 {len(solutions) - 3} 个解未显示")

    # BestFS求所有解
    print("\nBestFS算法 - 求所有解:")
    start_time = time.time()
    solutions = solver.bestfs_all_solutions()
    bestfs_time = time.time() - start_time

    print(f"找到 {len(solutions)} 个解 (耗时: {bestfs_time:.4f}秒)")
    print(f"BestFS比DFS {'快' if bestfs_time < dfs_time else '慢'} "
          f"{abs(bestfs_time - dfs_time):.4f}秒")


def demonstrate_different_sizes():
    """演示不同规模的问题"""
    print("\n不同规模问题的求解时间对比")
    print("=" * 50)

    sizes = [4, 6, 8, 10, 12]

    print("\n求一个解的时间对比:")
    print(f"{'N值':<4} {'DFS(秒)':<10} {'BestFS(秒)':<10} {'最小攻击启发式(秒)':<20}")
    print("-" * 50)

    for n in sizes:
        # DFS
        solver1 = NQueensSolver(n)
        start = time.time()
        solver1.dfs_one_solution()
        dfs_time = time.time() - start

        # BestFS
        solver2 = NQueensSolver(n)
        start = time.time()
        solver2.bestfs_one_solution()
        bestfs_time = time.time() - start

        # 最小攻击启发式
        solver3 = AdvancedNQueensSolver(n)
        start = time.time()
        solver3.bestfs_attack_heuristic_one()
        heuristic_time = time.time() - start

        print(f"{n:<4} {dfs_time:<10.4f} {bestfs_time:<10.4f} {heuristic_time:<20.4f}")


if __name__ == "__main__":
    demonstrate_basic_algorithms()
    demonstrate_advanced_algorithms()
    demonstrate_solution_count()
    demonstrate_different_sizes()

    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)