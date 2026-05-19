import time
import heapq
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class NQueensSolver(ABC):
    """Abstract base class for N-Queens solvers"""

    def __init__(self, n: int):
        self.n = n
        self.solutions = []
        self.nodes_explored = 0
        self.start_time = 0
        self.end_time = 0

    @abstractmethod
    def solve(self):
        """Solve the N-Queens problem"""
        pass

    def get_execution_time(self) -> float:
        """Get execution time in seconds"""
        return self.end_time - self.start_time

    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """Check if placing a queen at (row, col) is safe"""
        for i in range(row):
            # Check column conflict
            if board[i] == col:
                return False
            # Check diagonal conflicts
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def count_conflicts(self, board: List[int], row: int) -> int:
        """Count conflicts for a partial board state up to given row"""
        conflicts = 0
        for i in range(row):
            for j in range(i + 1, row):
                # Column conflict
                if board[i] == board[j]:
                    conflicts += 1
                # Diagonal conflict
                if abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

class DFSAllSolver(NQueensSolver):
    """DFS solver that finds all solutions"""

    def solve(self) -> List[List[int]]:
        """Find all N-Queens solutions using DFS"""
        self.start_time = time.time()
        self.solutions = []
        self.nodes_explored = 0

        board = [-1] * self.n  # board[i] = column position of queen in row i
        self._dfs(board, 0)

        self.end_time = time.time()
        return self.solutions

    def _dfs(self, board: List[int], row: int):
        """Recursive DFS implementation"""
        self.nodes_explored += 1

        # Base case: all queens placed
        if row == self.n:
            self.solutions.append(board.copy())
            return

        # Try placing queen in each column of current row
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self._dfs(board, row + 1)
                board[row] = -1  # backtrack

class DFSSingleSolver(NQueensSolver):
    """DFS solver that finds a single solution"""

    def solve(self) -> Optional[List[int]]:
        """Find a single N-Queens solution using DFS"""
        self.start_time = time.time()
        self.nodes_explored = 0

        board = [-1] * self.n
        result = self._dfs(board, 0)

        self.end_time = time.time()
        if result is not None:
            self.solutions = [result]  # Store the single solution as a list
        return result

    def _dfs(self, board: List[int], row: int) -> Optional[List[int]]:
        """Recursive DFS implementation that stops at first solution"""
        self.nodes_explored += 1

        # Base case: all queens placed
        if row == self.n:
            return board.copy()

        # Try placing queen in each column of current row
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                result = self._dfs(board, row + 1)
                if result is not None:
                    return result
                board[row] = -1  # backtrack

        return None

@dataclass
class BoardState:
    """Represents a board state for BestFS"""
    board: List[int]
    row: int
    heuristic: int = field(init=False)

    def __post_init__(self):
        # Heuristic: number of conflicts in current board state
        self.heuristic = self._calculate_heuristic()

    def _calculate_heuristic(self) -> int:
        """Calculate heuristic value (lower is better)"""
        conflicts = 0
        for i in range(self.row):
            for j in range(i + 1, self.row):
                # Column conflict
                if self.board[i] == self.board[j]:
                    conflicts += 1
                # Diagonal conflict
                if abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflicts += 1

        # Add penalty for unplaced queens (encourages completing the board)
        unplaced_penalty = (len(self.board) - self.row) * len(self.board)
        return conflicts + unplaced_penalty

    def __lt__(self, other):
        """Comparison for priority queue (lower heuristic is better)"""
        return self.heuristic < other.heuristic

    def is_complete(self) -> bool:
        """Check if board state is a complete solution"""
        return self.row == len(self.board) and self.heuristic == 0

class BestFSAllSolver(NQueensSolver):
    """Best-First Search solver that finds all solutions"""

    def solve(self) -> List[List[int]]:
        """Find all N-Queens solutions using Best-First Search"""
        self.start_time = time.time()
        self.solutions = []
        self.nodes_explored = 0

        # Priority queue for BestFS
        pq = []
        initial_state = BoardState([-1] * self.n, 0)
        heapq.heappush(pq, initial_state)

        while pq:
            current_state = heapq.heappop(pq)
            self.nodes_explored += 1

            # If we have a complete solution
            if current_state.is_complete():
                self.solutions.append(current_state.board.copy())
                continue

            # If board is full but not a solution, skip
            if current_state.row >= self.n:
                continue

            # Generate next states by placing queen in next row
            for col in range(self.n):
                if self.is_safe(current_state.board, current_state.row, col):
                    new_board = current_state.board.copy()
                    new_board[current_state.row] = col
                    new_state = BoardState(new_board, current_state.row + 1)
                    heapq.heappush(pq, new_state)

        self.end_time = time.time()
        return self.solutions

