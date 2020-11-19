import percolation

class BestPlayer
	# These are "static methods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        return random.choice([v for v in graph.V if v.color == -1])
       	vertex_colors = getColor(graph, active_player)
       	

        # Initial Strategies: 
        # 1) Choosing neighbors with the most connections and forming a path between
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
    	l = [[], [], []]
    	for v in graph.V: 
    		if v.color == active_player:
    			l[0].append(v)
    		elif v.color == -1:
    			l[2].append(v)
    		else:
    			l[1].append(v)
    	return l