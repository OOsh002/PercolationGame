import percolation

class BestPlayer:
	# These are "static methods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        ours, not_ours, uncolored = getColor(graph, active_player)
        all_neighbors = []
        if len(ours) == 0:
            all_neighbors = uncolored
        else:
            for v in ours:
                all_neighbors.extend(graph.GetNeighbors(v))
        all_neighbors.sort(key=lambda x: graph.Degree(x))
        chosen = all_neighbors[-1]
        return chosen

        # Initial Strategies: 
        # 1) Choosing neighbors of currently colored vertices with the most connections and forming a path between
        # your own color 
        # 2) Avoiding any isolated verticies and attempting to force the opponent to choose it

    def ChooseVertexToRemove(graph, active_player):
        return random.choice([v for v in graph.V if v.color == active_player])

        # Initial Strategies: 
        # 1) Erasing down the path instead of the middle of it (making sure that there
        # are no connections of the same color next to the vertex being erased)

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

k = 4; p = 0.5
G = percolation.BinomialRandomGraph(k, p)
ChooseVertexToColor(G, 2)