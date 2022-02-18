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

    def gv_plot(self, file_name):

        self.graph = Digraph(format='png')
        self.graph.attr(splines ='true')

        for node in self.network.nodes:
            color = self.get_node_color(node)
            self.graph.node(node.identifier, label=node.identifier, pos=f"{node.pos[0]},{node.pos[1]}!", fontsize = '10', shape='circle', style='filled', **color)

        # add edges
        for edge in self.network.edges:
            color = self.get_edge_color(edge)
            port = self.get_edge_port(edge)
            state = self.get_edge_state(edge)
            self.graph.edge(edge.initial_node.identifier, edge.final_node.identifier, **state, **color, **port)
                
           
        os.makedirs('output', exist_ok=True)
        self.__to_png(f'output/{file_name}')

    def get_node_color(self, node):
        coin_name = node.data.get('coin_name')
        if coin_name=='sink':
            return {'color':'blue', 'fillcolor':'lightblue'}
        elif coin_name=='source':
            return {'color':'red', 'fillcolor':'lightpink'}
        else:
            fillcolor = self.get_fillcolor(node.data.get('state'))
            return {'colorscheme':'rdylbu10', 'color':'black', 'fillcolor':fillcolor}


    def get_fillcolor(self, state):
        # normalize
        # node_state_max = max([node.data['state'] for node in self.network.nodes])
        # denominater = np.sqrt(np.sqrt(2))

        # # カラーバーリサイズ
        node_state_max = 32
        denominater = 2

        # # # カラーバーリサイズ
        # node_state_max = 10
        # denominater = 10**(-7)

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

    def __to_png(self, file_name):
        try:
            self.graph.render('output/_temp.dot', view=True)
        except:
            pass
        os.system(f'dot -Kfdp -n -Tpng output/_temp.dot -o {file_name}')

        # os.remove('_temp.dot')


# graphvizインストール
# https://niwakomablog.com/graphviz-error-handling/
    def to_gif(self, png_names):
        images = []
        for png_name in png_names:
            image = Image.open(f'output/{png_name}') 
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), re.findall(r'\d+', png_name)[0], font= ImageFont.truetype("arial.ttf", 64), fill='red') 
            images.append(image)

        images[0].save('output/out.gif', save_all=True, append_images=images[1:], duration=400, loop=0)


    # def to_movie(self, png_names):

    #     img_array = []
    #     for filename in png_names:
    #         img = cv2.imread(f'output/{filename}')
    #         height, width, layers = img.shape
    #         size = (width, height)
    #         img_array.append(img)

    #     name = 'project.mp4'
    #     out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MP4V'), 5.0, size)

    #     for i in range(len(img_array)):
    #         out.write(img_array[i])
    #     out.release()

