import percolation
import time

class ooshbot69:
	# These are "static methods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.

    # 1) Choosing neighbors of currently colored vertices with the most connections and forming a path between
    # your own color 
    # 2) Avoiding any isolated verticies and attempting to force the opponent to choose it
    def ChooseVertexToColor(graph, active_player):
        start = time.time()
        ours, not_ours, uncolored = ooshbot69.getColor(graph, active_player)
        scores = []                 # list of [vertex, score]; higher score is better
        a = -3                      # Penalty for not being a neighbor of one of our vertices

        # Neighbors of current vertices with high degree
        all_neighbors = []
        for v in ours:
            all_neighbors.extend([u for u in graph.GetNeighbors(v)])
        scores = [[u, graph.Degree(u)] for u in all_neighbors if u.color == -1]

        # Not neighbors of current vertices with high degree
        scores.extend([[u, graph.Degree(u)+a] for u in uncolored if (u not in all_neighbors and u.color == -1)])

        # Choose vertex with highest score
        scores.sort(key = lambda x: x[1])
        chosen = scores[-1][0]
        return chosen

    # Initial Strategies: 
    # 1) Choose the one that has the fewest number of connections to our vertices
    def ChooseVertexToRemove(graph, active_player):
        ours, not_ours, uncolored = ooshbot69.getColor(graph, active_player)
        if len(uncolored) != 0:
            print("Error")
        b = 0.5
        scores = []
        for v in ours: 
            connections = graph.IncidentEdges(v)
            friendly = len(list(filter(lambda x: x.a in ours and x.b in ours, connections)))
            opp = len(connections) - friendly
            score = b*(opp) -(friendly)
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