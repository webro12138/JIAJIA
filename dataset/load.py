from constant import DATASETS_PATH, NETWORK_DATASETS, BASE_MULTILAYER_NETWORK_DATASETS, SINGLE_LAYER_NETWORK_DATASETS, LF_MULTILAYER_NETWORK_DATASETS
from utils import read_list_for_txt
import networkx as nx 
import os
from network import MLN, SLN
def load_networks(names, gtypes, verbose=True):
    assert isinstance(names, list) or isinstance(gtypes, str), "names必须为list或str类型"
    if(isinstance(names, str)):
        assert isinstance(gtypes, str), "当只读取一个数据集时, gtypes必须为str"

    assert isinstance(gtypes, list) or isinstance(gtypes, str), "gtypes必须为list或str类型"
    if(isinstance(gtypes, str)):
        assert gtypes in ["undirected", "directed"], f"gtypes仅支持undirected和directed"
    
    if(isinstance(names, list)):
        if(isinstance(gtypes, list)):
            networks = []
            for i in range(len(names)):
                networks.append(load_network(names[i], gtypes[i], verbose))
    
        else:
            networks = []
            for i in range(len(names)):
                networks.append(load_network(names[i], gtypes, verbose))
        return networks
    else:
        return load_network(names, gtypes, verbose)

def load_network(name, gtype="undirected", verbose=True):
    '''
    输入:数据集名称name, 网络类型gtype
    输出:Network类
    '''
    assert gtype in ["undirected", "directed"], f"无{gtype}类型的图, 仅支持undirected和directed"

    ## 检查输入的数据集名称是否正确
    assert name in NETWORK_DATASETS, f"{name}数据集不存在"
    
    ## 单层网络，且符合单层网络base规范的
    if name in SINGLE_LAYER_NETWORK_DATASETS:
        network = load_base_single_network(name, gtype)

    ## 多层网络，且符合多层网络base规范的
    if name in BASE_MULTILAYER_NETWORK_DATASETS:
        network = load_base_multi_network(name, gtype)

    if name in LF_MULTILAYER_NETWORK_DATASETS:
        network = load_lf_multi_network(name, gtype)

    if(verbose):
        print_datasets_info(network)

    return network

def load_base_single_network(name, gtype):
    '''
    功能:这个函数只能读取based单层网络数据集格式,格式遵循固定规则,请勿混用
    输入:数据集名称name, 图类型gtype
    输出:一个单层网络SLN
    '''    

    ##按照base格式获取数据集的路径
    path = os.path.join(DATASETS_PATH, "SLNDatasets", name, "edge.txt")
    if(gtype =="undirected"):
        graph = nx.read_edgelist(path, create_using=nx.Graph(), nodetype=int)
    else:
        graph = nx.read_edgelist(path, create_using=nx.DiGraph(), nodetype=int)

    ## 构建单层网络
    sln = SLN(graph)
    sln.set_name(name)

    return sln

def load_base_multi_network(name, gtype):
    '''
    功能:这个函数只能读取base多层网络数据集格式,格式遵循固定规则,请勿混用
    输入:数据集名称name, 图类型gtype
    输出:一个多层网络MLN
    '''    

    ##按照base格式获取数据集的路径
    path = os.path.join(DATASETS_PATH, "MLNDatasets", name, "Dataset", name + ".edges")

    ## 读取数据, 存储为一个二维列表, 该列表每行的第一列为层序号，第二列为源节点id, 第三列为目标节点id
    data_info = read_list_for_txt(path)
        
    ## 构建一个字典, 该字典关键字是层序号, 值是二维数组, 存储着一个层的所有边
    edges_layers = {}
    for item in data_info:
        if(item[0] not in edges_layers):
            edges_layers[int(item[0])] = []
        edges_layers[int(item[0])].append([int(item[1]), int(item[2])])

    ## 求层数目
    number_of_layers = len(list(edges_layers.keys()))

    ## 创建每层对应的networkx图, 并且获得所有层的所有节点id, 这是为了防止有的层没有对应的节点。
    layers = []
    allnodes = []
    keys = list(edges_layers.keys())

    temp = 0
    for i in range(number_of_layers):
            if(gtype == "undirected"):
                layer = nx.Graph()
            else:
                layer = nx.DiGraph()
            
            layer.add_edges_from(edges_layers[keys[i]])
            temp += layer.number_of_edges()
            allnodes += list(layer.nodes)
            layers.append(layer)
    allnodes = set(allnodes)
    
    ## 将每层缺失的点添加进去，保证一个节点在所有层都有镜像
    for i in range(number_of_layers):
        layers[i].add_nodes_from(list(allnodes - set(layers[i].nodes)))

    ## 构建多层网络
    mln = MLN()
    mln.add_layers_from(layers)
    mln.set_name(name)
    return mln


def load_lf_multi_network(name, gtype):
    '''读取LF格式的多层网络
       输入:数据集名称name, 网络类型gtype, gtype ->["undirected", "indirected"]
       输出:多层网络MLN
    '''
    
    dataset_path = os.path.join(DATASETS_PATH, "MLNDatasets", name) # 获得name指定的数据集所在目录
    
    files = os.listdir(dataset_path) 

    layers = []
    for file in files:
        if ("layer" in file):
            if(gtype=="undirected"):
                graph = nx.read_edgelist(os.path.join(dataset_path, file), create_using=nx.Graph)
            else:
                graph = nx.read_edgelist(os.path.join(dataset_path, file), create_using=nx.DiGraph)
            layers.append(graph)

    mln = MLN()
    mln.add_layers_from(layers)
    mln.set_name(name)
    return mln

def print_datasets_info(network):
    '''
    根据网络的类型, 输出数据集的基本信息.
    输入:一个网络network
    '''
    print(f">>{network._name}加载成功<<")
    print(f"共有{network.number_of_nodes()}个节点")
    print(f"共有{network.number_of_edges()}条边")

    if(isinstance(network, MLN)):
         print(f"共有{network.number_of_layers()}个层")

    print("=================")