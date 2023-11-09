import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from diffusionModel import ICWeighter, IC, SIRWeighter, SIR
from algorithm import DegreeCentrality, SAW_ASA, NCVoteRank, PageRank, DegreeDiscount
from dataset import load_networks
from evalution import Evalution, InfluenceSpread
## 读取网络
networks = load_networks(["filmtrust"], "undirected")

## 定义权重生成器
weighter = SIRWeighter(APType="uniform", RPType="uniform", p=0.1, q=1)
weighter.assign_activa_prob_batch(networks)


## 定义IC模型
sir = SIR(weighter=weighter, MC=1000, verbose=True)

## 定义degree中心性算法
dc = DegreeCentrality(verbose=True)

## 定义SAW_ASA算法
saw_asa = SAW_ASA(sir)

## 定义NCVoteRank算法
nc_vote_rank = NCVoteRank(0.25)

## 定义PageRank
pagerank = PageRank()

## 定义DegreeDiscount算法
degree_discount = DegreeDiscount()


## 定义Influence spread指标
IS = InfluenceSpread(sir)
## 使用IC模型衡量S的质量
ev = Evalution([IS], networks, [pagerank, degree_discount, nc_vote_rank, saw_asa], [50])
print(ev())
