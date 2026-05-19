import time
import heapq
import random
from typing import List, Tuple, Optional, Set, Callable
from n_queens_solver import NQueensSolver


class AdvancedNQueensSolver(NQueensSolver):
    """增强版N皇后问题求解器 - 包含多种启发式算法"""

    def __init__(self, n: int):
        super().__init__(n)

    def get_attack_count(self, board: List[int], row: int, col: int) -> int:
        """计算在指定位置放置皇后后，该皇后会被攻击的次数"""
        attacks = 0
        for i in range(row):
            if board[i] == col:  # 同列攻击
                attacks += 1
            if abs(board[i] - col) == abs(i - row):  # 对角线攻击
                attacks += 1
        return attacks

    def get_free_positions_count(self, board: List[int], row: int, col: int) -> int:
        """计算在指定位置放置皇后后，下一行还有多少安全位置"""
        if row + 1 >= self.n:
            return 0

        free_count = 0
        temp_board = board[:]
        temp_board[row] = col

        for next_col in range(self.n):
            if self.is_safe(temp_board, row + 1, next_col):
                free_count += 1

        return free_count

    def get_diagonal_distance(self, board: List[int], row: int, col: int) -> int:
        """计算到棋盘中心的对角线距离（中心优先启发式）"""
        center = self.n // 2
        return abs(row - center) + abs(col - center)

    def bestfs_attack_heuristic_all(self) -> List[List[int]]:
        """BestFS算法 - 基于最小攻击次数启发式（求所有解）"""
        self.solutions = []

        def solve_recursive(board: List[int], row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            # 为当前行的每个可能位置计算攻击次数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    attacks = self.get_attack_count(board, row, col)
                    heapq.heappush(candidates, (attacks, col))

            # 按攻击次数从小到大尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                solve_recursive(board, row + 1)
                board[row] = -1

        board = [-1] * self.n
        solve_recursive(board, 0)
        return self.solutions

    def bestfs_attack_heuristic_one(self) -> Optional[List[int]]:
        """BestFS算法 - 基于最小攻击次数启发式（求一个解）"""
        def solve_recursive(board: List[int], row: int) -> bool:
            if row == self.n:
                return True

            # 为当前行的每个可能位置计算攻击次数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    attacks = self.get_attack_count(board, row, col)
                    heapq.heappush(candidates, (attacks, col))

            # 按攻击次数从小到大尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                if solve_recursive(board, row + 1):
                    return True
                board[row] = -1

            return False

        board = [-1] * self.n
        if solve_recursive(board, 0):
            return board[:]
        return None

    def bestfs_forward_checking_all(self) -> List[List[int]]:
        """BestFS算法 - 基于前向检查启发式（求所有解）"""
        self.solutions = []

        def solve_recursive(board: List[int], row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            # 为当前行的每个可能位置计算下一行的可用位置数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    free_positions = self.get_free_positions_count(board, row, col)
                    # 使用负数因为我们要最大化可用位置数
                    heapq.heappush(candidates, (-free_positions, col))

            # 按可用位置数从大到小尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                solve_recursive(board, row + 1)
                board[row] = -1

        board = [-1] * self.n
        solve_recursive(board, 0)
        return self.solutions

    def bestfs_forward_checking_one(self) -> Optional[List[int]]:
        """BestFS算法 - 基于前向检查启发式（求一个解）"""
        def solve_recursive(board: List[int], row: int) -> bool:
            if row == self.n:
                return True

            # 为当前行的每个可能位置计算下一行的可用位置数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    free_positions = self.get_free_positions_count(board, row, col)
                    # 使用负数因为我们要最大化可用位置数
                    heapq.heappush(candidates, (-free_positions, col))

            # 按可用位置数从大到小尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                if solve_recursive(board, row + 1):
                    return True
                board[row] = -1

            return False

        board = [-1] * self.n
        if solve_recursive(board, 0):
            return board[:]
        return None

    def bestfs_center_preference_all(self) -> List[List[int]]:
        """BestFS算法 - 基于中心优先启发式（求所有解）"""
        self.solutions = []

        def solve_recursive(board: List[int], row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            # 为当前行的每个可能位置计算到中心的距离
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    distance = self.get_diagonal_distance(board, row, col)
                    heapq.heappush(candidates, (distance, col))

            # 按到中心的距离从小到大尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                solve_recursive(board, row + 1)
                board[row] = -1

        board = [-1] * self.n
        solve_recursive(board, 0)
        return self.solutions

    def bestfs_center_preference_one(self) -> Optional[List[int]]:
        """BestFS算法 - 基于中心优先启发式（求一个解）"""
        def solve_recursive(board: List[int], row: int) -> bool:
            if row == self.n:
                return True

            # 为当前行的每个可能位置计算到中心的距离
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    distance = self.get_diagonal_distance(board, row, col)
                    heapq.heappush(candidates, (distance, col))

            # 按到中心的距离从小到大尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                if solve_recursive(board, row + 1):
                    return True
                board[row] = -1

            return False

        board = [-1] * self.n
        if solve_recursive(board, 0):
            return board[:]
        return None

    def backtracking_with_mrv_all(self) -> List[List[int]]:
        """回溯算法 + 最小剩余值启发式（求所有解）"""
        self.solutions = []

        def get_valid_columns(board: List[int], row: int) -> Set[int]:
            """获取指定行的有效列"""
            valid_cols = set(range(self.n))
            for i in range(row):
                if board[i] in valid_cols:
                    valid_cols.remove(board[i])  # 移除同列
                # 移除对角线
                diag1 = board[i] + (row - i)
                diag2 = board[i] - (row - i)
                valid_cols.discard(diag1)
                valid_cols.discard(diag2)
            return valid_cols

        def solve_recursive(board: List[int], row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            # 选择具有最少有效值的行（MRV启发式）
            if row < self.n - 1:
                min_valid = float('inf')
                next_row = row
                for r in range(row + 1, self.n):
                    valid_count = len(get_valid_columns(board, r))
                    if valid_count < min_valid:
                        min_valid = valid_count
                        next_row = r

                # 交换行
                if next_row != row:
                    board[row], board[next_row] = board[next_row], board[row]

            # 尝试当前行的所有有效列
            valid_cols = get_valid_columns(board, row)
            for col in sorted(valid_cols):  # 排序以确保确定性
                board[row] = col
                solve_recursive(board, row + 1)
                board[row] = -1

        board = [-1] * self.n
        solve_recursive(board, 0)
        return self.solutions

    def backtracking_with_mrv_one(self) -> Optional[List[int]]:
        """回溯算法 + 最小剩余值启发式（求一个解）"""
        def get_valid_columns(board: List[int], row: int) -> Set[int]:
            """获取指定行的有效列"""
            valid_cols = set(range(self.n))
            for i in range(row):
                if board[i] in valid_cols:
                    valid_cols.remove(board[i])  # 移除同列
                # 移除对角线
                diag1 = board[i] + (row - i)
                diag2 = board[i] - (row - i)
                valid_cols.discard(diag1)
                valid_cols.discard(diag2)
            return valid_cols

        def solve_recursive(board: List[int], row: int) -> bool:
            if row == self.n:
                return True

            # 选择具有最少有效值的行（MRV启发式）
            if row < self.n - 1:
                min_valid = float('inf')
                next_row = row
                for r in range(row + 1, self.n):
                    valid_count = len(get_valid_columns(board, r))
                    if valid_count < min_valid:
                        min_valid = valid_count
                        next_row = r

                # 交换行
                if next_row != row:
                    board[row], board[next_row] = board[next_row], board[row]

            # 尝试当前行的所有有效列
            valid_cols = get_valid_columns(board, row)
            for col in sorted(valid_cols):  # 排序以确保确定性
                board[row] = col
                if solve_recursive(board, row + 1):
                    return True
                board[row] = -1

            return False

        board = [-1] * self.n
        if solve_recursive(board, 0):
            return board[:]
        return None


if __name__ == "__main__":
    # 测试增强版算法
    solver = AdvancedNQueensSolver(6)

    print("增强版算法测试 (N=6):")
    print("=" * 50)

    algorithms = [
        ("最小攻击启发式", solver.bestfs_attack_heuristic_one),
        ("前向检查启发式", solver.bestfs_forward_checking_one),
        ("中心优先启发式", solver.bestfs_center_preference_one),
        ("MRV启发式", solver.backtracking_with_mrv_one)
    ]

    for algo_name, algo_func in algorithms:
        start_time = time.time()
        solution = algo_func()
        end_time = time.time()

        print(f"\n{algo_name}:")
        print(f"执行时间: {end_time - start_time:.6f} 秒")
        if solution:
            print(f"找到解: {solution}")
            solver.print_solution(solution)
        else:
            print("未找到解")