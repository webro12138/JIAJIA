from copy import deepcopy
import networkx as nx
from algorithm import AlgorithmBase

class NCVoteRank(AlgorithmBase):

    def __init__(self, theta, verbose=True):
        super().__init__()
        self.theta = theta
        self._verbose=verbose
    def run(self, network, k):
        
        network._graph.remove_edges_from(nx.selfloop_edges(network._graph))
        ad = network.average_degree()
        self._ks = self.k_shell(network)
        ab = {}
        for node in network.nodes():
            ab[node] = [0, 1]
    
        S = []
        for _ in range(k):
            candidate = set(network.nodes()) - set(S)
            for node in candidate:
                neighours = list(set(network[node]) - set(S))
                for neighour in neighours:
                    ab[node][0] += ab[neighour][1] * self.NC(network, neighour)\
                    * (1 - self.theta) + ab[neighour][1] * self.theta
    
            max_value = 0
            max_node = 0
            for node in ab:
                if(ab[node][0] > max_value):
                    max_value = ab[node][0]
                    max_node = node
        
            S.append(max_node)
            ab[max_node][1] = 0
            ab[max_node][0] = 0
            neighours = list(network[max_node])
            for neighour in neighours:
                if(ab[neighour][1] > 1 / ad):
                    ab[neighour][1] -= 1 / ad 
                tnei = list(set(network[neighour]) - set(S))
                for nei in tnei:
                    if(ab[nei][1] > 1 / (ad * 2)):
                        ab[nei][1] -= 1 / (ad * 2)  
        return S
    def k_shell(self, network):
        # 为了不改变原图
        graph = network._graph.copy()

        k_shells = {}
        # k从最小度开始
        degrees = (graph.degree[n] for n in graph.nodes())
        k = min(degrees)

        while nx.number_of_nodes(graph):

            node_k_shell = []

            nodes_degree = {n: graph.degree[n] for n in graph.nodes()}

            # 每次删除度值最小的节点而不能删除度为ks的节点否则产生死循环。https://neusncp.com/user/blog?id=242
            k_min = min(nodes_degree.values())

            #是否还存在度为k_min的节点
            flag = True

            while (flag):
                nodes_degree = {n: graph.degree[n] for n in graph.nodes()}
                for ke,va in nodes_degree.items():

                    if (va == k_min):
                        node_k_shell.append(ke)
                        graph.remove_node(ke)

                nodes_degree_check = {n: graph.degree[n] for n in graph.nodes()}

                # 检查图中是否存在度为kmin的节点
                if k_min not in nodes_degree_check.values():
                    flag = False

            for node in node_k_shell:
                k_shells[node] = k
        
            k += 1
    
        max_value = max(k_shells.items(), key=lambda x:x[1])
        min_value = min(k_shells.items(), key=lambda x:x[1])

        for key in k_shells:
            k_shells[key] = (k_shells[key] - min_value[1])/(max_value[1] - min_value[1])
    
        return k_shells 
    
    def NC(self, network, node):
        value = 0
        neighbors = network[node]
        for node in neighbors:
            value += self._ks[node]
        return value