import percolation
import time
# Returns the degree of the given vertex.
def Degree(graph, v):
    return len(graph.IncidentEdges(v))

# Returns all neighbors of the given vertex.
def GetNeighbors(graph, v):
    edges = graph.IncidentEdges(v)
    return [u for u in graph.V if percolation.Edge(u, v) in edges or percolation.Edge(v, u) in edges]

class PercolationPlayer:
    # OOSHBOT69
	# These are "static methods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.

    # 1) Choosing neighbors of currently colored vertices with the most connections and forming a path between
    # your own color 
    # 2) Avoiding any isolated vertices and attempting to force the opponent to choose it
    def ChooseVertexToColor(graph, active_player, a=-3):
        start = time.time()
        ours, not_ours, uncolored = ooshbot69.getColor(graph, active_player)
        scores = []                 # list of [vertex, score]; higher score is better
        if len(graph.V) < 15:
            a = -2
        else:
            a = -0.5                      # Penalty for not being a neighbor of one of our vertices

        a *= len(graph.V)
        # Neighbors of current vertices with high degree
        all_neighbors = []
        for v in ours:
            all_neighbors.extend([u for u in GetNeighbors(graph, v)])

        scores = dict([[u, Degree(graph, u)] for u in all_neighbors if u.color == -1])

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

    # parity?
    # Initial Strategies: 
    # 1) Choose the one that has the fewest number of connections to our vertices
    def ChooseVertexToRemove(graph, active_player, b=0.5):
        ours, not_ours, uncolored = ooshbot69.getColor(graph, active_player)
        should_remove = False
        if len(ours) < len(not_ours):
            should_remove = True
        if len(uncolored) != 0:
            print("Error")
        if len(graph.V) < 15:
            b = 2                   # how much we value deleting opponent connections - higher is more
        else:
            b = 0.9
        b *= len(graph.V)
        scores = []
        for v in ours: 
            connections = graph.IncidentEdges(v)
            neighbors = [u for u in graph.V if percolation.Edge(u, v) in connections or percolation.Edge(v, u) in connections]
            friendly = len(list(filter(lambda x: x.a in ours and x.b in ours, connections)))
            opp = len(connections) - friendly
            score = b*(opp) -(friendly)*len(graph.V)

            isolated_neighbors = [u for u in neighbors if Degree(graph, u) ==1 ]
            if len([u for u in isolated_neighbors if u in not_ours]) > 0:
                score += b
            if should_remove == True and len(isolated_neighbors) % 2 == 1:
                score  += b
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

# k = 4; p = 0.5
# G = percolation.BinomialRandomGraph(k, p)
# for v in G.V:
#     print(v, G.Degree(v))
# v = ooshbot69.ChooseVertexToColor(G, 2)
# print(v)