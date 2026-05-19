import time
import heapq
from typing import List, Tuple, Optional, Set


class NQueensSolver:
    """N皇后问题求解器 - 实现多种算法"""

    def __init__(self, n: int):
        self.n = n
        self.solutions = []

    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """检查在指定位置放置皇后是否安全"""
        for i in range(row):
            # 检查列冲突
            if board[i] == col:
                return False
            # 检查对角线冲突
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def dfs_all_solutions(self) -> List[List[int]]:
        """DFS算法求解所有可行解"""
        self.solutions = []
        board = [-1] * self.n  # board[i] 表示第i行皇后所在的列

        def backtrack(row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            for col in range(self.n):
                if self.is_safe(board, row, col):
                    board[row] = col
                    backtrack(row + 1)
                    board[row] = -1

        backtrack(0)
        return self.solutions

    def dfs_one_solution(self) -> Optional[List[int]]:
        """DFS算法求解一个可行解"""
        board = [-1] * self.n

        def backtrack(row: int) -> bool:
            if row == self.n:
                return True

            for col in range(self.n):
                if self.is_safe(board, row, col):
                    board[row] = col
                    if backtrack(row + 1):
                        return True
                    board[row] = -1
            return False

        if backtrack(0):
            return board[:]
        return None

    def get_conflicts_count(self, board: List[int], row: int, col: int) -> int:
        """计算在指定位置放置皇后后的冲突数"""
        conflicts = 0
        for i in range(row):
            if board[i] == col:  # 同列冲突
                conflicts += 1
            if abs(board[i] - col) == abs(i - row):  # 对角线冲突
                conflicts += 1
        return conflicts

    def bestfs_all_solutions(self) -> List[List[int]]:
        """BestFS算法求解所有可行解（基于最小冲突启发式）"""
        self.solutions = []

        def solve_recursive(board: List[int], row: int):
            if row == self.n:
                self.solutions.append(board[:])
                return

            # 为当前行的每个可能位置计算冲突数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    conflicts = self.get_conflicts_count(board, row, col)
                    heapq.heappush(candidates, (conflicts, col))

            # 按冲突数从小到大尝试
            while candidates:
                _, col = heapq.heappop(candidates)
                board[row] = col
                solve_recursive(board, row + 1)
                board[row] = -1

        board = [-1] * self.n
        solve_recursive(board, 0)
        return self.solutions

    def bestfs_one_solution(self) -> Optional[List[int]]:
        """BestFS算法求解一个可行解（基于最小冲突启发式）"""
        def solve_recursive(board: List[int], row: int) -> bool:
            if row == self.n:
                return True

            # 为当前行的每个可能位置计算冲突数
            candidates = []
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    conflicts = self.get_conflicts_count(board, row, col)
                    heapq.heappush(candidates, (conflicts, col))

            # 按冲突数从小到大尝试
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

    def get_solution_matrix(self, solution: List[int]) -> List[List[str]]:
        """将解转换为矩阵形式便于显示"""
        if not solution:
            return []

        matrix = [['.' for _ in range(self.n)] for _ in range(self.n)]
        for row, col in enumerate(solution):
            matrix[row][col] = 'Q'
        return matrix

    def print_solution(self, solution: List[int]):
        """打印单个解"""
        matrix = self.get_solution_matrix(solution)
        for row in matrix:
            print(' '.join(row))
        print()


if __name__ == "__main__":
    # 测试4皇后问题
    solver = NQueensSolver(4)

    print("DFS算法 - 所有解:")
    solutions = solver.dfs_all_solutions()
    print(f"找到 {len(solutions)} 个解")
    for i, sol in enumerate(solutions):
        print(f"解 {i+1}:")
        solver.print_solution(sol)

    print("DFS算法 - 一个解:")
    solution = solver.dfs_one_solution()
    if solution:
        solver.print_solution(solution)

    print("BestFS算法 - 所有解:")
    solutions = solver.bestfs_all_solutions()
    print(f"找到 {len(solutions)} 个解")
    for i, sol in enumerate(solutions):
        print(f"解 {i+1}:")
        solver.print_solution(sol)

    print("BestFS算法 - 一个解:")
    solution = solver.bestfs_one_solution()
    if solution:
        solver.print_solution(solution)