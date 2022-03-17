from src import Setting
from src import QuantumWalk
from src import Network
import numpy as np
import os
import json

setgraph = Setting()
setgraph.call()

# Creating networkf
graph = Network()
graph.custom(node_identifiers=setgraph.config['node_identifiers'],
             sink=setgraph.config['sink'],
             source=setgraph.config['source'],
             source_cycles=setgraph.config['source_cycles'],
             node_thetas=setgraph.config['node_thetas'],
             xi=setgraph.config['xi']
            )

# 普段
qw = QuantumWalk(graph, max_step=setgraph.config['max_step'])
while qw.step.step!=qw.max_step:
    qw.evolve()
    qw.to_plot(f'gv_{qw.step.step}.png')

qw.step.to_csv()

# # 行列
# for i in [13]:
#     with open(f"config{i}.json") as f:
#         config = json.load(f)

#     graph = Network()
#     graph.custom(node_identifiers=config['node_identifiers'],
#                 sink=config['sink'],
#                 source=config['source'],
#                 source_cycles=config['source_cycles'],
#                 node_thetas=config['node_thetas']
#                 )

#     os.makedirs('output', exist_ok=True)
#     qw = QuantumWalk(graph, max_step=config['max_step'])
#     while qw.step.step!=qw.max_step:
#         qw.evolve(xi=0)
#         qw.to_plot(f'gv_{qw.step.step}.png')

#     qw.step.to_csv()
#     os.rename("output", f"output_beta{i}")



# graph.dump_info()
# graph.to_gif()

# for[node for node in graph.nodes if node.data["coin_name"] in ["source","sink"]]

################################################ 前回 ################################################

# graph.add_node('0,0')
# graph.add_edge('0,0', '0,0', data={'state':0, 'edge_type':'s0'})
# graph.add_edge('0,0', '0,0', data={'state':0, 'edge_type':'s1'})

# for i in range(50):
#     graph.expand(directions=['left', 'right', 'up', 'down'], xlim=[-2,2], ylim=[-2,2])

# # グラフ(1)
# graph.add_pin_node(pin_node_identifier='2,3', connect_node_identifier='2,2')
# graph.add_pin_node(pin_node_identifier='-2,-3', connect_node_identifier='-2,-2')
# graph.set_coin_name(properties={'-2,-3':'source', '2,3':'sink'}, nokey_coin='dressed_photon')
# graph.set_coin_theta(properties={'-2,-2': np.arcsin(np.sqrt(2/3))}, nokey_coin=np.arcsin(np.sqrt(2/3)))

# グラフ(2)
# graph.add_pin_node(pin_node_identifier='3,2', connect_node_identifier='2,2')
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='-3,2', connect_node_identifier='-2,2')
# graph.set_coin_name(properties={'-3,-2':'source', '3,2':'sink', '-3,2':'sink'}, nokey_coin='dressed_photon')

# グラフ(3)
# graph.add_pin_node(pin_node_identifier='3,2', connect_node_identifier='2,2')
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='-2,-3', connect_node_identifier='-2,-2')
# graph.set_coin_name(properties={'-3,-2':'source', '3,2':'sink', '-2,-3':'sink'}, nokey_coin='dressed_photon')

# グラフ(4)
# graph.add_pin_node(pin_node_identifier='3,2', connect_node_identifier='2,2')
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='2,-3', connect_node_identifier='2,-2')
# graph.set_coin_name(properties={'-3,-2':'source', '3,2':'sink', '2,-3':'sink'}, nokey_coin='dressed_photon')

# グラフ(5)
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='-3,2', connect_node_identifier='-2,2')
# graph.add_pin_node(pin_node_identifier='2,-3', connect_node_identifier='2,-2')
# graph.set_coin_name(properties={'-3,-2':'source', '-3,2':'sink', '2,-3':'sink'}, nokey_coin='dressed_photon')

# グラフ(6)
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='2,-3', connect_node_identifier='2,-2')
# graph.set_coin_name(properties={'-3,-2':'source', '2,-3':'sink'}, nokey_coin='dressed_photon')

# グラフ(7)
# graph.add_pin_node(pin_node_identifier='-3,-2', connect_node_identifier='-2,-2')
# graph.add_pin_node(pin_node_identifier='-2,3', connect_node_identifier='-2,2')
# graph.set_coin_name(properties={'-3,-2':'source', '-2,3':'sink'}, nokey_coin='dressed_photon')

# graph.dump_info()

# Setting quantum walk on network

# qw = QuantumWalk(graph)

# for i in range(100): # 20 step
#     qw.evolve()
#     # if i%1000==0 or i%1000==1:
#     if True:
#         graph.to_plot(f'gv_{i}.png')
#         print(f'gv_{i}.png')

# qw.step.to_csv()

# graph.dump_info()
# graph.to_gif()



