
import networkx as nx
from algorithm import AlgorithmBase
class DegreeDiscount(AlgorithmBase):
    def __init__(self, verbose=True):
        super().__init__()
        self._verbose = verbose
    
    def run(self, network, k:int):
        assert network.is_weighted(), "网络的边上没有被赋予激活概率，请使用Weighter对其加权"
        dv = dict(nx.degree(network._graph, weight="weight"))
        ddv = dv.copy()
        tv = dict() 
        S = []
        for _ in range(k):
            s = max(ddv.items(), key = lambda x:x[1])[0]
            S.append(s)
            ddv.pop(s)
            neighbors = network[s]
        
            for neighbor in list(set(neighbors) - set(S)):
                tv[neighbor] = tv.setdefault(neighbor, 0) + network[s][neighbor]['weight']
                ddv[neighbor] = dv[neighbor] - 2 * tv[neighbor] - (dv[neighbor] - tv[neighbor]) * tv[neighbor] * network[s][neighbor]['weight']   
        return S