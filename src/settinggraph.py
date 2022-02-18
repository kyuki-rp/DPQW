#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
import tkinter
import json
import tkinter.ttk as ttk
from tkinter import filedialog

class Setting():
    def __init__(self):
        pass

    def call(self):

        self.setting_select = SettingSelect()
        self.setting_select.main()

        if self.setting_select.var.get()==1:
            self.set_graph_size = SettingGraphSize()
            self.set_graph_size.main()

            self.set_graph_node = SettingGraphNode(self.set_graph_size)
            self.set_graph_node.main()

            self.set_sink = SettingSink(self.set_graph_node)
            self.set_sink.main()

            self.set_source = SettingSource(self.set_graph_node)
            self.set_source.main()

            self.source_cycle = SourceCycle(self.set_source)
            self.source_cycle.main()

            self.node_theta = NodeTheta(self.set_graph_node, self.set_sink, self.set_source)
            self.node_theta.main()

            self.set_xi = SettingXi()
            self.set_xi.main()

            self.set_max_step = SettingMaxStep()
            self.set_max_step.main()

            self.config = {'node_identifiers': [k for k,v in self.set_graph_node.checkboxs.items() if v.get()==True],
                            'sink': [k for k,v in self.set_sink.checkboxs.items() if v.get()==True],
                            'source': [k for k,v in self.set_source.checkboxs.items()  if v.get()==True],
                            'source_cycles':self.source_cycle.source_cycles,
                            'node_thetas':self.node_theta.node_thetas,
                            'xi':self.set_xi.xi,
                            'max_step':self.set_max_step.max_step
                          }


        elif self.setting_select.var.get()==2:
            self.setting_json = SettingJson()
            self.setting_json.main()
            self.config = self.setting_json.config

            
        else:
            raise ValueError("Not implemented.")

        self.__to_json(self.config, 'output/config.json')


    def __to_json(self, output_dict, file_path):
        os.makedirs('output', exist_ok=True)
        with open(file_path, 'w') as outfile:
            json.dump(output_dict, outfile)




class SettingSelect():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("DP graph")
        self.root.geometry(f"400x300")

    def main(self):

        self.var = tkinter.IntVar()
        self.var.set(0)

        radio1 = tkinter.Radiobutton(text="Create the configuration file.", variable=self.var, value=1)
        radio1.pack(padx=10, pady=10, side=tkinter.TOP)

        radio2 = tkinter.Radiobutton(text="Select the configuration file.", variable=self.var, value=2)
        radio2.pack(padx=10, pady=0, side=tkinter.TOP)

        # Button for setting graph size
        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()


    def __next(self, event):
        print(f"Get radio button: {self.var.get()}")
        self.root.destroy()


class SettingGraphSize():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("DP graph")
        self.root.geometry(f"400x300")
        
    def main(self):
        # Message
        Static = tkinter.Label(text="Fill graph size.")
        Static.place(x=5, y=10)

        # Setting graph size
        Static = tkinter.Label(text="Graph size:")
        Static.place(x=5, y=30)

        self.edit_box_x = tkinter.Entry(width=3)
        self.edit_box_x.insert(tkinter.END, 10)
        self.edit_box_x.place(x=75, y=30)

        Static = tkinter.Label(text="×")
        Static.place(x=95, y=30)

        self.edit_box_y = tkinter.Entry(width=3)
        self.edit_box_y.insert(tkinter.END, 10)
        self.edit_box_y.place(x=115, y=30)

        # Button for setting graph size
        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        self.x_size = self.edit_box_x.get()
        self.y_size = self.edit_box_y.get()

        print(f"Get graph size: {self.x_size}, {self.y_size}")
        self.root.destroy()


