import numpy as np
import os
import json
import shutil
import sys

sys.path.append('../')

from src.network import Network
from src.quantumwalk import QuantumWalk


# Create config
def create_config(input_n, bn_act):
       node_identifiers = [f"{i},{j}" for i in range(input_n+2) for j in range(input_n+2) if (i+j>=input_n) and not (i==0 and j==input_n+1) and not (i==input_n+1 and j==0) and not (i==input_n+1 and j==input_n+1)]

       assignments = dict(
              [(f"{i},{input_n+1}->{i},{input_n}", bn_act) for i in range(1, input_n+1)]
              + [(f"{input_n+1},{j}->{input_n},{j}", bn_act) for j in range(1, input_n+1)] 
              + [(f"{i},{j}->{i},{j+1}", [1,0]) for i in range(input_n+2) for j in range(input_n+2) if i+j==input_n and j!=input_n]
              + [(f"{i},{j}->{i+1},{j}", bn_act) for i in range(input_n+2) for j in range(input_n+2) if i+j==input_n and i!=input_n]
       )
       assignments[f"{input_n},{input_n+1}->{input_n},{input_n}"] = [0, 0]

       config = {
       "node_identifiers": node_identifiers,
       "assignments": assignments
       }
 
       if bn_act==["reflect", "reflect"]:
           config_file_name = f"config({input_n};reflect).json"
       else:
           config_file_name = f"config({input_n};sink).json"

       with open(f'..\configs\{config_file_name}', 'w') as f:
           json.dump(config, f, ensure_ascii=False, indent=4)

# create_config(input_n=5, bn_act=["reflect", "reflect"])
# create_config(input_n=5, bn_act=[0,0])
# create_config(input_n=7, bn_act=["reflect", "reflect"])
# create_config(input_n=7, bn_act=[0,0])
# create_config(input_n=9, bn_act=["reflect", "reflect"])
# create_config(input_n=9, bn_act=[0,0])
# create_config(input_n=11, bn_act=["reflect", "reflect"])
# create_config(input_n=11, bn_act=[0,0])
# create_config(input_n=13, bn_act=["reflect", "reflect"])
# create_config(input_n=13, bn_act=[0,0])
# create_config(input_n=15, bn_act=["reflect", "reflect"])
# create_config(input_n=15, bn_act=[0,0])
# create_config(input_n=17, bn_act=["reflect", "reflect"])
# create_config(input_n=17, bn_act=[0,0])
# create_config(input_n=19, bn_act=["reflect", "reflect"])
# create_config(input_n=19, bn_act=[0,0])
create_config(input_n=21, bn_act=["reflect", "reflect"])
# create_config(input_n=21, bn_act=[0,0])


def get_coin(xjRatio):
    theta = np.arctan(np.sqrt(2)/(xjRatio))
    coin = np.array([[0,                          0,                          0,                          np.cos(2*theta),            np.sin(2*theta)/np.sqrt(2), np.sin(2*theta)/np.sqrt(2)],
                     [0,                          0,                          0,                          np.sin(2*theta)/np.sqrt(2), -np.cos(theta)**2,          np.sin(theta)**2          ],
                     [0,                          0,                          0,                          np.sin(2*theta)/np.sqrt(2), np.sin(theta)**2,           -np.cos(theta)**2         ],
                     [np.cos(2*theta),            np.sin(2*theta)/np.sqrt(2), np.sin(2*theta)/np.sqrt(2), 0,                          0,                          0                         ],
                     [np.sin(2*theta)/np.sqrt(2), -np.cos(theta)**2,          np.sin(theta)**2,           0,                          0,                          0                         ],
                     [np.sin(2*theta)/np.sqrt(2), np.sin(theta)**2,           -np.cos(theta)**2,          0,                          0,                          0                         ],         
       ])
    return coin


# ファイル名取得
files = os.listdir(f'../configs')

for file in files:

    output_dir = file.replace('config', 'output').replace('.json', '')
    os.makedirs(f'../{output_dir}', exist_ok=True)
    shutil.copy(f"../configs/{file}", f"../{output_dir}/config.json")

    # config読み込み
    with open(f"../{output_dir}/config.json") as f:
        config = json.load(f)

    graph = Network()
    graph.custom(node_identifiers=config["node_identifiers"], assignments=config["assignments"])

    for xjRatio in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]:
        for xi in range(91):
            if (xjRatio>=0.2 and xi>=77) or xjRatio>0.2:
                graph.convergence(assignments=config["assignments"], coin_func=get_coin, xjRatio=xjRatio, xi=xi, output_dir=output_dir)


# output_dir="evolve_test"
# os.makedirs(f'../{output_dir}', exist_ok=True)

# # config読み込み
# with open(f"../configs/config(5;reflect).json") as f:
#     config = json.load(f)

# graph = Network()
# graph.custom(node_identifiers=config["node_identifiers"], assignments=config["assignments"])
# graph.evolve_test(assignments=config["assignments"], coin_func=get_coin, xjRatio=1, xi=60, output_dir=output_dir)