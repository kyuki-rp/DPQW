from src import Setting
from src import QuantumWalk
from src import Network


setgraph = Setting()
setgraph.call()


# Creating networkf
graph = Network()
graph.custom(node_identifiers=setgraph.config['node_identifiers'],
             sink=setgraph.config['sink'],
             source=setgraph.config['source'],
             source_cycles=setgraph.config['source_cycles'],
             node_thetas=setgraph.config['node_thetas']
            )

# # グラフ(1)

# graph.custom(node_identifiers=['0,6',
#                                '-5,5','-4,5','-3,5,','-2,5','-1,5','0,5','1,5','2,5','3,5','4,5','5,5',
#                                '-5,4','-4,4','-3,4,','-2,4','-1,4','0,4','1,4','2,4','3,4','4,4','5,4',
#                                '-5,3','-4,3','-3,3,','-2,3','-1,3','0,3','1,3','2,3','3,3','4,3','5,3',
#                                '-5,2','-4,2','-3,2,','-2,2','-1,2','0,2','1,2','2,2','3,2','4,2','5,2',
#                                '-5,1','-4,1','-3,1,','-2,1','-1,1','0,1','1,1','2,1','3,1','4,1','5,1',
#                                '-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0'],
#              sink=['0,6'],
#              source=['-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0']
#             )

# # グラフ(2)
# graph.custom(node_identifiers=['0,6',
#                                '-1,5','0,5','1,5',
#                                '-2,4','-1,4','0,4','1,4','2,4',
#                                '-3,3,','-2,3','-1,3','0,3','1,3','2,3','3,3',
#                                '-4,2','-3,2,','-2,2','-1,2','0,2','1,2','2,2','3,2','4,2',
#                                '-5,1','-4,1','-3,1,','-2,1','-1,1','0,1','1,1','2,1','3,1','4,1','5,1',
#                                '-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0'],
#              sink=['0,6'],
#              source=['-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0']
#             )

# # グラフ(3)
# graph.custom(node_identifiers=['4,6',
#                                '0,5','1,5','2,5','3,5','4,5',
#                                '0,4','1,4','2,4','3,4','4,4',
#                                '0,3','1,3','2,3','3,3','4,3',
#                                '0,2','1,2','2,2','3,2','4,2',
#                                '0,1','1,1','2,1','3,1','4,1',
#                                '0,0'],
#              sink=['4,6'],
#              source=['0,0']
#             )

# # グラフ(4)
# graph.custom(node_identifiers=['-1,6','0,6','1,6',
#                                '-2,5','-1,5','0,5','1,5','2,5',
#                                '-3,4','-2,4','-1,4','0,4','1,4','2,4','3,4',
#                                '-4,3','-3,3,','-2,3','-1,3','0,3','1,3','2,3','3,3','4,3',
#                                '-5,2','-4,2','-3,2,','-2,2','-1,2','0,2','1,2','2,2','3,2','4,2','5,2',
#                                '-6,1', '-5,1','-4,1','-3,1,','-2,1','-1,1','0,1','1,1','2,1','3,1','4,1','5,1', '6,1',
#                                '-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0'],
#              sink=['-1,6', '0,6', '1,6', '-2,5', '-3,4', '-4,3', '-5,2', '-6,1', '2,5', '3,4', '4,3', '5,2', '6,1'],
#              source=['-5,0','-4,0','-3,0,','-2,0','-1,0','0,0','1,0','2,0','3,0','4,0','5,0'],
#              source_cycles={'-5,0':"1,0,1,0",'-4,0':"1,0,1,0",'-3,0,':"1,0,1,0",'-2,0':"1,0,1,0",'-1,0':"1,0,1,0",'0,0':"1,0,1,0",'1,0':"1,0,1,0",'2,0':"1,0,1,0",'3,0':"1,0,1,0",'4,0':"1,0,1,0",'5,0':"1,0,1,0"}
#             )

# Setting quantum walk on network
qw = QuantumWalk(graph, max_step=setgraph.config['max_step'])
while qw.step.step!=qw.max_step:
    qw.evolve()
    qw.to_plot(f'gv_{qw.step.step}.png')

qw.step.to_csv()
# graph.dump_info()
# graph.to_gif()


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