class SettingGraphNode():
    def __init__(self, set_graph_size):
        self.root = tkinter.Tk()
        self.root.title("DP graph")
        self.root.geometry(f"400x300")

        self.x_size = set_graph_size.x_size
        self.y_size = set_graph_size.y_size
        
    def main(self):
        # Message
        Static = tkinter.Label(text="Select graph node.")
        Static.place(x=5, y=10)

        xmax = int(self.x_size)-1
        ymax = int(self.y_size)-1

        self.checkboxs = {}
        for x in range(int(self.x_size)):
            for y in range(int(self.y_size)):
                self.checkboxs[f'{x},{ymax-y}'] = tkinter.BooleanVar()
                self.checkboxs[f'{x},{ymax-y}'].set(False)
                CheckBox = tkinter.Checkbutton(variable=self.checkboxs[f'{x},{ymax-y}'])
                CheckBox.place(x=30+20*x, y=70+20*y)

        for x in range(int(self.x_size)):
            Static = tkinter.Label(text=x)
            Static.place(x=35+20*x, y=90+20*ymax)

        for y in range(int(self.y_size)):
            Static = tkinter.Label(text=ymax-y)
            Static.place(x=10, y=70+20*y)

        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        for k, v in self.checkboxs.items():
            print(k, v.get())
        self.root.destroy()


class SettingSink():
    def __init__(self, set_graph_node):
        self.root = tkinter.Tk()
        self.root.title("DP graph")
        self.root.geometry(f"400x300")
        self.set_graph_node = set_graph_node
        self.x_size = set_graph_node.x_size
        self.y_size = set_graph_node.y_size
        
    def main(self):

        # Message
        Static = tkinter.Label(text="Select sink node.")
        Static.place(x=5, y=10)

        xmax = int(self.x_size)-1
        ymax = int(self.y_size)-1

        self.checkboxs = {}
        for x in range(int(self.x_size)):
            for y in range(int(self.y_size)):
                if f'{x},{ymax-y}' in [k for k, v in self.set_graph_node.checkboxs.items() if v.get()==True]:
                    self.checkboxs[f'{x},{ymax-y}'] = tkinter.BooleanVar()
                    self.checkboxs[f'{x},{ymax-y}'].set(False)
                    CheckBox = tkinter.Checkbutton(variable=self.checkboxs[f'{x},{ymax-y}'])
                    CheckBox.place(x=30+20*x, y=70+20*y)

        for x in range(int(self.x_size)):
            Static = tkinter.Label(text=x)
            Static.place(x=35+20*x, y=90+20*ymax)

        for y in range(int(self.y_size)):
            Static = tkinter.Label(text=ymax-y)
            Static.place(x=10, y=70+20*y)

        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        for k, v in self.checkboxs.items():
            print(k, v.get())
        self.root.destroy()


class SettingSource():
    def __init__(self, set_graph_node):
        self.root = tkinter.Tk()
        self.root.title("DP graph")
        self.root.geometry(f"400x300")
        self.set_graph_node = set_graph_node
        self.x_size = set_graph_node.x_size
        self.y_size = set_graph_node.y_size
        
    def main(self):
        # Message
        Static = tkinter.Label(text="Select source node.")
        Static.place(x=5, y=10)

        xmax = int(self.x_size)-1
        ymax = int(self.y_size)-1

        self.checkboxs = {}
        for x in range(int(self.x_size)):
            for y in range(int(self.y_size)):
                if f'{x},{ymax-y}' in [k for k, v in self.set_graph_node.checkboxs.items() if v.get()==True]:
                    self.checkboxs[f'{x},{ymax-y}'] = tkinter.BooleanVar()
                    self.checkboxs[f'{x},{ymax-y}'].set(False)
                    CheckBox = tkinter.Checkbutton(variable=self.checkboxs[f'{x},{ymax-y}'])
                    CheckBox.place(x=30+20*x, y=70+20*y)

        for x in range(int(self.x_size)):
            Static = tkinter.Label(text=x)
            Static.place(x=35+20*x, y=90+20*ymax)

        for y in range(int(self.y_size)):
            Static = tkinter.Label(text=ymax-y)
            Static.place(x=10, y=70+20*y)

        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        for k, v in self.checkboxs.items():
            print(k, v.get())
        self.root.destroy()


class SourceCycle():
    def __init__(self, set_source):
        self.root = tkinter.Tk()
        self.root.title('Tkinter training')
        self.root.geometry("400x300")

        self.set_source = set_source

    def main(self):

        # Message
        Static = tkinter.Label(text="Fill the source cycle.")
        Static.place(x=5, y=10)

        self.edit_boxs = {}
        y = 0
        for source in [k for k,v in self.set_source.checkboxs.items() if v.get()==True]:
            y += 1
            Static = tkinter.Label(text=f"{source}: ", width = 5)
            Static.place(x=10, y=30+20*y)
            self.edit_boxs[source] = tkinter.Entry(width = 50)
            self.edit_boxs[source].insert(tkinter.END, '1,0,1,0')
            self.edit_boxs[source].place(x=50, y=30+20*y)

        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        self.source_cycles = {}
        for k, v in self.edit_boxs.items():
            self.source_cycles[k] = v.get()
            print(f"Edit_box: {v.get()}")
        self.root.destroy()

