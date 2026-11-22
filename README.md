# Forest Pathfinding Visualizer

A Python pathfinding project that compares **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Uniform Cost Search (UCS)**, and **A\*** in a randomly generated forest. The environment contains walls and traversable fire zones with different movement costs, so **the route with the fewest steps is not always the route with the lowest cost**.

Each algorithm runs on the same forest, prints its chosen route, reports search statistics, and produces an **animated GIF of an agent following the completed path**.

## Features

- Generate a reproducible **15 × 15** forest with adjustable obstacle and fire probabilities.
- Compare four classic search algorithms on the same environment.
- Move in four directions: **up, down, left, and right** (no diagonals).
- Navigate around walls and account for the higher cost of stepping into fire.
- Measure **path length**, **nodes expanded**, and **total traversal cost**.
- Print each path in the terminal and export animated GIFs using **Pillow**.

## Forest Legend

| Symbol | Tile | Cost to enter |
|:---:|---|:---:|
| `S` | Start | Not counted initially |
| `*` | Goal | 1 |
| `.` | Open ground | 1 |
| `f` | Small fire | 3 |
| `F` | Large fire | 5 |
| `#` | Obstacle / wall | Impassable |
| `P` | Path marker (terminal output only) | Depends on the original tile |

All fire tiles are **passable**, just more expensive than open ground. The total cost sums the costs of cells entered along the path, excluding the initial start cell.

## Algorithms

| Algorithm | Strategy | Path guarantee |
|---|---|---|
| **BFS** | Uses a FIFO queue to explore cells layer by layer. | Fewest steps, but not necessarily lowest cost. |
| **DFS** | Uses a LIFO stack to explore one branch deeply before others. | Finds a valid route if one exists; not necessarily shortest or cheapest. |
| **UCS** | Uses a min-heap to prioritize the smallest accumulated cost `g(n)`. | Lowest total cost with the project's positive step costs. |
| **A\*** | Uses a min-heap ordered by `f(n) = g(n) + h(n)`. | Lowest total cost with the default admissible Manhattan heuristic. |

**A\*** uses Manhattan distance by default:

```text
h(n) = abs(current_row - goal_row) + abs(current_col - goal_col)
```

Since movement is limited to four directions and every move costs at least 1, this estimate never overstates the remaining cost. A custom heuristic can be supplied via `agent.astar(heuristic=...)`; optimality depends on its properties.

## Project Structure

```text
.
├── agent.py        # SearchAgent: BFS, DFS, UCS, and A*
├── forest.py       # Forest generation and text display
├── animation.py    # Pillow-based GIF animation
├── test.py         # Runs all four algorithms and saves their GIFs
├── main.py         # Main program / entry point
└── README.md
```

*The filenames shown match the imports in the provided Python code.*

## Getting Started

### Prerequisites

- **Python 3**
- **Pillow** — used by `animation.py` to draw and save GIF frames

Install Pillow from your project directory:

```bash
python -m pip install Pillow
```

The pathfinding and forest-generation modules otherwise use Python's standard library (`collections`, `heapq`, and `random`).

### Run

```bash
python main.py
```

The entry point generates a forest with `seed=42`, places `S` at `(0, 0)` and `*` at `(14, 14)`, then runs all four algorithms on that same grid. For each successful search, it prints a grid with `P` marking the intermediate path cells and reports:

```text
Path Length: ... steps
Nodes Expanded: ...
Total Cost: ...
```

The script also saves these files in the current working directory:

```text
bfs.gif
dfs.gif
ucs.gif
astar.gif
```

## GIF Animations

The `save_path_gif()` function in `animation.py` uses **Pillow** (`Image`, `ImageDraw`) to draw the forest and a **yellow circular agent**. Each animation frame places the agent at the next position along the algorithm's final route.

| BFS | DFS |
|---|---|
| ![BFS path animation](bfs.gif) | ![DFS path animation](dfs.gif) |

| UCS | A* |
|---|---|
| ![UCS path animation](ucs.gif) | ![A* path animation](astar.gif) |

> **These animations show the agent traversing the final path, not the order in which nodes are explored during the search.** Run the program and commit the generated GIFs alongside the README to display them on GitHub.

### Animation options

```python
from animation import save_path_gif

save_path_gif(
    grid=agent.grid,
    path=agent.last_path,
    out_path="astar.gif",
    cell=32,
    delay_ms=400,
)
```

| Argument | Purpose | Default |
|---|---|---|
| `grid` | The forest's two-dimensional tile list. | Required |
| `path` | Ordered list of `(row, col)` positions to animate. | Required |
| `out_path` | Name or location of the output GIF. | `animation.gif` |
| `cell` | Width and height of each square, in pixels. | `32` |
| `delay_ms` | Time between frames, in milliseconds. | `400` |

For the default 15 × 15 forest and `cell=32`, each frame is **480 × 480 pixels**. The GIF loops continuously.

## Example: Run a Single Algorithm

```python
from forest import generate_forest_15x15, print_forest
from agent import SearchAgent
from animation import save_path_gif

forest = generate_forest_15x15(seed=42)
print_forest(forest)

agent = SearchAgent(start=(0, 0), goal=(14, 14), grid=forest)
result = agent.astar()

if result is not None:
    path_length, nodes_expanded, total_cost = result
    print(f"Path length: {path_length} steps")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Total cost: {total_cost}")
    save_path_gif(agent.grid, agent.last_path, out_path="astar.gif")
else:
    print("No path found.")
```

Every search method returns `(path_length, nodes_expanded, total_cost)` if it succeeds, or `None` if no route exists. When successful, the resulting coordinate sequence is available in `agent.last_path`.

## Customize the Forest

You can adjust the probabilities used to generate non-start/non-goal tiles:

```python
forest = generate_forest_15x15(
    obstacle_prob=0.18,
    small_fire_prob=0.10,
    large_fire_prob=0.06,
    seed=42,
)
```

A fixed `seed` generates a repeatable environment, which makes algorithm comparisons easier. Change or omit it to explore different layouts.

**Important:** A random forest is not guaranteed to be solvable. The provided `test_search_agent()` calls `save_path_gif()` even when a search may fail, while `save_path_gif()` expects a nonempty path. For randomly generated maps, only call the animator after confirming a successful search. Also note that `SearchAgent.last_path` is not reset when a search fails, so do not reuse an old path by accident.

## What This Project Demonstrates

This simulator illustrates the difference between **minimizing the number of moves** and **minimizing weighted movement cost**. BFS can select a short route through fire, while UCS and A\* can select a longer but less costly route. DFS highlights how traversal order affects the path found. The GIFs make each algorithm's final choice easy to inspect side by side.
