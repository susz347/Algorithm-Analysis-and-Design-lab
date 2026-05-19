# N-Queens Algorithm Comparison - Experiment Summary

## Overview

This experiment implements and compares multiple algorithms for solving the N-Queens problem, demonstrating different approaches to constraint satisfaction problems.

## Implemented Algorithms

### 1. DFS-All (Depth-First Search - All Solutions)
- **Purpose**: Find all possible solutions
- **Approach**: Standard backtracking with complete search
- **Performance**: Most efficient for finding all solutions
- **Time Complexity**: O(N!)
- **Space Complexity**: O(N)

### 2. DFS-Single (Depth-First Search - Single Solution)
- **Purpose**: Find first valid solution
- **Approach**: Early termination DFS
- **Performance**: Fastest for single solution (Winner in benchmark)
- **Time Complexity**: O(N!) worst case, much better average case
- **Space Complexity**: O(N)

### 3. BestFS-All (Best-First Search - All Solutions)
- **Purpose**: Find all solutions with heuristic guidance
- **Approach**: Priority queue with conflict-based heuristic
- **Performance**: Slower than DFS due to overhead but more systematic
- **Time Complexity**: O(N!)
- **Space Complexity**: O(N²)

### 4. BestFS-Single (Best-First Search - Single Solution)
- **Purpose**: Find single solution with heuristic guidance
- **Approach**: Best-first search with early termination
- **Performance**: Good balance of speed and intelligent search
- **Time Complexity**: O(N!) worst case
- **Space Complexity**: O(N²)

### 5. Optimized BestFS Variants
- **Enhancement**: Improved heuristic with future conflict estimation
- **Performance**: Better node exploration efficiency
- **Trade-off**: Higher computational overhead per node

## Experimental Results

### Performance Rankings (8x8 Board)

**Single Solution Finding:**
1. **DFS-Single** (0.0002s, 114 nodes) - Winner
2. **BestFS-Single** (0.0002s, 61 nodes)
3. **Opt-BestFS-Single** (0.0003s, 58 nodes)

**All Solutions Finding:**
1. **DFS-All** (0.0033s, 2057 nodes) - Winner
2. **BestFS-All** (0.0071s, 2057 nodes)
3. **Opt-BestFS-All** (0.0121s, 2057 nodes)

### Key Findings

1. **DFS-Single is fastest** for finding a single solution due to minimal overhead
2. **DFS-All is most efficient** for complete enumeration
3. **BestFS variants explore fewer nodes** but have higher per-node cost
4. **Optimized versions show better node efficiency** but don't overcome algorithmic overhead
5. **Memory usage is minimal** across all algorithms for small to medium boards

## Algorithm Analysis

### DFS Advantages
- Simple implementation and debugging
- Minimal memory overhead
- Predictable performance characteristics
- Optimal for complete solution enumeration

### BestFS Advantages
- Intelligent search ordering
- Fewer nodes explored for single solutions
- More systematic exploration
- Better for finding "good" solutions early

### Trade-offs

| Algorithm | Speed | Memory | Node Efficiency | Implementation Complexity |
|-----------|-------|--------|----------------|--------------------------|
| DFS-All | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★☆☆☆☆ |
| DFS-Single | ★★★★★ | ★★★★★ | ★★★☆☆ | ★☆☆☆☆ |
| BestFS-All | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |
| BestFS-Single | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| Opt-BestFS | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★☆ |

## Usage Instructions

### Quick Start
```bash
# Run demonstration on 8x8 board
python main.py quick

# Run comprehensive benchmark
python main.py benchmark

# Test algorithm correctness
python test_nqueens.py

# Interactive mode
python main.py
```

### Command Line Options
- `demo [size]`: Run demonstration on specific board size
- `test`: Run correctness tests
- `quick`: Quick 8x8 demonstration
- `benchmark [sizes]`: Run benchmark on specified sizes (comma-separated)

## Files Structure

- `README.md`: Comprehensive documentation and theory
- `algorithms.py`: Algorithm implementations
- `benchmark.py`: Performance testing system
- `main.py`: Main program with multiple interfaces
- `test_nqueens.py`: Correctness test suite
- `requirements.txt`: Dependencies
- `benchmark_results.txt`: Sample benchmark output
- `EXPERIMENT_SUMMARY.md`: This summary document

## Educational Value

This implementation demonstrates:

1. **Algorithm Design Patterns**: Backtracking, heuristic search
2. **Performance Analysis**: Time/space complexity, empirical testing
3. **Trade-off Analysis**: Different approaches to same problem
4. **Implementation Skills**: Clean code, testing, benchmarking
5. **Problem-Solving**: Constraint satisfaction techniques

## Conclusion

The experiment successfully demonstrates that:
- **Simple algorithms (DFS) often outperform complex ones** for well-structured problems
- **Heuristic guidance improves node efficiency** but may not overcome overhead
- **Early termination is highly effective** for single-solution problems
- **Complete enumeration requires systematic approaches** like DFS

For the N-Queens problem, DFS variants are recommended due to their simplicity and efficiency, while BestFS variants provide valuable insights into heuristic search techniques.