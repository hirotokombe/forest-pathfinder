from forest import generate_forest_15x15, print_forest
from agent import SearchAgent
from test import test_search_agent

forest = generate_forest_15x15(seed=42)

agent = SearchAgent((0, 0), (14, 14), forest)

print_forest(forest)
test_search_agent(agent)

