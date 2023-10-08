import random
from diffusionModel.DiffusionBase import DiffusionBase
from tqdm import tqdm
from diffusionModel import Weighter
import numpy as np

class MLICWeighter(Weighter):

    def __init__(self, APType="fixed_fixed",  inter_p = [], intra_p = [], inter_range = [], intra_range = [], seed = None):
        super(Weighter, self)
        assert APType in ["fixed_fixed", "random_fixed", "fixed_random", "random_random"], "APType的值只能是'fixed_fixed', 'random_fixed', 'fixed_random', 'random_random'"
        self._APType = APType
        self._inter_p = inter_p
        self._intra_p = intra_p
        self._inter_range = inter_range
        self._intra_range = intra_range
        self._seed = seed
    
    def assign_active_prob(self, network):
        assert network.number_of_layers() > 0, "网络中没有层"
        if(self._seed != None):
            np.random.seed(self._seed)
        aptype = self._APType.split("_")[0]
        
        if(aptype == "fixed"):
            for i in range(network.number_of_layers()):
                for node1, node2 in network.layers[i].edges():
                    if(isinstance(self._inter_p, list)):
                        network.layers[i][node1][node2]["weight"] = self._inter_p[i]
                    else:
                        network.layers[i][node1][node2]["weight"] = self._inter_p

        if(aptype == "random"):
            for i in range(network.number_of_layers()):
                for node1, node2 in network.layers[i].edges():
                    if(isinstance(self._inter_range, list)):
                        network.layers[i][node1][node2]["weight"] = np.random.uniform(self._inter_range[i][0], self._inter_range[i][1])
                    else:
                        network.layers[i][node1][node2]["weight"] = np.random.uniform(self._inter_range[0], self._inter_range[1])
    
    def assign_active_threhsold(self, network):
        assert network.number_of_layers() > 0, "网络中没有层"
        if(self._seed != None):
            np.random.seed(self._seed)
        aptype = self._APType.split("_")[1]
        if(aptype == "fixed"):
            if(network.number_of_layers() != 1):
                    for i in range(network.number_of_layers()):
                        for node in network.layers[i]:
                            if(isinstance(self._intra_p, list)):
                                network.layers[i].nodes[node]["threshold"] = self._intra_p[i]
                            else:
                                network.layers[i].nodes[node]["threshold"] = self._intra_p
            
        if(aptype == "random"):
            if(network.number_of_layers() != 1):
                    for i in range(network.number_of_layers()):
                        for node in network.layers[i]:
                            if(isinstance(self._intra_range, list)):
                                network.layers[i].nodes[node]["threshold"] = np.random.uniform(self._intra_range[i][0], self._intra_range[i][1])
                            else:
                                network.layers[i].nodes[node]["threshold"] = np.random.uniform(self._intra_range[0], self._intra_range[1])

    def get_threshold(self, network, layer_num, node):
        return network.layers[layer_num].nodes[node]["threshold"]
    
    def get_active_prob(self, network, layer_num, edge):
        return network.layers[layer_num][edge[0]][edge[1]]["weight"]
    
class MLIC(DiffusionBase):

    def __init__(self, weighter=None, MC=10000, verbose=True):
        super().__init__()
        self._S = []
        self._weighter = weighter
        self._MC = MC
        self._verbose = verbose
        self._network = None
    
    def simulate(self, network, S):
        self.set_network(network)
        self.set_S(S)
        self._weighter.assign_weights(self._network)
        
        if self._verbose:
            loops = tqdm(range(self._MC))
        else:
            loops = range(self._MC)

        influence_spread = 0
        for i in loops:
            influence_spread += self.step()
            if self._verbose:
                loops.set_description("传播模拟")
        influence_spread = influence_spread / self._MC
     
        return influence_spread
    
    def step(self):
            new_active = [self._S[:] for _ in range(self._network.number_of_layers())]
            A = [self._S[:] for _ in range(self._network.number_of_layers())]
            condition = True
            
            while condition:
                new_ones = [[] for _ in range(self._network.number_of_layers())]
                for i in range(self._network.number_of_layers()):
                    for s in new_active[i]:
                        neighbors = list(set(self._network.single_layer_neigbors(i, s)) - set(A[i]))
                        for neighbor in neighbors:
                       
                            if(self._weighter.get_active_prob(self._network, i, (s, neighbor)) > random.uniform(0, 1)):
                                new_ones[i].append(neighbor)
                                for j in range(self._network.number_of_layers()):
                                    if(j != i and neighbor not in new_ones[j]):
                                        if(random.uniform(0, 1) < self._weighter.get_threshold(self._network, j, neighbor)):
                                            new_ones[j].append(neighbor)
                for i in range(self._network.number_of_layers()):
                    new_active[i] = list(set(new_ones[i]) - set(A[i]))
                    A[i] += new_active[i]
                

                condition = False
                for active in new_active:
                    if(len(active) != 0):
                        condition = True

            temp = []
            for i in range(self._network.number_of_layers()):
                temp += A[i] 
            
            return len(set(temp))
    
    def approx_func(self, network, S):
        self.set_network(network)
        self.set_S(S)
        self._weighter.assign_weights(self._network)

        inactive_pro = [{} for _ in range(self._network.number_of_layers())]
        for i in range(self._network.number_of_layers()):
            neighbors = set().union(*[set(self._network.layers[i][node]) for node in self._S])
            for node in self._network.layers[i]:
                if node not in self._S and node in neighbors:
                    inactive_pro[i][node] = self.inactive_probability(self._network, node, i, self._S)
    
        edv = len(self._S)
    
        p = {}
        for j in range(self._network.number_of_layers()):
            for key in inactive_pro[j].keys():
                p[key] = p.setdefault(key, 1) * inactive_pro[j][key]
    

        for key in p:
            edv += 1 - p[key]

        return edv
    
    def inactive_probability(self, mln, node, layer, S):
        if(mln.gtype=="directed"):
            neighbors = list(mln.layers[layer].predecessors(node))
        else:
            neighbors = list(mln.layers[layer][node])
            
        prob = 1.0
        for neighbor in neighbors:
            if(neighbor in S):
                weight = mln.layers[layer][neighbor][node]["weight"]
                prob *= (1 - weight)
    
        return prob