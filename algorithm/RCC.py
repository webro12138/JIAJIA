from algorithm import AlgorithmBase
from tqdm import tqdm
import random
from utils import count_frequency

def node2vec_sample(succ, prev_succ, prev_node, p, q):
    succ_len = len(succ)
    prev_succ_len = len(prev_succ)

    probs = list()
    prob_sum = 0

    prev_succ_set = list()
    for i in range(prev_succ_len):
        prev_succ_set.insert(0, prev_succ[i])
    # 计算node2vec的各边权重
    
    for i in range(succ_len):
        if succ[i] == prev_node:
            prob = 1. / p
        elif len(prev_succ_set) > 0 and succ[i] != prev_succ_set[-1]:
            prob = 1.
        else:
            prob = 1. / q
        probs.append(prob)
        prob_sum += prob

    rand_num = random.uniform(0, 1) * prob_sum

    for i in range(succ_len):
        rand_num -= probs[i]
        if rand_num <= 0:
            sample_succ = succ[i]
            return sample_succ

def node2vec_walk(graph, nodes, max_depth, p, q):
    # 初始化 walks的起点为nodes
    walks, succ = [nodes], list(graph[nodes])
    prev_succ, prev_node = [-1], [-1]
    cur_nodes = nodes
    for l in range(max_depth):
        # node2vec_sample 选出下一个点的函数
        sampled_succ = node2vec_sample(succ, prev_succ, prev_node, p, q)
        if(sampled_succ == None):
            sampled_succ = random.choice(list(graph.nodes))

        walks.append(sampled_succ)
        prev_node, prev_succ = cur_nodes, succ
        cur_nodes = sampled_succ
        succ = list(graph[cur_nodes])
        
    return walks

class RCC(AlgorithmBase):
    def __init__(self, walk_iter, walk_length, p, q, verbose=True):
        super().__init__()
        self._walk_iter = walk_iter
        self._walk_length = walk_length
        self._p = p
        self._q = q
        self._verbose = verbose
    
    def get_score(self, network):
        score = {}
        for key in network.nodes():
            score[key] = 0

        for layer in network.layers:
            tracks = []
            for _ in range(self._walk_iter):
                tracks += node2vec_walk(layer, random.choice(list(layer.nodes)), self._walk_length, self._p, self._q)
            temp = count_frequency(tracks)
            for key in temp:
                score[key] += temp[key]
        score = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
        return score
            
    def run(self, network, k):
        assert isinstance(k, int), "k是一个正整数"
        S = []
        score = list(self.get_score(network).items())
        for i in range(k):
            S.append(score[i][0])
       
        return S
