#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

class Node():
    def __init__(self, identifier, pos):
        self.identifier = identifier
        self.inedges = []
        self.outedges = []
        self.data = {}
        self.pos = pos


    def add_inedges(self, edge):
        self.inedges.append(edge)

    def remove_inedges(self, edge):
        self.inedges.remove(edge)
        
    def add_outedges(self, edge):
        self.outedges.append(edge)

    def remove_outedges(self, edge):
        self.outedges.remove(edge)

    def data_update(self, key, val):
        self.data[key] = val

    def get_state(self):
        return [(inedge.initial_node.identifier, inedge.final_node.identifier, inedge.data['state']) for inedge in self.inedges]
        
    def get_indegree(self):
        return len(self.inedges)
    
    def get_outdegree(self):
        return len(self.outedges)

    def dump_info(self):
        print(f"{self.identifier}:{self.data}")
        print(f"  + inedges:{','.join([f'{edge.initial_node.identifier}->{edge.final_node.identifier}' for edge in self.inedges])}")
        print(f"  + outedges:{','.join([f'{edge.initial_node.identifier}->{edge.final_node.identifier}' for edge in self.outedges])}")

