import networkx as nx
import numpy as np
from network import Network

class MLN(Network):
    def __init__(self) -> None:
        super().__init__()
        self.layers = []
        self.nodes_index = {}    
        self.out_degrees = None
        self._nodes = []
        self.average_out_degree = 0
        self.adjs = None
        self.gtype = None
        
    def add_layer(self, graph):
        """向多层网络NLM中添加层
           输入:输入一个层，该层是一个networkx Graph
        """
        assert isinstance(graph, nx.DiGraph) or isinstance(graph, nx.Graph), "The graph must be a directed or undirected graph"
        
        if(len(self.layers) != 0):
            ## 如果是不是第一层, 则每次添加层时都要对多层网络的节点集进行扩充
            self.layers.append(graph.copy())
            self._nodes = list(set(self._nodes) | set(graph.nodes))    
        else:
            ## 第一次添加层, 要判断多层网络的类型type
            ## 注意, 获取可以研究一下不同层为不同图的理论.如第一层为有向图,第二层为无向图, 那么就要修改MLN类.
            self.layers.append(graph)
            if(type(graph) == nx.Graph):
                self.gtype = 'indirected'
            else:
                self.gtype = "directed"
               
            self._nodes = list(self.layers[0].nodes())
        
        ## 确保每一层都有相同的节点
        for i in range(self.number_of_layers()):
            self.layers[i].add_nodes_from(self._nodes)

        ## 为节点和位置建立一个字典映射
        for i in range(self.number_of_nodes()):
            self.nodes_index[self._nodes[i]] = i 
        

    def get_node_index(self, v):
        """给定节点id获得节点位置索引
           输入:节点v
           输出:节点索引
        """
        return self.nodes_index[v]

    def get_index_from_node_banches(self, nodes):
        nodes_index = []
        for node in nodes:
            nodes_index.append(self.nodes_index[node])
        return nodes_index
    
    def add_layers_from(self, layers):
        if(len(layers) != 0):
            for layer in layers:
                self.add_layer(layer)
        else:
            print("请注意, 网络没有任何层")

    def number_of_layers(self):
        return len(self.layers)
   
    def number_of_nodes(self):
        return len(self._nodes)
    
    def number_of_edges(self):
        number_of_edges = 0
        for i in range(self.number_of_layers()):
            number_of_edges += self.layers[i].number_of_edges()
        return number_of_edges

    def neighbors(self, nodes):
            result = []
            for i in range(self.number_of_layers()):
                result += self.single_layer_neigbors(i, nodes)
            return result

    def single_layer_neigbors(self, layer_num, nodes):
        if(isinstance(nodes, list)):
            neis = []
            for node in nodes:
                neis += list(self.layers[layer_num][node])
        else:
            return list(self.layers[layer_num][nodes])

    def degrees(self, banch=None):
        if not isinstance(banch, list) and banch != None:
            for i in range(self.number_of_layers()):
                return len(self.layers[i][banch])
        
        if banch == None:
            banch = self.nodes()

        mldegree = {}
        for node in banch:
            mldegree[node] = 0
            for i in range(self.number_of_layers()):
                mldegree[node] += len(self.layers[i][node])
        
        if len(mldegree) == 1:
            return mldegree[banch] 

        return mldegree
    
    # def node_all_neigbour(self, nodes, hop=1):
    #     result = []
    #     new_nodes = nodes[:]
    #     index = 0
    #     while index < hop:
    #         one_iter_nodes = []
    #         for node in new_nodes:
    #             for i in range(self.number_of_layers()):
    #                 one_iter_nodes += list(self.layers[i][node])
    #         one_iter_nodes = set(one_iter_nodes)
    #         new_nodes = list(set(one_iter_nodes) - set(new_nodes))
    #         result += new_nodes
    #         index += 1    
    #     result = list(set(result) - set(nodes))
    #     return result
