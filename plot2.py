import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import html
import os
import re
import numpy as np


##### カラーバー修正 #####
from src import Network
from src import Observer
import json

params = {
  "output_alpha97": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(1)"},
  "output_alpha98": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(2)"},
  "output_alpha99": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(3)"},
  "output_alpha100": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(4)"},
  "output_alpha101": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(5)"},
  "output_alpha102": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(6)"},
  "output_alpha103": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(7)"},
  "output_alpha104": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(8)"},
  "output_alpha105": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(9)"},
  "output_alpha106": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(10)"},
  "output_alpha107": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(11)"},
  "output_alpha108": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(12)"},
}

md = pd.DataFrame([])
for dir, param in params.items():

    # config読み込み
    with open(f"{dir}/config.json") as f:
        config = json.load(f)
    # edge_log読み込み
    edge_log = pd.read_csv(f"{dir}/edge_log.csv").applymap(complex)
    # node_log読み込み
    node_log = pd.read_csv(f"{dir}/node_log.csv")
    node_log = node_log.iloc[-1,:]

    ms = edge_log[[
                    "1,11->1,10:v-",
                    "2,10->2,9:v-",
                    "3,9->3,8:v-",
                    "4,8->4,7:v-",
                    "5,7->5,6:v-",
                    "6,6->6,5:v-",
                    "7,5->7,4:v-",
                    "8,4->8,3:v-",
                    "9,3->9,2:v-",
                    "10,2->10,1:v-",
                    "11,1->11,0:v-",
                    "11,11->11,12:v+",
                    ]].iloc[-2]

    ms.name = param["ξ"]
    md = md.append(ms)
    md = md[[      "1,11->1,10:v-",
                    "2,10->2,9:v-",
                    "3,9->3,8:v-",
                    "4,8->4,7:v-",
                    "5,7->5,6:v-",
                    "6,6->6,5:v-",
                    "7,5->7,4:v-",
                    "8,4->8,3:v-",
                    "9,3->9,2:v-",
                    "10,2->10,1:v-",
                    "11,1->11,0:v-",
                    "11,11->11,12:v+",
                    ]]


md.to_csv("md.csv")

md_re = np.round(np.real(md), decimals=3)
md_im = np.round(np.imag(md), decimals=3)
pd.DataFrame(md_re).to_csv("md_re.csv", index=False)
pd.DataFrame(md_im).to_csv("md_im.csv", index=False)

mde = np.dot(md.values.T, md.values.conjugate())

pd.DataFrame(np.real(mde)).to_csv("mde_re.csv", index=False)
pd.DataFrame(np.imag(mde)).to_csv("mde_im.csv", index=False)

np.dot(md.values.conjugate(), np.array([0,0,0,0,0,0,0,0,0,0,0,np.sqrt(11)]))
# array([ 8.58531477e-03-3.29566303e-02j,  4.83283828e-03-4.25398193e-02j,
    #    -2.05798612e-02-5.14167387e-02j,  1.61272310e-01-1.56148659e-01j,
    #     3.68658870e-01-2.24391984e-01j,  4.31892261e-01-2.38452176e-01j,
    #     3.49975509e-01-2.30584216e-01j,  1.02318257e-01-1.26630714e-01j,
    #     1.26617991e-02-5.74268415e-02j,  1.66637997e-02-6.29272372e-02j,
    #     1.38105077e-19-1.37939489e-18j, -2.31323250e+00-2.22549436e+00j])

array([-0.72502818+0.64528106j, -1.03444347+1.67834216j,
       -0.1619965 +1.06707529j, -1.13830916+1.51172292j,
       -0.56535244+0.8450509j , -1.24093599+1.62723045j,
       -0.51729521+0.77064563j, -0.9581417 +1.6376001j ,
       -0.18765492+1.08296886j, -1.30737185+1.44667347j,
       -0.5       +0.8660254j ,  0.64923249+0.55784834j])