class BestFSSingleSolver(NQueensSolver):
    """Best-First Search solver that finds a single solution"""

    def solve(self) -> Optional[List[int]]:
        """Find a single N-Queens solution using Best-First Search"""
        self.start_time = time.time()
        self.solutions = []
        self.nodes_explored = 0

        # Priority queue for BestFS
        pq = []
        initial_state = BoardState([-1] * self.n, 0)
        heapq.heappush(pq, initial_state)

        while pq:
            current_state = heapq.heappop(pq)
            self.nodes_explored += 1

            # If we have a complete solution, return immediately
            if current_state.is_complete():
                solution = current_state.board.copy()
                self.solutions = [solution]  # Store as list for consistency
                self.end_time = time.time()
                return solution

            # If board is full but not a solution, skip
            if current_state.row >= self.n:
                continue

            # Generate next states by placing queen in next row
            for col in range(self.n):
                if self.is_safe(current_state.board, current_state.row, col):
                    new_board = current_state.board.copy()
                    new_board[current_state.row] = col
                    new_state = BoardState(new_board, current_state.row + 1)
                    heapq.heappush(pq, new_state)

        self.end_time = time.time()
        return None

class OptimizedBestFSAllSolver(NQueensSolver):
    """Optimized Best-First Search with better heuristic"""

    def solve(self) -> List[List[int]]:
        """Find all N-Queens solutions using optimized Best-First Search"""
        self.start_time = time.time()
        self.solutions = []
        self.nodes_explored = 0

        pq = []
        initial_state = BoardState([-1] * self.n, 0)
        heapq.heappush(pq, initial_state)

        # Keep track of visited states to avoid duplicates
        visited = set()

        while pq:
            current_state = heapq.heappop(pq)
            self.nodes_explored += 1

            # Create state signature for duplicate detection
            state_sig = tuple(current_state.board[:current_state.row])
            if state_sig in visited:
                continue
            visited.add(state_sig)

            if current_state.is_complete():
                self.solutions.append(current_state.board.copy())
                continue

            if current_state.row >= self.n:
                continue

            # Generate children and sort by safety (most promising first)
            children = []
            for col in range(self.n):
                if self.is_safe(current_state.board, current_state.row, col):
                    new_board = current_state.board.copy()
                    new_board[current_state.row] = col
                    children.append((col, new_board))

            # Sort children by column conflicts heuristic
            children.sort(key=lambda x: self._column_conflicts_heuristic(x[1], current_state.row + 1))

            for col, new_board in children:
                new_state = BoardState(new_board, current_state.row + 1)
                heapq.heappush(pq, new_state)

        self.end_time = time.time()
        return self.solutions

    def _column_conflicts_heuristic(self, board: List[int], row: int) -> int:
        """Enhanced heuristic considering future conflicts"""
        conflicts = 0
        # Count current conflicts
        for i in range(row):
            for j in range(i + 1, row):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1

        # Add future conflict estimation
        if row < self.n:
            available_cols = set(range(self.n))
            for i in range(row):
                if board[i] in available_cols:
                    available_cols.remove(board[i])
                # Remove diagonal positions
                diag1 = board[i] + (row - i)
                diag2 = board[i] - (row - i)
                if diag1 in available_cols:
                    available_cols.discard(diag1)
                if diag2 in available_cols:
                    available_cols.discard(diag2)

            # Penalty for fewer available positions
            conflicts += (self.n - row) * (self.n - len(available_cols)) // 2

        return conflicts

class OptimizedBestFSSingleSolver(NQueensSolver):
    """Optimized Best-First Search for single solution"""

    def solve(self) -> Optional[List[int]]:
        """Find a single N-Queens solution using optimized Best-First Search"""
        self.start_time = time.time()
        self.solutions = []
        self.nodes_explored = 0

        pq = []
        initial_state = BoardState([-1] * self.n, 0)
        heapq.heappush(pq, initial_state)

        visited = set()

        while pq:
            current_state = heapq.heappop(pq)
            self.nodes_explored += 1

            state_sig = tuple(current_state.board[:current_state.row])
            if state_sig in visited:
                continue
            visited.add(state_sig)

            if current_state.is_complete():
                solution = current_state.board.copy()
                self.solutions = [solution]  # Store as list for consistency
                self.end_time = time.time()
                return solution

            if current_state.row >= self.n:
                continue

            # Generate and sort children
            children = []
            for col in range(self.n):
                if self.is_safe(current_state.board, current_state.row, col):
                    new_board = current_state.board.copy()
                    new_board[current_state.row] = col
                    children.append((col, new_board))

            children.sort(key=lambda x: self._column_conflicts_heuristic(x[1], current_state.row + 1))

            for col, new_board in children:
                new_state = BoardState(new_board, current_state.row + 1)
                heapq.heappush(pq, new_state)

        self.end_time = time.time()
        return None

    def _column_conflicts_heuristic(self, board: List[int], row: int) -> int:
        """Enhanced heuristic considering future conflicts"""
        conflicts = 0
        # Count current conflicts
        for i in range(row):
            for j in range(i + 1, row):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1

        # Add future conflict estimation
        if row < self.n:
            available_cols = set(range(self.n))
            for i in range(row):
                if board[i] in available_cols:
                    available_cols.remove(board[i])
                # Remove diagonal positions
                diag1 = board[i] + (row - i)
                diag2 = board[i] - (row - i)
                if diag1 in available_cols:
                    available_cols.discard(diag1)
                if diag2 in available_cols:
                    available_cols.discard(diag2)

            # Penalty for fewer available positions
            conflicts += (self.n - row) * (self.n - len(available_cols)) // 2

        return conflicts