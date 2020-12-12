import percolation
import time
import random

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Edge({0}, {1})".format(self.a, self.b)

def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

# Returns the degree of the given vertex.
def Degree(graph, v):
    return len(IncidentEdges(graph, v))

# Returns all neighbors of the given vertex.
def GetNeighbors(graph, v):
    edges = IncidentEdges(graph, v)
    return [u for u in graph.V if Edge(u, v) in edges or Edge(v, u) in edges]

class PercolationPlayer:
    # ooshbot69!!!
    # 1) Choosing neighbors of currently colored vertices with the most connections and forming a path between
    # your own color 
    # 2) Avoiding any isolated vertices and attempting to force the opponent to choose it
    def ChooseVertexToColor(graph, active_player):
        ours, not_ours, uncolored = PercolationPlayer.getColor(graph, active_player)
        scores = dict()               # dictionary with vertex as key and score as value
        
        # Parameter a: penalty for not being a neighbor of one of our vertices
        if len(graph.V) < 15:
            a = -2
        else:
            a = -0.5                      

        a *= len(graph.V)
        # Neighbors of current vertices with high degree
        all_neighbors = []
        for v in ours:
            all_neighbors.extend([u for u in GetNeighbors(graph, v)])

        scores.update([[u, Degree(graph, u)] for u in all_neighbors if u.color == -1])

        # Not neighbors of current vertices with high degree
        scores.update([[u, Degree(graph, u)+a] for u in uncolored if (u not in all_neighbors and u.color == -1)])

        # Increase score if it's connected to a vertex of degree 1
        for v in ours:
            isolated_neighbors = [u for u in GetNeighbors(graph, v) if Degree(graph, u) == 1]
            if len(isolated_neighbors) > 1:
                scores[v] += a

        # Choose vertex with highest score
        scores = sorted(scores.items(), key = lambda x: x[1])
        chosen = scores[-1][0]
        return chosen

    # Heuristic based on connections to friendly and opposing vertices
    def ChooseVertexToRemove(graph, active_player):
        ours, not_ours, uncolored = PercolationPlayer.getColor(graph, active_player)
        
        if len(uncolored) != 0:
            print("Error")
        if len(graph.V) < 15:
            b = 2                   # how much we value deleting opponent connections - higher is more
        else:
            b = 0.7
        b *= len(graph.V)
        scores = []
        for v in ours: 
            connections = IncidentEdges(graph, v)
            neighbors = [u for u in graph.V if Edge(u, v) in connections or Edge(v, u) in connections]
            friendly = len(list(filter(lambda x: x.a in ours and x.b in ours, connections)))
            opp = len(connections) - friendly
            score = b*(opp) -(friendly)*len(graph.V)

            # Prioritize removing extra opposing vertices if we can 
            isolated_neighbors = [u for u in neighbors if Degree(graph, u) ==1 and u in not_ours]
            if len(isolated_neighbors) > 0:
                score += b

            scores.append([v, score])

        # choose vertex with highest score
        scores.sort(key = lambda x: x[1])
        chosen = scores[-1][0]
        return chosen

    #return list of vertices that belong to BestPlayer and list of vertices that belong to 
    #other player, and a list of uncolored vertices
    def getColor(graph, active_player):
        our_vertices = []
        not_our_vertices = []
        uncolored = []
        for v in graph.V: 
            if v.color == active_player:
                our_vertices.append(v)
            elif v.color == -1:
                uncolored.append(v)
            else:
                not_our_vertices.append(v)
        return (our_vertices, not_our_vertices, uncolored)