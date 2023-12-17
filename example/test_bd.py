import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from diffusionModel import ICWeighter, IC, SIRWeighter, SIR
from algorithm import DegreeCentrality, SAW_ASA, NCVoteRank, PageRank, DegreeDiscount
from dataset import load_networks
## 读取网络
network = load_network("filmtrust", "undirected")

## 定义权重生成器
weighter = ICWeighter(APType="uniform", p=0.1)
weighter.assign_activa_prob_batch(networks)


## 定义IC模型
ic = IC(weighter=weighter, MC=1000, verbose=True)


## 定义DegreeDiscount算法
degree_discount = DegreeDiscount()

S = degree_discount(network, 20)
inflence_spread = IC(network, S)
print(influence_spread)
