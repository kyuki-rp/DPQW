import vtk
import os
import graphviz
from graphviz import Source
from graphviz import Graph
from graphviz import Digraph
from PIL import Image, ImageDraw, ImageFont
import glob
import cv2
import re
import numpy as np
import time

class Observer():

    def __init__(self, network):
        self.network = network
        self.png_names = []

    def gv_plot(self, dir, file_name, boundary_node_identifiers):

        self.graph = Digraph(format='png')
        self.graph.attr(splines ='true')

        for node in self.network.nodes:
            color = self.get_node_color(node, boundary_node_identifiers)
            self.graph.node(node.identifier, label=node.identifier, pos=f"{node.pos[0]},{node.pos[1]}!", fontsize = '10', style='filled', **color)

        # add edges
        for edge in self.network.edges:
            color = self.get_edge_color(edge)
            port = self.get_edge_port(edge)
            state = self.get_edge_state(edge)
            self.graph.edge(edge.initial_node.identifier, edge.final_node.identifier, **state, **color, **port)
           
        self.__to_png(dir, file_name)

    def get_node_color(self, node, boundary_node_identifiers):
        if node.identifier in boundary_node_identifiers:
            fillcolor=self.get_fillcolor(node.data.get('state'))
            return {'colorscheme':'rdylbu10', 'shape':'Msquare', 'color':'black', 'fillcolor':fillcolor}
        else:
            fillcolor=self.get_fillcolor(node.data.get('state'))
            return {'colorscheme':'rdylbu10', 'shape':'circle', 'color':'black', 'fillcolor':fillcolor}


    def get_fillcolor(self, state):

        # # カラーバーリサイズ
        node_state_max = 32
        denominater = 2

        if state<node_state_max*1/denominater**9:
            return '10'
        elif state<node_state_max*1/denominater**8:
            return '9'
        elif state<node_state_max*1/denominater**7:
            return '8'
        elif state<node_state_max*1/denominater**6:
            return '7'
        elif state<node_state_max*1/denominater**5:
            return '6'
        elif state<node_state_max*1/denominater**4:
            return '5'
        elif state<node_state_max*1/denominater**3:
            return '4'
        elif state<node_state_max*1/denominater**2:
            return '3'
        elif state<node_state_max*1/denominater:
            return '2'
        else:
            return '1'

    def get_edge_state(self, edge):
        state = edge.data['state']
        if state!=0:
            return {'label':f"{edge.data['state']:.2f}"}
        else:
            return {'label':''}

    def get_edge_color(self, edge):
        edge_type = edge.data['edge_type']
        state = edge.data['state']
        if state!=0:
            if edge_type=='s0':
                return {'color':'#ff00ff', 'fontcolor':'#ff00ff', 'style':'solid', 'penwidth':'2'}
            elif edge_type=='h+':
                return {'color':'#ff0000', 'fontcolor':'#ff0000', 'style':'solid', 'penwidth':'2'}
            elif edge_type=='h-':
                return {'color':'#0000ff', 'fontcolor':'#0000ff', 'style':'solid', 'penwidth':'2'}
            elif edge_type=='s1':
                return {'color':'#00ff00', 'fontcolor':'#00ff00', 'style':'solid', 'penwidth':'2'}
            elif edge_type=='v+':
                return {'color':'#ff0000', 'fontcolor':'#ff0000', 'style':'solid', 'penwidth':'2'}
            elif edge_type=='v-':
                return {'color':'#0000ff', 'fontcolor':'#0000ff', 'style':'solid', 'penwidth':'2'}
        else:
            if edge_type=='s0':
                return {'color':'#ff00ff99', 'fontcolor':'#ff00ff99', 'style':'dotted'}
            elif edge_type=='h+':
                return {'color':'#ff000099', 'fontcolor':'#ff000099', 'style':'dotted'}
            elif edge_type=='h-':
                return {'color':'#0000ff99', 'fontcolor':'#0000ff99', 'style':'dotted'}
            elif edge_type=='s1':
                return {'color':'#00ff0099', 'fontcolor':'#00ff0099', 'style':'dotted'}
            elif edge_type=='v+':
                return {'color':'#ff000099', 'fontcolor':'#ff000099', 'style':'dotted'}
            elif edge_type=='v-':
                return {'color':'#0000ff99', 'fontcolor':'#0000ff99', 'style':'dotted'}


    def get_edge_port(self, edge):
        if edge.data['edge_type']=='s0':
            return {'tailport':'ne', 'headport':'ne'}
        elif edge.data['edge_type']=='s1':
            return {'tailport':'sw', 'headport':'sw'}
        elif edge.initial_node.identifier==edge.final_node.identifier and edge.data['edge_type']=='h+':
            return {'tailport':'w', 'headport':'w'}
        elif edge.initial_node.identifier==edge.final_node.identifier and edge.data['edge_type']=='h-':
            return {'tailport':'e', 'headport':'e'}
        elif edge.initial_node.identifier==edge.final_node.identifier and edge.data['edge_type']=='v+':
            return {'tailport':'s', 'headport':'s'}
        elif edge.initial_node.identifier==edge.final_node.identifier and edge.data['edge_type']=='v-':
            return {'tailport':'n', 'headport':'n'}
        else:
            return {}

    def __to_png(self, dir, file_name):
        try:
            self.graph.render(f'{dir}/_temp.dot', view=True)
        except:
            pass
        os.system(f'dot -Kfdp -n -Tpng {dir}/_temp.dot -o {dir}/{file_name}')



# graphvizインストール
# https://niwakomablog.com/graphviz-error-handling/



