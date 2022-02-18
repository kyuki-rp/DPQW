import numpy as np
import pandas as pd
from .edge import Edge
from .node import Node
from .observer import Observer
import itertools


class Network():
    '''
    A directed graph class that can store multiedges.
    This class wraps networkx.
    '''
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.oup_pngs = []
        self.xi = 0

    def get_adjacency_matrix(self):
        # TODO: replace sparse df.
        labels = [node.identifier for  node in self.nodes]
        adj_matrix = pd.DataFrame(index=labels,columns=labels)
        for (innode, outnode) in [(node.identifier, outedge.final_node.identifier) for node in self.nodes for outedge in node.outedges]:
            adj_matrix.loc[innode, outnode] = 1
        adj_matrix = adj_matrix.replace(np.nan, 0)
        return adj_matrix

    
    def add_node(self, identifier):
        '''
        Adding method for node
        '''
        if identifier not in [node.identifier for node in self.nodes]:
            pos = [int(identifier.split(',')[0]),int(identifier.split(',')[1])]
            new_node = Node(identifier, pos)
            self.nodes.append(new_node)

    def create_lattice_graph(self, n_i, n_j):
        for i in range(n_i):
            for j in range(n_j):
                self.add_node(f'{j},{i}', pos=(j,i))


    def add_edge(self, initial_node_identifier, final_node_identifier, data=None):
        '''
        Adding method for edge
        '''
        
        if f"{initial_node_identifier}->{final_node_identifier}:{data['edge_type']}" not in [f"{edge.initial_node.identifier}->{edge.final_node.identifier}:{edge.data['edge_type']}" for edge in self.edges]:
            initial_node = self.get_node(initial_node_identifier)
            final_node = self.get_node(final_node_identifier)

            new_edge = Edge(initial_node, final_node, data)
            self.edges.append(new_edge)

            # add adjacent edges for nodes.
            initial_node.add_outedges(new_edge)
            final_node.add_inedges(new_edge)


    def add_selfloop_edge(self, node_identifier, data={}):
        data_ = data
        data_['color'] = 'black'
        self.add_edge(node_identifier, node_identifier, data)


    def add_bidirectional_edge(self, initial_node_identifier, final_node_identifier, data={}):
        data_ = data[0]
        data_['color'] = 'red'
        self.add_edge(initial_node_identifier, final_node_identifier, data_)

        data_ = data[1]
        data_['color'] = 'blue'
        self.add_edge(final_node_identifier, initial_node_identifier, data_)
        

    def get_node(self, search_identifier):
        '''
        Getting method of edge index
        '''
        node_index = [node.identifier for node in self.nodes].index(search_identifier)
        return self.nodes[node_index]

    def get_edge(self, search_initial_node, search_final_node, edge_type=None):
        '''
        Getting method of edge index
        '''
        if edge_type is None:
            edge_index = [f'{edge.initial_node.identifier}->{edge.final_node.identifier}' for edge in self.edges].index(f'{search_initial_node}->{search_final_node}')
        else:
            edge_index = [f"{edge.initial_node.identifier}->{edge.final_node.identifier}:{edge.data['edge_type']}" for edge in self.edges].index(f'{search_initial_node}->{search_final_node}:{edge_type}')

        return self.edges[edge_index]
        

    def remove_edge(self, edge):
        '''
        Removing method for edge
        '''
        self.edges.remove(edge)

        # remove adjacent edges information for nodes.
        edge.initial_node.remove_outedges(edge)
        edge.final_node.remove_inedges(edge)


    def dump_info(self):
        print('--- Nodes info ---')
        for node in self.nodes:
            node.dump_info()

        print('--- Edges info ---')
        for edge in self.edges:
            edge.dump_info()
            
    def remove_node(self, search_identifier):
        '''
        Nodes removing method
        '''
        node_index = [node.identifier for node in self.nodes].index(search_identifier)
        
        # remove adjacent_inedges
        for edge in self.nodes[node_index].inedges[::-1]:
            self.remove_edge(edge.initial_node.identifier, edge.final_node.identifier)

        # remove adjacent_outedges
        for edge in self.nodes[node_index].outedges[::-1]:
            self.remove_edge(edge.initial_node.identifier, edge.final_node.identifier)

         # remove node
        _ =  self.nodes.pop(node_index)




    def set_coin_theta(self, properties, nokey_coin):
        for node in self.nodes:
            if node.identifier in properties.keys():
                node.data_update(key='coin_theta', val=properties[node.identifier])
            else:
                node.data_update(key='coin_theta', val=nokey_coin)

    # def remove_edge(self, search_initial_node, search_final_node):
    #     edge_index = [f'{edge.initial_node.identifier}->{edge.final_node.identifier}' for edge in self.edges].index(f'{search_initial_node}->{search_final_node}')

    #     # remove adjacent_edges from node
    #     self.edges[edge_index].initial_node.remove_outedges(search_initial_node, search_final_node)
    #     self.edges[edge_index].final_node.remove_inedges(search_initial_node, search_final_node)

    #     # remove edge
    #     _ = self.edges.pop(edge_index)


    def expand(self, directions, xlim=[-np.inf,np.inf], ylim=[-np.inf,np.inf]):
        old_node_identifiers = [[int(node.identifier.split(',')[0]), int(node.identifier.split(',')[1])] for node in self.nodes]

        for direction, node_identifiers in self.get_end_node_identifiers().items():
            for node_identifier in node_identifiers:
                node_type = self.get_new_node_type(node_identifier, direction, xlim=xlim, ylim=ylim)

                if direction=='west' and 'west' not in node_type:
                    new_node_identifier = self.get_new_node_identifier(node_identifier, direction)
                elif direction=='east' and 'east' not in node_type:
                    new_node_identifier = self.get_new_node_identifier(node_identifier, direction)
                elif direction=='south' and 'south' not in node_type:
                    new_node_identifier = self.get_new_node_identifier(node_identifier, direction)
                elif direction=='north' and 'north' not in node_type:
                    new_node_identifier = self.get_new_node_identifier(node_identifier, direction)
                else:
                    new_node_identifier = node_identifier

                if direction=='west':
                    self.add_node(new_node_identifier)
                    self.add_edge(node_identifier, new_node_identifier, data={'state':0, 'edge_type':'h-'})
                    self.add_edge(new_node_identifier, node_identifier, data={'state':0, 'edge_type':'h+'})
                elif direction=='east':
                    self.add_node(new_node_identifier)
                    self.add_edge(node_identifier, new_node_identifier, data={'state':0, 'edge_type':'h+'})
                    self.add_edge(new_node_identifier, node_identifier, data={'state':0, 'edge_type':'h-'})
                elif direction=='south':
                    self.add_node(new_node_identifier)
                    self.add_edge(node_identifier, new_node_identifier, data={'state':0, 'edge_type':'v-'})
                    self.add_edge(new_node_identifier, node_identifier, data={'state':0, 'edge_type':'v+'})
                elif direction=='north':
                    self.add_node(new_node_identifier)
                    self.add_edge(node_identifier, new_node_identifier, data={'state':0, 'edge_type':'v+'})
                    self.add_edge(new_node_identifier, node_identifier, data={'state':0, 'edge_type':'v-'})

                self.add_edge(node_identifier, node_identifier, data={'state':0, 'edge_type':'s0'})
                self.add_edge(node_identifier, node_identifier, data={'state':0, 'edge_type':'s1'})


    def custom(self, node_identifiers, sink=[], source=[], source_cycles={}, node_thetas={}, xi=0):
        for node_identifier in node_identifiers:
            self.add_node(node_identifier)
        
        edges_info = self.get_edge_info(node_identifiers, sink, source)
        for  (from_node_identifier, to_node_identifier, edge_type) in edges_info:
            self.add_edge(from_node_identifier, to_node_identifier, data={'state':0, 'edge_type':edge_type})

        # Set coin_name
        for node in self.nodes:
            if node.identifier in sink:
                node.data_update(key='coin_name', val='sink')
            elif node.identifier in source:
                node.data_update(key='coin_name', val='source')
            elif node.identifier in node_identifiers:
                node.data_update(key='coin_name', val='dressed_photon')

        # Set source_cycle
        for node in self.nodes:
            if node.identifier in source_cycles.keys():
                cycle = itertools.cycle([float(i) for i in source_cycles[node.identifier].split(',')])
                node.data_update(key='source_cycle', val=cycle)

        # Set node_thetas
        for node in self.nodes:
            if node.identifier in node_thetas.keys():
                theta = eval(node_thetas[node.identifier])
                node.data_update(key='coin_theta', val=theta)

        # Set xi
        self.xi = eval(f"{xi}/180*np.pi")


    def get_edge_info(self, node_identifiers, sink, source, sink_edge_types=['v+','v-','h+','h-'], source_edge_types=['v+','v-','h+','h-']):
    # def get_edge_info(self, node_identifiers, sink, source, sink_edge_types=['v+','v-'], source_edge_types=['v+','v-']):
        edges_info = []
        for from_node_identifier in node_identifiers:
            edge_type_check = []
            for to_node_identifier in node_identifiers:
                x_dif = int(to_node_identifier.split(',')[0]) - int(from_node_identifier.split(',')[0])
                y_dif = int(to_node_identifier.split(',')[1]) - int(from_node_identifier.split(',')[1])
                
                 # from.sinkの場合
                if from_node_identifier in sink and to_node_identifier not in sink:
                    if x_dif==0 and y_dif==1 and 'v+' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                        edge_type_check.append('v+')
                    elif x_dif==0 and y_dif==-1 and 'v-' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                        edge_type_check.append('v-')
                    elif x_dif==1 and y_dif==0 and 'h+' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                        edge_type_check.append('h+')
                    elif x_dif==-1 and y_dif==0 and 'h-' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                        edge_type_check.append('h-')

                # to.sinkの場合
                elif from_node_identifier not in sink and to_node_identifier in sink:
                    if x_dif==0 and y_dif==1 and 'v-' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                        edge_type_check.append('v+')
                    elif x_dif==0 and y_dif==-1 and 'v+' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                        edge_type_check.append('v-')
                    elif x_dif==1 and y_dif==0 and 'h-' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                        edge_type_check.append('h+')
                    elif x_dif==-1 and y_dif==0 and 'h+' in sink_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                        edge_type_check.append('h-')

                # from.to.sink
                elif from_node_identifier in sink and to_node_identifier in sink:
                    pass

                # from.sourceの場合
                elif from_node_identifier in source and to_node_identifier not in source:
                    if x_dif==0 and y_dif==1 and 'v+' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                        edge_type_check.append('v+')
                    elif x_dif==0 and y_dif==-1 and 'v-' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                        edge_type_check.append('v-')
                    elif x_dif==1 and y_dif==0 and 'h+' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                        edge_type_check.append('h+')
                    elif x_dif==-1 and y_dif==0 and 'h-' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                        edge_type_check.append('h-')

                # to.sourceの場合
                elif from_node_identifier not in source and to_node_identifier in source:
                    if x_dif==0 and y_dif==1 and 'v-' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                        edge_type_check.append('v+')
                    elif x_dif==0 and y_dif==-1 and 'v+' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                        edge_type_check.append('v-')
                    elif x_dif==1 and y_dif==0 and 'h-' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                        edge_type_check.append('h+')
                    elif x_dif==-1 and y_dif==0 and 'h+' in source_edge_types:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                        edge_type_check.append('h-')

                # from.to.sourceの場合
                elif from_node_identifier in source and to_node_identifier in source:
                    pass

                # その他の場合
                else:
                    if x_dif==0 and y_dif==0:
                        edges_info.append((from_node_identifier, to_node_identifier, 's0'))
                        edges_info.append((from_node_identifier, to_node_identifier, 's1'))
                        edge_type_check.append('s0')
                        edge_type_check.append('s1')
                    elif x_dif==0 and y_dif==1:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                        edge_type_check.append('v+')
                    elif x_dif==0 and y_dif==-1:
                        edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                        edge_type_check.append('v-')
                    elif x_dif==1 and y_dif==0:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                        edge_type_check.append('h+')
                    elif x_dif==-1 and y_dif==0:
                        edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                        edge_type_check.append('h-')
                
            # boundary
            if from_node_identifier not in sink+source:
                for edge_type in ['s0', 's1', 'v+', 'v-', 'h+', 'h-']:
                    if edge_type not in edge_type_check:
                        edges_info.append((from_node_identifier, from_node_identifier, edge_type))
                        edges_info.append((from_node_identifier, from_node_identifier, self.reverse_edge_type(edge_type)))
        return edges_info

    def reverse_edge_type(self, edge_type):
        if edge_type=='h+':
            return 'h-'
        elif edge_type=='h-':
            return 'h+'
        elif edge_type=='v+':
            return 'v-'
        elif edge_type=='v-':
            return 'v+'

    def get_edge_type(self, from_node_identifier, to_node_identifier):
        row_dif = int(to_node_identifier.split(',')[0]) - int(from_node_identifier.split(',')[0])
        col_dif = int(to_node_identifier.split(',')[1]) - int(from_node_identifier.split(',')[1])

        if col_dif==0:
            if row_dif==1:
                from_edge_type = 'v+'
                to_edge_type = 'v-'
            elif row_dif==-1:
                from_edge_type = 'v-'
                to_edge_type = 'v+'
        elif row_dif==0:
            if col_dif==1:
                from_edge_type = 'h+'
                to_edge_type = 'h-'
            elif col_dif==-1:
                from_edge_type = 'h-'
                to_edge_type = 'h+'
        else:
            raise(ValueError("Not adjacent error."))

        return from_edge_type, to_edge_type


            
    def add_pin_node(self, pin_node_identifier, connect_node_identifier):

        self.add_node(pin_node_identifier)

        from_edge_type, to_edge_type = self.get_edge_type(pin_node_identifier, connect_node_identifier)
        
        remove_edge = self.get_edge(connect_node_identifier, connect_node_identifier, edge_type=from_edge_type)
        self.remove_edge(remove_edge)
        remove_edge = self.get_edge(connect_node_identifier, connect_node_identifier, edge_type=to_edge_type)
        self.remove_edge(remove_edge)

        self.add_edge(pin_node_identifier, connect_node_identifier, data={'state':0, 'edge_type':from_edge_type})
        self.add_edge(connect_node_identifier, pin_node_identifier, data={'state':0, 'edge_type':to_edge_type})

    def get_end_node_identifiers(self):
        end_node_identifiers = {}
        node_coordinates = [[int(node.identifier.split(',')[0]), int(node.identifier.split(',')[1])] for node in self.nodes]
        df = pd.DataFrame(node_coordinates, columns=['row', 'col'])
        
        # west
        sorted_df = df.sort_values(['row', 'col'])
        sorted_df = sorted_df.drop_duplicates(subset='row', keep='first')
        end_node_identifiers['west'] = sorted_df.apply(lambda x: f"{x['row']},{x['col']}", axis=1).to_list()

        # east
        sorted_df = df.sort_values(['row', 'col'])
        sorted_df = sorted_df.drop_duplicates(subset='row', keep='last')
        end_node_identifiers['east'] = sorted_df.apply(lambda x: f"{x['row']},{x['col']}", axis=1).to_list()

        # south
        sorted_df = df.sort_values(['col','row'])
        sorted_df = sorted_df.drop_duplicates(subset='col', keep='first')
        end_node_identifiers['south'] = sorted_df.apply(lambda x: f"{x['row']},{x['col']}", axis=1).to_list()

        # north
        sorted_df = df.sort_values(['col','row'])
        sorted_df = sorted_df.drop_duplicates(subset='col', keep='last')
        end_node_identifiers['north'] = sorted_df.apply(lambda x: f"{x['row']},{x['col']}", axis=1).to_list()

        # # self
        # all = end_node_identifiers['left'] + end_node_identifiers['right'] + end_node_identifiers['down'] + end_node_identifiers['up']
        # end_node_identifiers['self'] = list(set(all))

        return end_node_identifiers


    def get_new_node_type(self, node_identifier, direction, xlim, ylim):

        row = int(node_identifier.split(',')[0])
        col = int(node_identifier.split(',')[1])

        if col==xlim[0] and row==ylim[0]:
            return 'southwest'
        elif col==xlim[0] and row==ylim[1]:
            return 'northwest'
        elif col==xlim[1] and row==ylim[0]:
            return 'southeast'
        elif col==xlim[1] and row==ylim[1]:
            return 'northeast'
        elif col==xlim[0]:
            return 'west'
        elif row==ylim[0]:
            return 'south'
        elif col==xlim[1]:
            return 'east'
        elif row==ylim[1]:
            return 'north'
        else:
            return 'inside'


    def get_new_node_identifier(self, node_identifier, direction):

        if direction=='west':
            return f"{node_identifier.split(',')[0]},{int(node_identifier.split(',')[1])-1}"

        elif direction=='east':
            return f"{node_identifier.split(',')[0]},{int(node_identifier.split(',')[1])+1}"

        elif direction=='south':
            return f"{int(node_identifier.split(',')[0])-1},{node_identifier.split(',')[1]}"

        elif direction=='north':
            return f"{int(node_identifier.split(',')[0])+1},{node_identifier.split(',')[1]}"
            

    def sync_boundary(self):

        for edge in self.edges:
            if edge.initial_node.identifier==edge.final_node.identifier:
                node_identifier = edge.initial_node.identifier
                
                if edge.data['edge_type']=='h+':
                    plus_state = self.get_edge(node_identifier, node_identifier, edge_type='h+').data['state']
                    minus_state = self.get_edge(node_identifier, node_identifier, edge_type='h-').data['state']
                    self.get_edge(node_identifier, node_identifier, edge_type='h+').data_update(key='state', val=minus_state)
                    self.get_edge(node_identifier, node_identifier, edge_type='h-').data_update(key='state', val=plus_state)

                elif edge.data['edge_type']=='v+':
                    plus_state = self.get_edge(node_identifier, node_identifier, edge_type='v+').data['state']
                    minus_state = self.get_edge(node_identifier, node_identifier, edge_type='v-').data['state']
                    self.get_edge(node_identifier, node_identifier, edge_type='v+').data_update(key='state', val=minus_state)
                    self.get_edge(node_identifier, node_identifier, edge_type='v-').data_update(key='state', val=plus_state)

    def to_plot(self, file_name):
        ovserver = Observer(self)
        ovserver.gv_plot(file_name)
        self.oup_pngs.append(file_name)
    
    def to_gif(self):
        ovserver = Observer(self)
        ovserver.to_gif(self.oup_pngs)