class NodeTheta():
    def __init__(self, set_graph_node, set_sink, set_source):
        self.root = tkinter.Tk()
        self.root.title('Tkinter training')
        self.root.geometry("400x300")

        self.nodes = set([k for k,v in set_graph_node.checkboxs.items() if v.get()==True]) - set([k for k,v in set_sink.checkboxs.items() if v.get()==True]) - set([k for k,v in set_source.checkboxs.items() if v.get()==True])

    def main(self):

        # Message
        Static = tkinter.Label(text="Fill the node theta.")
        Static.place(x=5, y=10)

        self.edit_boxs = {}
        y = 0
        for node in self.nodes:
            y += 1
            Static = tkinter.Label(text=f"{node}: ", width = 5)
            Static.place(x=10, y=30+20*y)
            self.edit_boxs[node] = tkinter.Entry(width = 50)
            self.edit_boxs[node].insert(tkinter.END, 'np.arcsin(np.sqrt(2/3))')
            self.edit_boxs[node].place(x=50, y=30+20*y)

        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        self.node_thetas = {}
        for k, v in self.edit_boxs.items():
            self.node_thetas[k] = v.get()
            print(f"Edit_box: {v.get()}")
        self.root.destroy()


class SettingXi():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Tkinter training')
        self.root.geometry("400x300")

    def main(self):

        # Message
        Static = tkinter.Label(text="Fill the xi.")
        Static.place(x=5, y=10)

        # Setting graph size
        Static = tkinter.Label(text="Xi:")
        Static.place(x=5, y=30)

        self.edit_box = tkinter.Entry(width=10)
        self.edit_box.insert(tkinter.END, 0)
        self.edit_box.place(x=75, y=30)

        # Button for setting graph size
        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        self.xi = self.edit_box.get()
        print(f"Edit_box: {self.edit_box.get()}")
        self.root.destroy()


class SettingMaxStep():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Tkinter training')
        self.root.geometry("400x300")

    def main(self):

        # Message
        Static = tkinter.Label(text="Fill the max step.")
        Static.place(x=5, y=10)

        # Setting graph size
        Static = tkinter.Label(text="Max step:")
        Static.place(x=5, y=30)

        self.edit_box = tkinter.Entry(width=10)
        self.edit_box.insert(tkinter.END, 100)
        self.edit_box.place(x=75, y=30)

        # Button for setting graph size
        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)

        # mainloop
        self.root.mainloop()

    def __next(self, event):
        self.max_step = int(self.edit_box.get())
        print(f"Edit_box: {self.edit_box.get()}")
        self.root.destroy()


class SettingJson():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Tkinter training')
        self.root.geometry("400x300")

    def main(self):
        file_button = tkinter.Button(text = 'File', width = 5, command = self.__open_file_command)
        file_button.pack(padx=10, pady=10, side=tkinter.LEFT, anchor=tkinter.NW)
        self.edit_box = tkinter.Entry(width = 50)
        self.edit_box.pack(padx=10, pady=15, side=tkinter.TOP, anchor=tkinter.NW, fill=tkinter.X)
        button = tkinter.Button(text='Next', width=10)
        button.bind("<Button-1>", self.__next)
        button.pack(padx=10, pady=10, side=tkinter.BOTTOM, anchor=tkinter.SE)
        
        # mainloop
        self.root.mainloop()


    def __open_file_command(self):
        file_path = filedialog.askopenfilename(filetypes = [('JSONファイル', '*.json')])
        self.edit_box.delete(0, tkinter.END)
        self.edit_box.insert(tkinter.END, file_path)

    def __next(self, event):
        self.file_path = self.edit_box.get()
        print(f"Setting json file path: {self.file_path}")
        with open(self.file_path) as f:
            self.config = json.load(f)

        self.root.destroy()


