import sys
import numpy as np
from collections import defaultdict

"""
How to run:

python3 ttc.py [input_filename]

For instance, for the test document, try running
"python3 ttc.py test"

"""

def load():
	"""
	Loads data from an input file; the name of the input file is passed as a command-line argument.
	You can assume that this will correctly load data

	Input: 
		There are a total of n agents in the system = lines in the file.
		Line i (ranging from 0 to n-1) contains the preferences of agent i
		Assume that agent i owns item i

	Output: 

		prefs = [pref_0, pref_1, pref_2, ..., pref_n],
		where each pref_i = [agent_1, ...] is agent i's preference over other agents

	"""

	try:
		with open(f"{sys.argv[1]}.txt") as infile:

			prefs = []

			data = infile.readlines()

			for line in data:
				prefs.append([int(x) for x in line.strip('\n').split(',')])

			return prefs
	except:
		sys.exit("Please provide input file as command-line argument")

def prettyprint(all_trades):
	"""
	Input: all_trades = dictionary of {agent: who they traded with}
	Output: nicely formatted trading outcomes
	
	"""

	for agent in range(len(all_trades)):
		print(f"agent {agent} <- agent {all_trades[agent]}'s item")


class DirectedGraph:
    def __init__(self):
        self.adj_list = {}
        self.dic = {}

    def add_edge(self, source, target):
        if source not in self.adj_list:
            self.adj_list[source] = []
        self.adj_list[source].append(target)

    def is_empty(self):
        return len(self.adj_list) == 0

    def has_cycle(self):
        visited = set()
        stack = set()
        cycle = []

        def dfs(node):
            visited.add(node)
            stack.add(node)
            for neighbor in self.adj_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    nonlocal cycle
                    cycle = list(stack)
                    cycle.append(neighbor)
                    return True
            stack.remove(node)
            return False

        for node in self.adj_list:
            if node not in visited:
                if dfs(node):
                    return cycle[::-1]
        return False

    def show_graph(self):
        for node in self.adj_list:
            print(f"{node} -> {self.adj_list[node]}")

    def show_circular_edges(self):
        visited = set()
        cycles = []
        for node in self.adj_list:
            if node not in visited:
                cycle = self._dfs_for_cycles(node, visited, [])
                if cycle is not None:
                    cycles.append(cycle)
        for cycle in cycles:
            prev_node = cycle[-1]
            for node in cycle:
                if node == prev_node:
                    continue
                # print(f"{prev_node} -> {node}")
                self.dic[prev_node] = node
                prev_node = node
            if cycle[0] == cycle[-1]:
                self.dic[cycle[-1]] = cycle[-1]
                # print(f"{cycle[-1]} -> {cycle[-1]}")
        return self.dic

    def _dfs_for_cycles(self, node, visited, stack):
        visited.add(node)
        stack.append(node)
        for neighbor in self.adj_list.get(node, []):
            if neighbor not in visited:
                cycle = self._dfs_for_cycles(neighbor, visited, stack)
                if cycle is not None:
                    return cycle
            elif neighbor in stack:
                index = stack.index(neighbor)
                return stack[index:]
        stack.pop()
        return None

def ttc(prefs):
    n = len(prefs)
    all_trades = {}
    flag = [0]*n
    ROUND = 0

    while all(flag) != True:
        # remain = flag.count(0)
        graph = DirectedGraph()
        for i in range(n):
            if flag[i] == 0:
                graph.add_edge(i, prefs[i][ROUND])
            else: continue
        ROUND += 1
        all_trades.update(graph.show_circular_edges())
        for key in all_trades.keys(): flag[key] = 1

    return all_trades


def main():
	prefs = load()
	# print(prefs)
	all_trades = ttc(prefs)
	prettyprint(all_trades)


if __name__ == "__main__":
	main()


"""

Output for test.txt 

agent 0 <- agent 0's item
agent 1 <- agent 1's item
agent 2 <- agent 3's item
agent 3 <- agent 2's item

"""


