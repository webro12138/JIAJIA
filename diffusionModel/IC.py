from diffusionModel import DiffusionBase, Weighter
import random
from tqdm import tqdm

class ICWeighter(Weighter):

    def __init__(self, APType="random", p=None):
        super(Weighter, self)
        assert APType in ["uniform", "random"], "APType的值只能时'random'或'uniform'"
        self._APType = APType
        self._p = p
    


    def assign_active_prob(self, network):
            if(self._APType == "random"):
                for node1, node2 in network.edges():
                    network[node1][node2]["weight"] = random.uniform(self._p[0], self._p[1])
            if(self._APType == "uniform"):
                for node1, node2 in network.edges():
                    network[node1][node2]["weight"] = self._p

    def get_active_prob(self, network, edge):
        return network[edge[0]][edge[1]]["weight"] 

class IC(DiffusionBase):

    def __init__(self, weighter=None, MC=10000, verbose=True):
        super().__init__()
        self._S = []
        self._weighter = weighter
        self._MC = MC
        self._verbose = verbose
        self._network = None

    def simulate(self, network, S):
        self._network = network
        self._S = S
        self._weighter.assign_weights(network)

        if self._verbose:
            loops = tqdm(range(self._MC))
        else:
            loops = range(self._MC)

        influence_spread = 0
        for _ in loops:
            influence_spread += self.step()
            if self._verbose:
                loops.set_description("传播模拟")
        influence_spread = influence_spread / self._MC

        return influence_spread
    
    def gen_weighter(self, APType="uniform", p=0):
        assert self._network != None, "网络为空，请先使用set_network函数置入网络"
        self._weighter = ICWeighter(APType, p)
        self._weighter.gen_active_prob(self._network)

    def step(self):
        A, new_active = self._S[:], self._S[:]
        while new_active:
            one_active = []
            for node in new_active:
                neigbours = list(self._network[node])
                for nei in neigbours:
                    if(self._weighter.get_active_prob(self._network, (node, nei)) > random.uniform(0, 1)):
                        one_active.append(nei)
            new_active = list(set(one_active) - set(A))
            A += new_active
        
        return len(A)
        
    def inactive_probability(self, node):
        if(self._network.gtype=="directed"):
            neighbors = list(self._network.predecessors(node))
        else:
            neighbors = list(self._network[node])
        prob = 1.0
        for neighbor in neighbors:
            if(neighbor in self._S):
                weight = self._network[neighbor][node]["weight"]
                prob *= (1 - weight)
        return prob
    
    def approx_func(self, network, S):
        self.set_network(network)
        self.set_S(S)
        self._weighter.assign_weights(self._network)
        neighbors = self._network.neighbors(S)
        
        edv = len(self._S)
        for node in self._network.nodes():
            if node not in self._S and node in neighbors:
                edv += 1 - self.inactive_probability(node)
      
        return edv