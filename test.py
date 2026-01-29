def test_search_agent(agent):
    """Run all search algorithms on the agent's grid and print results."""
    results = {}

    print("\n--- BFS ---")
    res_bfs = agent.bfs()
    results["BFS"] = res_bfs
    if res_bfs:
        print(f"Path Length: {res_bfs[0]} steps")
        print(f"Nodes Expanded: {res_bfs[1]}")
        print(f"Total Cost: {res_bfs[2]}")

    print("\n--- DFS ---")
    res_dfs = agent.dfs()
    results["DFS"] = res_dfs
    if res_dfs:
        print(f"Path Length: {res_dfs[0]} steps")
        print(f"Nodes Expanded: {res_dfs[1]}")
        print(f"Total Cost: {res_dfs[2]}")

    print("\n--- UCS ---")
    res_ucs = agent.ucs()
    results["UCS"] = res_ucs
    if res_ucs:
        print(f"Path Length: {res_ucs[0]} steps")
        print(f"Nodes Expanded: {res_ucs[1]}")
        print(f"Total Cost: {res_ucs[2]}")

    print("\n--- A* ---")
    res_astar = agent.astar()
    results["A*"] = res_astar
    if res_astar:
        print(f"Path Length: {res_astar[0]} steps")
        print(f"Nodes Expanded: {res_astar[1]}")
        print(f"Total Cost: {res_astar[2]}")

    return results
