import random
import itertools
import copy
import sys
import traceback

import time
import signal
import errno
import percolator

class Vertex:
    def __init__(self, index, color=-1):
        self.index = index
        self.color = color

    def __repr__(self):
        if self.color == -1:
            return "Vertex({0})".format(self.index)
        else:
            return "Vertex({0}, {1})".format(self.index, self.color)


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Edge({0}, {1})".format(self.a, self.b)


class Graph:
    def __init__(self, v, e):
        self.V = set(v)
        self.E = set(e)

    def __repr__(self):
        return "Graph({0}, {1})".format(self.V, self.E)

    def __deepcopy__(self, memo):
        V = {v.index: Vertex(v.index, v.color) for v in self.V}
        E = [Edge(V[e.a.index], V[e.b.index]) for e in self.E]
        return Graph(V.values(), E)

### DO NOT RELY ON THESE METHODS IN YOUR CODE! THEY WILL NOT NECESSARILY EXIST! ###
### THESE ARE BEING USED FOR DRIVER CODE ONLY ###

# Gets a vertex with given index if it exists, else return None.
def GetVertex(graph, i):
    for v in graph.V:
        if v.index == i:
            return v
    return None

# Returns the incident edges on a vertex.
def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

# modified random player class
# modified the play method to pass in a and b
# Removes the given vertex v from the graph, as well as the edges attached to it.
# Removes all isolated vertices from the graph as well.
def Percolate(graph, v):
    # Get attached edges to this vertex, remove them.
    for e in IncidentEdges(graph, v):
        graph.E.remove(e)
    # Remove this vertex.
    graph.V.remove(v)
    # Remove all isolated vertices.
    to_remove = {u for u in graph.V if len(IncidentEdges(graph, u)) == 0}
    graph.V.difference_update(to_remove)

class TimeoutError(Exception):
    pass

class Timeout:
    def __init__(self, seconds=0.5, error_message="Timeout of {0} seconds hit"):
        self.seconds = seconds
        self.error_message = error_message.format(seconds)
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


# This is the main game loop.
def PlayGraph(s, t, graph):
    players = [s, t]
    active_player = 0

    # Phase 1: Coloring Phase
    while any(v.color == -1 for v in graph.V):
        # First, try to just *run* the player's code to get their vertex.
        try:
            with Timeout():
                chosen_vertex = players[active_player].ChooseVertexToColor(copy.deepcopy(graph), active_player)

        # If user code does not return within appropriate timeout, select random action.
        except TimeoutError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            chosen_vertex = RandomPlayer.ChooseVertexToColor(copy.deepcopy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = GetVertex(graph, chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != -1:
                return 1 - active_player
            # If output is reasonable, color this vertex.
            original_vertex.color = active_player
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player

        # Swap current player.
        active_player = 1 - active_player

    # Check that all vertices are colored now.
    assert all(v.color != -1 for v in graph.V)

    # Phase 2: Removal phase
    # Continue while both players have vertices left to remove.
    while len([v for v in graph.V if v.color == active_player]) > 0:
        # First, try to just *run* the removal code.
        try:
            with Timeout():
                chosen_vertex = players[active_player].ChooseVertexToRemove(copy.deepcopy(graph), active_player)

        # If user code does not return within appropriate timeout, select random action.
        except TimeoutError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            chosen_vertex = RandomPlayer.ChooseVertexToRemove(copy.deepcopy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = GetVertex(graph, chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != active_player:
                return 1 - active_player
            # If output is reasonable, remove ("percolate") this vertex + edges attached to it, as well as isolated vertices.
            Percolate(graph, original_vertex)
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Swap current player
        active_player = 1 - active_player

    # Winner is the non-active player.
    return 1 - active_player


# This method generates a binomial random graph with 2k vertices
# having probability p of an edge between each pair of vertices.
def BinomialRandomGraph(k, p):
    v = {Vertex(i) for i in range(2 * k)}
    e = {Edge(a, b) for (a, b) in itertools.combinations(v, 2) if random.random() < p}
    return Graph(v, e)


# This method creates and plays a number of random graphs using both passed in players.
def PlayBenchmark(p1, p2, iters):
    graphs = (
        BinomialRandomGraph(random.randint(1, 20), random.random())
        for _ in range(iters)
    )
    wins = [0, 0]
    for graph in graphs:
        g1 = copy.deepcopy(graph)
        g2 = copy.deepcopy(graph)
        # Each player gets a chance to go first on each graph.
        winner_a = PlayGraph(p1, p2, g1)
        wins[winner_a] += 1
        winner_b = PlayGraph(p2, p1, g2)
        wins[1-winner_b] += 1
    return wins


# This is a player that plays a legal move at random.
class RandomPlayer:
    # These are "static methdods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        return random.choice([v for v in graph.V if v.color == -1])

    def ChooseVertexToRemove(graph, active_player):
        return random.choice([v for v in graph.V if v.color == active_player])


# This is a player that plays a legal move at random.
class RandomPlayer:
    # These are "static methods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player, a=0):
        return random.choice([v for v in graph.V if v.color == -1])

        # Initial Strategies: 
        # 1) Choosing neighbors with the most conections and forming a path between
        # your own color 
        # 2) Avoiding any isolated verticies and attempting to force the opponent to choose it

    def ChooseVertexToRemove(graph, active_player, b=0):
        return random.choice([v for v in graph.V if v.color == active_player])

        # Initial Strategies: 
        # 1) Erasing down the path instead of the middle of it (making sure that there
        # are no connections of the same color next to the vertex being erased)


if __name__ == "__main__":
    # NOTE: we are not creating INSTANCES of these classes, we're defining the players
    # as the class itself. This lets us call the static methods.
    p1 = RandomPlayer
    p2 = percolator.PercolationPlayer
    iters = 100
    winrates = []
    for i in range(5):
        wins = PlayBenchmark(p1, p2, iters)
        print(wins)
        print(
            "Player 1: {0} Player 2: {1}".format(
                1.0 * wins[0] / sum(wins), 1.0 * wins[1] / sum(wins)
            )
        )
        winrates.append(1.0 * wins[1] / sum(wins))
    print("Average: " + str(sum(winrates)/5))

# -0.25, 2
# -0.5, 0.9
# -3, 0.9
# -3, 2
# -5, 0.5
# -5, 0.9
# -10, 0.9