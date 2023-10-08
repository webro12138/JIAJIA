import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from diffusionModel import ICWeighterICWeighterICWeighterICWeighter, IC
from algorithm import DegreeCentrality
from dataset import load_network

## 读取网络
network = load_network("facebook", "undirected")

## 定义权重生成器
weighter = ICWeighter(APType="random", p=(0, 1))

## 定义IC模型
ic = IC(weighter=weighter, MC=10000, verbose=True)

## 定义degree中心性算法
dc = DegreeCentrality(verbose=True)

## 度中心性选择种子节点
S = dc(network, k=5)

## 使用IC模型衡量S的质量
influence_spread = ic(network, S)
print(influence_spread)