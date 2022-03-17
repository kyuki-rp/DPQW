import numpy as np
import pandas as pd
from src.edge import Edge
from src.node import Node
from src.observer import Observer
from src.quantumwalk import QuantumWalk

class Network():
    '''
    A directed graph class that can store multiedges.
    This class wraps networkx.
    '''
    def __init__(self):
        self.edges = []
        self.nodes = []
    
    def add_node(self, identifier):
        '''
        Adding method for node
        '''
        if identifier not in [node.identifier for node in self.nodes]:
            pos = [int(identifier.split(',')[0]),int(identifier.split(',')[1])]
            new_node = Node(identifier, pos)
            self.nodes.append(new_node)

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

    def custom(self, node_identifiers, assignments, initial_state={}):
        
        # setting nodes
        for node_identifier in node_identifiers:
            self.add_node(node_identifier)
        
        # setting edges
        edges_info = self.get_edge_info(node_identifiers)
        for (from_node_identifier, to_node_identifier, edge_type) in edges_info:
            self.add_edge(from_node_identifier, to_node_identifier, data={'state':0, 'edge_type':edge_type})

        # setting edges initial state
        for edge in self.edges:
            if f"{edge.initial_node}->{edge.final_node}" in initial_state.keys():
                edge.data_update(key='state',val=initial_state["{edge.initial_node}->{edge.final_node}"])
            else:
                edge.data_update(key='state',val=0)

    def get_edge_info(self, node_identifiers):

        edges_info = []
        for from_node_identifier in node_identifiers:
            for to_node_identifier in node_identifiers:
                x_dif = int(to_node_identifier.split(',')[0]) - int(from_node_identifier.split(',')[0])
                y_dif = int(to_node_identifier.split(',')[1]) - int(from_node_identifier.split(',')[1])
                
                if x_dif==0 and y_dif==0:
                    edges_info.append((from_node_identifier, to_node_identifier, 's0'))
                    edges_info.append((from_node_identifier, to_node_identifier, 's1'))
                elif x_dif==0 and y_dif==1:
                    edges_info.append((from_node_identifier, to_node_identifier, 'v+'))
                elif x_dif==0 and y_dif==-1:
                    edges_info.append((from_node_identifier, to_node_identifier, 'v-'))
                elif x_dif==1 and y_dif==0:
                    edges_info.append((from_node_identifier, to_node_identifier, 'h+'))
                elif x_dif==-1 and y_dif==0:
                    edges_info.append((from_node_identifier, to_node_identifier, 'h-'))
                
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

    def to_plot(self, dir, file_name, boundary_node_identifiers):
        ovserver = Observer(self)
        ovserver.gv_plot(dir, file_name, boundary_node_identifiers)

    def evolve(self, assignments, coin, xi, step):
        qw = QuantumWalk()
        graph_edges, Us, inflow = qw.get_matrix(assignments, self.edges, coin, xi)

        # Step set coin
        step_set_U = 1
        for Ui in Us:
            step_set_U = Ui * step_set_U

        # Evolve
        outflow = (step_set_U ** (step//len(Us))) * inflow
        inflow = outflow
        self.log.write(step=step//len(Us)*len(Us), graph_edges=graph_edges ,outflow=outflow)

        # Evolve remainder
        for step_i in range(step-step//len(Us)*len(Us)):
            outflow = Us[step_i] * inflow
            inflow = outflow
            self.log.write(step=step//len(Us)*len(Us)+(step_i+1), graph_edges=graph_edges, outflow=outflow)

        return graph_edges, outflow

    def data_update(self, graph_edges, outflow):
        new_states = [(outflow_edge, outflow_val) for outflow_edge, outflow_val in zip(graph_edges[:, 3], outflow.toarray().flatten()[:-1])]

        # edge overwrite
        for edge, state in new_states:
            edge.data_update(key='state',val=state)

        # node overwrite
        for node in self.nodes:
            states = np.array([edge.data['state'] for edge in node.inedges])
            sum_states = np.dot(states, states.conjugate())
            if sum_states.imag==0:
                sum_states=sum_states.real
            else:
                raise ValueError("error!")
            node.data_update(key='state',val=sum_states)

    def convergence(self, assignments, coin_func, xjRatio, xi, output_dir):
        
        coin = coin_func(xjRatio)
        
        self.log = EdgeLog()
        for i in range(1,100):
            step = 10**i + 1
            graph_edges, outflow_old = self.evolve(assignments, coin, xi=xi, step=step)
            graph_edges, outflow_new = self.evolve(assignments, coin, xi=xi, step=step+2)

            # Calculate difference
            outflow_dif = outflow_old - outflow_new
            outflow_dif_sum = np.abs((outflow_dif.T * outflow_dif.conjugate()).sum())
            print(step, outflow_dif_sum)

            outflow_old = outflow_new

            # Break
            if outflow_dif_sum<1e-8:
                break

        # Output edge log
        self.log.to_csv(dir=f'../{output_dir}', file_name=f'edge_log(xjRatio={xjRatio};xi={xi})')

        # # Update graph
        # self.data_update(graph_edges, outflow_new)

        # # Plot graph
        # boundary_node_identifiers = [assignment.split("->")[0] for assignment in assignments.keys()]
        # self.to_plot(dir=f'../{output_dir}', file_name=f'gv(xjRatio={xjRatio};xi={xi}).png', boundary_node_identifiers=boundary_node_identifiers)


    def evolve_test(self, assignments, coin_func, xjRatio, xi, output_dir):
        
        coin = coin_func(xjRatio)
        
        self.log = EdgeLog()
        for step in range(1, 10):
            graph_edges, outflow = self.evolve(assignments, coin, xi=xi, step=step)

            # Update graph
            self.data_update(graph_edges, outflow)

            # Plot graph
            boundary_node_identifiers = [assignment.split("->")[0] for assignment in assignments.keys()]
            self.to_plot(dir=f'../{output_dir}', file_name=f'gv(xjRatio={xjRatio};xi={xi};step={step}).png', boundary_node_identifiers=boundary_node_identifiers)

        # Output edge log
        self.log.to_csv(dir=f'../{output_dir}', file_name=f'edge_log(xjRatio={xjRatio};xi={xi})')


class EdgeLog():
    '''
    EdgeLog class.
    '''
    def __init__(self):
        self.edge_df = pd.DataFrame()
    
    def write(self, step, graph_edges, outflow):
        cols = self.get_col(graph_edges)
        outflow_se = pd.Series(outflow.toarray().flatten()[:-1], index=cols, name=step)
        self.edge_df = self.edge_df.append(outflow_se)

    def to_csv(self, dir, file_name):
        self.edge_df.to_csv(f'{dir}/{file_name}.csv')

    def get_col(self, graph_edges):
        col_df = pd.DataFrame(graph_edges[:,:-1], columns=["initial_node", "final_node", "edge_type"])
        col_df["edge_type"] = col_df["edge_type"].map({0:"s0",1:"h+",2:"h-", 3:"s1", 4:"v+", 5:"v-"})
        return col_df.apply(lambda x: f"{x['initial_node']}->{x['final_node']}:{x['edge_type']}", axis=1).tolist()