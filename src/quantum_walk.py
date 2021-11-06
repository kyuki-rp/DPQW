#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import Counter

class QuantumWalk():
    '''
    Quantum walk class.
    '''
    def __init__(self, graph, max_step):
        self.__graph = graph
        self.step = Step()
        self.max_step = max_step
        
    def get_sorted_adjacent_edges(self, node):

        inflow = np.array([(edge.data['edge_type'], edge) for edge in node.inedges])
        outflow = np.array([(edge.data['edge_type'], edge) for edge in node.outedges])

        # print(f"- old::{node.identifier}: {[edge.data['state'] for edge in node.inedges]}")
        
        if len(inflow)>6:
            inflow_ = []
            for edge_type, edge in inflow:
                if edge_type in [val for (val, cnt) in Counter([edge_type for edge_type, _ in inflow]).items() if cnt!=1]: # duplicate key
                    if edge.initial_node.identifier!=edge.final_node.identifier: # boundary
                        inflow_.append([edge_type, edge])
                else:
                    inflow_.append([edge_type, edge])
            inflow = np.array(inflow_)

        if len(inflow) >= 2:
            inflow_sort_strs = ['s0','h+', 'h-','s1','v+','v-']
            outflow_sort_strs  = ['s0','h+', 'h-','s1','v+','v-']
            inflow  = np.array([inflow[np.where(inflow[:,0]==sort_str)[0][0],:] for sort_str in inflow_sort_strs]) # Sort by edge color
            outflow  = np.array([outflow[np.where(outflow[:,0]==sort_str)[0][0],:] for sort_str in outflow_sort_strs]) # Sort by edge color

        # print(f"+ old::{node.identifier}: {[edge.data['state'] for edge in inflow[:,1]]}")

        if len(inflow) == 0:
            sorted_inedges = inflow
            sorted_outedges = outflow
        else:
            sorted_inedges = inflow[:,1]
            sorted_outedges = outflow[:,1]

        return sorted_inedges, sorted_outedges



    def evolve(self):
        # step
        self.step.add()

        # calculate
        new_states = []
        for node in self.__graph.nodes:
            source_val = next(node.data['source_cycle'])
            new_state = self.get_new_state(node, source_val)
            new_states += new_state

        # overwrite
        for edge in self.__graph.edges:
            edge.data_update(key='state',val=0)
        for edge, state in new_states:
            edge.data_update(key='state',val=state)

        self.__graph.sync_boundary()

        # overwrite
        for node in self.__graph.nodes:
            states = np.array([edge.data['state'] for edge in node.inedges])
            sum_states = np.dot(states, states)
            node.data_update(key='state',val=sum_states)
        
        self.step.write_log(self.__graph)

            

    def get_new_state(self, node, source_val):

        # sink
        if node.data['coin_name']=='sink':
            return [(edge, 0) for edge in node.outedges]

        # source
        elif node.data['coin_name']=='source':
            return [(edge, source_val) for edge in node.outedges]

        # inedges are 0s
        elif sum([edge.data['state']!=0 for edge in node.inedges])==0:
            return [(edge, 0) for edge in node.outedges]

        # dressed_photon
        elif node.data['coin_name']=='dressed_photon':
            coin_cls = Coin(node)
            coin = coin_cls.get(coin_name='dressed_photon', theta=node.data['coin_theta'])

            # coin = [[a,b],
            #         [c,d]]
            coin_a = coin[:3, :3]
            coin_b = coin[:3, 3:]
            coin_c = coin[3:, :3]
            coin_d = coin[3:, 3:]

            sorted_inedges, sorted_outedges = self.get_sorted_adjacent_edges(node)

            # print('input:', node.identifier, [edge.data['state'] for edge in sorted_inedges])

            # calculate next state
            inedges_a = sorted_inedges[:3]
            inedges_b = sorted_inedges[3:]
            outedges_a = sorted_outedges[:3]
            outedges_b = sorted_outedges[3:]
            vec_a = np.array([edge.data['state'] for edge in inedges_a])
            vec_b = np.array([edge.data['state'] for edge in inedges_b])

            new_state_a = coin_b.dot(vec_a)
            new_state_b = coin_c.dot(vec_b)

            new_state_a = [(edge, new_state_a[i]) for i, edge in enumerate(outedges_b)]
            new_state_b = [(edge, new_state_b[i]) for i, edge in enumerate(outedges_a)]

            # if node.identifier =='0,2':
            #     print(':::',vec_a, vec_b, coin_b, coin_c, new_state_a, new_state_b)

            # print('output:', node.identifier, [i[1] for i in new_state_a + new_state_b])


            return new_state_a + new_state_b

        else:
            raise(ValueError("Not implemented error."))

    def to_plot(self, file_name):
        if self.step.step<100 or ((self.step.step%100==0 or self.step.step%100==1) and self.step.step<1000) or ((self.step.step%1000==0 or self.step.step%1000==1) and self.step.step<10000) or (self.step.step%10000==0 or self.step.step%10000==1):
            self.__graph.to_plot(file_name)
            print(file_name)



class Coin():
    '''
    Setteing class of quantum coin per node.
    Now, only Grover walk is implemented.
    '''
    def __init__(self, node):
        self.node = node
        self.degree = node.get_indegree()

    # def get(self, coin_name):
    #     return eval(f'self.{coin_name}()')

    def get(self, coin_name, theta):
        return self.dressed_photon(theta)

    def grover(self):
        if self.degree in [0, 1]:
            coin = np.identity(self.degree)
            return coin
        elif self.degree==2:
            coin = np.array([[0,1],[1,0]])
            return coin
        elif self.degree>=3:
            n = self.degree
            uni_array = np.zeros((self.degree, self.degree)) + 2/n
            coin = uni_array + np.eye(self.degree) * (-2/n + 2/n -1)
            # coin = np.fliplr(coin)
            return coin

    def dressed_photon(self, theta=np.arcsin(np.sqrt(2/3))):
        zero = np.zeros((3,3))
        h_theta = np.array([[np.cos(2*theta), np.sin(2*theta)/np.sqrt(2), np.sin(2*theta)/np.sqrt(2)],
                            [np.sin(2*theta)/np.sqrt(2), -np.cos(theta)**2, np.sin(theta)**2],
                            [np.sin(2*theta)/np.sqrt(2), np.sin(theta)**2, -np.cos(theta)**2]
                        ])

        up_coin = np.hstack([zero, h_theta])
        down_coin = np.hstack([h_theta, zero])
        coin = np.vstack([up_coin, down_coin])
        return coin



class Step():
    def __init__(self):
        self.step = 0
        self.node_df = pd.DataFrame()
        self.edge_df = pd.DataFrame()
        
    def add(self):
        self.step += 1

    def write_log(self, graph):
        for node in graph.nodes:
            self.node_df.loc[self.step, node.identifier] = node.data['state']
        for edge in graph.edges:
            self.edge_df.loc[self.step, f"{edge.initial_node.identifier}->{edge.final_node.identifier}:{edge.data['edge_type']}"] = edge.data['state']

    def to_csv(self):
        self.node_df.to_csv('output/node_log.csv', index=False)
        self.edge_df.to_csv('output/edge_log.csv', index=False)
