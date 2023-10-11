from algorithm import AlgorithmBase
from tqdm import tqdm
from utils import save_json, load_json
from copy import deepcopy
import networkx as nx
import numpy as np
import random
 
class SAW_ASA(AlgorithmBase):
    def __init__(self, diffusion_model, beta=0.4, T_h=1800, T_f=20, theta=5, features_save_path=None, features_read_path=None, verbose=True):
        super().__init__()
        self._diffusion_model = diffusion_model
        self._diffusion_model.set_verbose(False)
        self._beta = beta
        self._features_save_path = features_save_path
        self._features_read_path = features_read_path
        self._T_h = T_h
        self._T_f= T_f
        self._theta = theta
        self._verbose = verbose
        
    
    def set_setting(self, network, k):
        self.network = network
        self.k = k

    def run(self, network, k):
        self.set_setting(network, k)
        if(self._features_read_path):
            features = load_json(self._features_read_path)
            print("特征读取成功")
        else:
            features = extract_centrality()
            if(self._features_save_path):
                save_json(features)
                print("特征保存成功")
        
        rank = self.node_ranking(features)
        candidate_pool = self.candidate_pool_selection(rank)
        S = self.simulated_annealing(candidate_pool)
        return S

    def simulated_annealing(self, candidate_pool):
        r = 0
        S = candidate_pool[0:self.k]
        influence_spread = EDV(G, S)
        new_S = deepcopy(S)
        new_influence_spread = 0
        while(T_h > T_f):
            for _ in range(20):
                C = set(candidate_pool) - set(S)
                s = random.choice(list(C))
                index = random.choice(list(range(len(S))))
                temp = new_S[index] 
                new_S[index] = s
                new_influence_spread = self._diffusion_model.approx_func(self.network, new_S)
                if(new_influence_spread > influence_spread):
                    S[index] = s
                    influence_spread = new_influence_spread
                    r = 0
                else:
                    new_S[index] = temp
                    r += 1   
            self._T_h = self._T_h - self._theta * np.log(r + 1)
            if(self._verbose):
                print(f"正在进行模拟退火|fitness:{influence_spread:.4f}        ", end="\r")
            
        return S

    def candidate_pool_selection(self, rank):
        n = self.network.number_of_nodes() 
        number_of_candidate_nodes = int(np.ceil(self.k + (n - self.k) * np.power(self._beta * self.k / n, 1 - self._beta)))
        allNodes = list(self.network.nodes())
        score = {}
        for i in range(n):
            score[allNodes[i]] = rank
    
        score = sorted(score.items(), key=lambda x:x[1], reverse=True)
    
        candidate_pool = []
    
        for i in range(number_of_candidate_nodes):
            candidate_pool.append(score[i][0])
        return candidate_pool

    def node_ranking(self, features):  
        W = np.random.dirichlet(np.ones(4),size=1)
        M = np.array(features)
        return np.matmul(M,  W.T)

    def extract_centrality(self):
        degree = nx.degree(self.network)
        betweenness = nx.betweenness_centrality(self.network)
        closeness = nx.closeness.closeness_centrality(self.network)
        eigenvector = nx.eigenvector_centrality(self.network, max_iter=600)
        
        features = []
        for node in self.network:
            features.append([degree[node], betweenness[node], closeness[node], eigenvector[node]])

        if(self._verbose):
            print("中心性提取成功")
    
        return features