from network import Network
import networkx as nx

class TSLN(Network):
    ## life_time 给定的是每条边存在的范围，例如{"1":{"2":(1, 2)}}表示的是边(1, 2)在[1, 2]的范围内存在
    def __init__(self, graph, life_time):
        super().__init__()
        if(type(graph) == nx.Graph):
            self.gtype="indirected"
        if(type(graph) == nx.DiGraph):
            self.gtype="directed"
        self._graph = graph
        self._life_time = life_time

    def set_life_time(self, life_time):
        assert isinstance(life_time, dict), "life_time必须是一个dict"
        self._life_time = life_time

    def number_of_edges(self):
        return self._graph.number_of_edges()
    
    def number_of_edges_at_t(self, t):
        result = 0
        for node1, node2 in self._graph.edges():
            if self._life_time[node1][node2][0] <= t and  self._life_time[node1][node2][0] >= t:
                result = result + 1
        return result

    def number_of_nodes(self):
        return self._graph.number_of_nodes()


    def edges(self):
        return list(self._graph.edges)
    
    def edges_at_t(self, t):
        result = []
        for node1, node2 in self._graph.edges():
            if self._life_time[node1][node2][0] <= t and  self._life_time[node1][node2][0] >= t:
                result.append((node1, node2))
        return result

    def nodes(self):
        return list(self._graph.nodes)

    def __getitem__(self, key):
        return self._graph[key]

    def __setitem__(self, key, value):
        self._graph[key] = value
    
    def degrees(self, banch=None, t=1, type="at_t"):
        assert type in ["at_t", "all"], "type must be at_t or all"

        if(type == "at_t"):
            assert t != None, "t must be specified"
            degrees_dict = {}
            if(banch == None):
                banch = self.nodes()

            if(isinstance(banch, list)):

                for node in banch:
                    degrees_dict[node] = len(self._graph[node])
        
                return degrees_dict

            else:
                return len(self._graph[banch])
        else:
            return self.degrees_at_t(t)
        
    def degrees_at_t(self, t, banch=None):
        degrees_dict = {}
        if(banch == None):
            banch = self.nodes()

        if(isinstance(banch, list)):
            for node in banch:
                degrees_dict[node] = len(self.neighbors_at_t(banch, t))
            return degrees_dict[node]
        else:
            return len(self.neighbors_at_t(banch, t))
        
    def neighbors(self, nodes, t=1, type="at_t"):
        assert type in ["at_t", "all"], "type must be at_t or all"
        if(type == "all"):
            if(isinstance(nodes, list)):
                neis = []
                for node in nodes:
                    neis += list(self._graph[node])
                return neis
            else:
                return self._graph[nodes]
        else:
            assert t != None, "t must be specified"
            return self.neighbors_at_t(nodes, t)

    def neighbors_at_t(self, nodes, t):
        
        if(not isinstance(nodes, list)):
            nodes = [nodes]
            neis_at_t = []
            for node in nodes:
                neis = list(self._graph[node])
                for nei in neis:
                    if(self._life_time[node][nei][0] >=t and self._life_time[node][nei][0] <=t):
                        neis_at_t.append(nei)
        if(not isinstance(nodes, list)):
            return neis_at_t[0]
        else:
            return neis_at_t
