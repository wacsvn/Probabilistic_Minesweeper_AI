# Minesweeper AI

An AI-based solution for solving Minesweeper puzzles using constraint satisfaction and probabilistic reasoning.

## Project Overview

This project implements an AI agent that can solve Minesweeper puzzles of various sizes and difficulties. The AI uses a combination of logical deduction and probabilistic reasoning to uncover safe tiles and flag mines efficiently.

## Implementation Approach

### Minimal AI (Initial Version)

The initial Minimal AI algorithm included basic components such as:

- Board representation
- State updating
- Safe tile detection
- Action prioritization
- Uninformed search techniques

Key features of the Minimal AI:
- Uses sets for tracking revealed and flagged tiles
- Employs a neighbor function that adapts to boundary conditions
- Implements a simple heuristic via priority queue for action selection

**Performance of Minimal AI:**

| Board Size | Sample Size | Score | Worlds Complete |
|------------|-------------|-------|-----------------|
| 5x5        | 1000        | 392   | 392             |
| 8x8        | 1000        | 0     | 0               |
| 16x16      | 1000        | 0     | 0               |
| 16x30      | 1000        | 0     | 0               |
| Total      | 4000        | 392   | 392             |

### Final AI (Improved Version)

The Final AI builds upon the initial version with significant improvements:

- Enhanced constraint propagation (via the `assess` function in the Tile class)
- Advanced search strategy using the NavigationStack class (OrderedDict) for depth-first exploration
- Priority-based action selection (operations deque)
- Board-wide inference through the `sweep` function
- NumPy array representation for performance optimization
- Probabilistic reasoning via the `probe_random` function
- Improved error handling

**Performance of Final AI:**

| Board Size | Sample Size | Score | Worlds Complete |
|------------|-------------|-------|-----------------|
| 5x5        | 1000        | 1000  | 1000            |
| 8x8        | 1000        | 603   | 603             |
| 16x16      | 1000        | 976   | 488             |
| 16x30      | 1000        | 0     | 0               |
| Total      | 4000        | 2579  | 2091            |

## Future Improvements

Potential enhancements to improve performance:

1. **A* Search Algorithm**: Implement a heuristic function that estimates the risk of uncovering a given cell based on surrounding revealed cells and remaining mines.

2. **Bayesian Networks**: Model each cell as a node with a binary state (mine or no mine). Use revealed numbers as evidence to update probabilities across the board.

3. **Monte Carlo Tree Search**: Simulate random possible moves to estimate winning probabilities, particularly useful in late-game scenarios with fewer remaining mines.

## Project Structure

The project consists of several Python files:

- `AI.py`: Abstract base class defining the AI interface
- `MyAI.py`: Implementation of the Minesweeper AI agent
- `World.py`: Game engine that manages the Minesweeper board
- `Action.py`: Defines possible actions (LEAVE, UNCOVER, FLAG, UNFLAG)
- `WorldGenerator.py`: Utility for generating random Minesweeper worlds
- `Main.py`: Entry point for running the AI on Minesweeper worlds

## Usage

### Running the AI

```bash
python3 Main.py -f <world_file> [-v] [-d]
```

Or to run on multiple worlds:

```bash
python3 Main.py -f <directory_path> [-v] [-d]
```

### Options

- `-f`, `-F`: Specify file or directory name
- `-m`, `-M`: Enable ManualAI mode (human player)
- `-r`, `-R`: Enable RandomAI mode
- `-v`, `-V`: Enable verbose mode
- `-d`, `-D`: Enable debug mode

### Generating Test Worlds

```bash
python3 WorldGenerator.py <numFiles> <filename> <rowDimension> <colDimension> <numMines>
```

## Requirements

- Python 3.x
- NumPy (for the Final AI implementation)
