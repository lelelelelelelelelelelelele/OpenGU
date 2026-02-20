import random
import colorsys
from typing import List, Dict, Any
import networkx as nx
import pandas as pd
import plotly.express as px
from pyvis.network import Network
from torch_geometric.datasets import Planetoid
from torch_geometric.utils import to_networkx
import json
import self_lpa
def load_cora_as_nx():
    """返回 NetworkX 无向图"""
    dataset = Planetoid(root='./data', name='Cora')
    data = dataset[0]                               # PyG Data 对象
    G = to_networkx(data, to_undirected=True)       # 转成无向 NetworkX
    return G
def _LPA(G, seed):
    random.seed(seed)
    
    # 1. 运行 LPA
    # communities = nx.algorithms.community.label_propagation_communities(G)
    communities = self_lpa.self_lpa(G, label_number=15, iter=20, seed=seed)
    shards: List[List[int]] = [sorted(c) for c in communities]
    def _distinct_colors(n):
        HSV_tuples = [(x*1.0/n, 0.5, 0.8) for x in range(n)]
        hex_colors = ['#%02x%02x%02x' % tuple(int(c*255) for c in colorsys.hsv_to_rgb(*hsv)) 
                      for hsv in HSV_tuples]
        return hex_colors
    
    colors = _distinct_colors(len(shards))
    node2color = {}
    for idx, shard in enumerate(shards):
        for node in shard:
            node2color[node] = colors[idx]
    return shards, node2color
def lpa_shards_and_vis(
        G: nx.Graph,
        seed: int = 42,
        pyvis_height: str = "600px",
        out_prefix: str = "lpa_demo"
    ) -> Dict[str, Any]:
    """
    运行 LPA，返回社区 shard 列表，并生成可视化文件。

    返回值
    ------
    shards: List[List[int]]
        每个元素是一个社区，社区内部是节点列表。
    同时会在当前目录生成：
        {out_prefix}_graph.html   —— 交互式网络图
        {out_prefix}_bar.html     —— 社区大小柱状图
    """
    random.seed(seed)
    
    # 1. 运行 LPA
    communities = nx.algorithms.community.label_propagation_communities(G)
    shards: List[List[int]] = [sorted(c) for c in communities]
    
    # 2. 给每个社区分配一个颜色
    def _distinct_colors(n):
        HSV_tuples = [(x*1.0/n, 0.5, 0.8) for x in range(n)]
        hex_colors = ['#%02x%02x%02x' % tuple(int(c*255) for c in colorsys.hsv_to_rgb(*hsv)) 
                      for hsv in HSV_tuples]
        return hex_colors
    
    colors = _distinct_colors(len(shards))
    node2color = {}
    for idx, shard in enumerate(shards):
        for node in shard:
            node2color[node] = colors[idx]
    
    # 3. PyVis 交互图
    net = Network(height=pyvis_height, bgcolor="#ffffff", font_color="black", notebook=False)
    net.from_nx(G)
    # === 新增：减轻前端负担 ===
    options = {
        "physics": {
            "enabled": False,
            "barnesHut": {
                "gravitationalConstant": -2000,
                "centralGravity": 0.1,
                "springLength": 50,
                "springConstant": 0.01,
                "damping": 0.09,
                "avoidOverlap": 0.1
            },
            "stabilization": {"iterations": 10}
        },
        "nodes": {"font": {"size": 8}},
        "edges": {"smooth": {"type": "continuous"}}
    }

    net.set_options(json.dumps(options))

    for n in net.nodes:
        nid = n["id"]
        n["color"] = node2color[nid]
        n["title"] = f"community: {list(node2color.values()).index(node2color[nid])}"
    # net.repulsion()
    net.write_html(f"{out_prefix}_graph.html")
    
    # 4. Plotly 社区大小柱状图
    df = pd.DataFrame({"community": list(range(len(shards))),
                       "size": [len(s) for s in shards]})
    fig = px.bar(df, x="community", y="size",
                 color="community",
                 color_discrete_sequence=colors,
                 title="Community sizes (Label Propagation)")
    fig.write_html(f"{out_prefix}_bar.html")
    
    print(f"已生成文件：{out_prefix}_graph.html 和 {out_prefix}_bar.html")
    
    return {"shards": shards, "node2color": node2color}

# ------------------ DEMO ------------------
if __name__ == "__main__":
    # 随便造一个图做演示
    # G = nx.karate_club_graph()
    # G = load_cora_as_nx()
    # result = lpa_shards_and_vis(G, seed=2024)
    # print("社区 shard 列表：", result["shards"])
    pass