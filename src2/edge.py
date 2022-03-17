#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.node import Node

class Edge():
    def __init__(self, initial_node:Node, final_node:Node, data={}):
        self.initial_node = initial_node
        self.final_node = final_node
        self.data = data

    def data_update(self, key, val):
        self.data[key] = val

    def dump_info(self):
        print(f"{self.initial_node.identifier}->{self.final_node.identifier}:{self.data}")
