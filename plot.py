import difflib
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import html
import os
import re
import numpy as np
from scipy.interpolate import griddata


# ##### meta.md作成 ######
# for i in list(range(22,46)) :
#     imgs_dir = f'output_alpha{i}'
#     files = os.listdir(imgs_dir)
#     png_files = sorted([(int(file[:-4].split('_')[-1]), file) for file in os.listdir(imgs_dir) if file[-4:]=='.png'], key=lambda x: x[0])
#     df = pd.DataFrame(png_files, columns=['step', 'image_path'])
#     df["image"] = df["image_path"].map(lambda s: f"![]({s})")
#     df["step"] = df["step"].apply(str).map(lambda s: html.escape(s))

#     table = df.to_markdown(index=False)

#     with open(f"{imgs_dir}/meta.md", "w") as f:
#         f.write(table)

##### カラーバー修正 #####
from src import Network
from src import Observer
import json

params = {
#   "output_alpha25": {"name":"二等辺三角形型（鋭角）", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha26": {"name":"二等辺三角形型（鋭角）", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha27": {"name":"二等辺三角形型（鋭角）", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha28": {"name":"3段テーパ型", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha29": {"name":"3段テーパ型", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha30": {"name":"3段テーパ型", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha31": {"name":"非対称型（左側切欠き）", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha32": {"name":"非対称型（左側切欠き）", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha33": {"name":"非対称型（左側切欠き）", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha34": {"name":"非対称型（右側切欠き）", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha35": {"name":"非対称型（右側切欠き）", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha36": {"name":"非対称型（右側切欠き）", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha37": {"name":"正三角形", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha38": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha39": {"name":"正三角形", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha40": {"name":"二等辺三角形型（鈍角）", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha41": {"name":"二等辺三角形型（鈍角）", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha42": {"name":"二等辺三角形型（鈍角）", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha43": {"name":"長方形", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha44": {"name":"長方形", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha45": {"name":"長方形", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha46": {"name":"二等辺三角形型（鋭角）", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha47": {"name":"二等辺三角形型（鋭角）", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha48": {"name":"二等辺三角形型（鋭角）", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha49": {"name":"二等辺三角形型（鋭角）", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha50": {"name":"3段テーパ型", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha51": {"name":"3段テーパ型", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha52": {"name":"3段テーパ型", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha53": {"name":"3段テーパ型", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha54": {"name":"非対称型（左側切欠き）", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha55": {"name":"非対称型（左側切欠き）", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha56": {"name":"非対称型（左側切欠き）", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha57": {"name":"非対称型（左側切欠き）", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha58": {"name":"非対称型（右側切欠き）", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha59": {"name":"非対称型（右側切欠き）", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha60": {"name":"非対称型（右側切欠き）", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha61": {"name":"非対称型（右側切欠き）", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha62": {"name":"正三角形", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha63": {"name":"正三角形", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha64": {"name":"正三角形", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha65": {"name":"正三角形", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha66": {"name":"二等辺三角形型（鈍角）", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha67": {"name":"二等辺三角形型（鈍角）", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha68": {"name":"二等辺三角形型（鈍角）", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha69": {"name":"二等辺三角形型（鈍角）", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha70": {"name":"長方形", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha71": {"name":"長方形", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha72": {"name":"長方形", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha73": {"name":"長方形", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha74": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 0.1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha75": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha76": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 10, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha77": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 0.001, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha78": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 0.01, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha79": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 100, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha80": {"name":"二等辺三角形型（鋭角・逆向き）", "x/j": 1000, "input":'1,1,1,1,...', "ξ":0},
# #   "output_alpha81": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":0},
# #   "output_alpha82": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":60},
# #   "output_alpha83": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":120},
# #   "output_alpha84": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":180},
# #   "output_alpha85": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":240},
# #   "output_alpha86": {"name":"正三角形", "x/j": 1, "input":'1,1,1,1,...', "ξ":300}
#   "output_alpha87": {"name":"3段テーパ型", "x/j": 0.2, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha88": {"name":"3段テーパ型", "x/j": 0.5, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha89": {"name":"3段テーパ型", "x/j": 2, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha90": {"name":"3段テーパ型", "x/j": 5, "input":'1,1,1,1,...', "ξ":0},
#   "output_alpha91": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":0},
#   "output_alpha92": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_alpha110": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_alpha93": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":120},
#   "output_alpha94": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":180},
#   "output_alpha95": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":240},
#   "output_alpha111": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":270},
#   "output_alpha96": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":300},
#   "output_alpha97": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(1)"},
#   "output_alpha98": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(2)"},
#   "output_alpha99": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(3)"},
#   "output_alpha100": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(4)"},
#   "output_alpha101": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(5)"},
#   "output_alpha102": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(6)"},
#   "output_alpha103": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(7)"},
#   "output_alpha104": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(8)"},
#   "output_alpha105": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(9)"},
#   "output_alpha106": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(10)"},
#   "output_alpha107": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(11)"},
#   "output_alpha108": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(12)"},
#   "output_alpha109": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":"60(check)"},
#   "output_alpha112": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":7.5},
#   "output_alpha113": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":15},
#   "output_alpha114": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":22.5},
#   "output_alpha115": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":30},
#   "output_alpha116": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":37.5},
#   "output_alpha117": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":45},
#   "output_alpha118": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":52.5},
#   "output_alpha119": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_alpha120": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_alpha121": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":75},
#   "output_alpha122": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":82.5},
#   "output_alpha123": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_alpha124": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":97.5},
#   "output_alpha125": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":105},
#   "output_alpha126": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":112.5},
#   "output_alpha127": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":120},
#   "output_alpha128": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":127.5},
#   "output_alpha129": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":135},
#   "output_alpha130": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":142.5},
#   "output_alpha131": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":150},
#   "output_alpha132": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":157.5},
#   "output_alpha133": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":165},
#   "output_alpha134": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":172.5},
#   "output_alpha135": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":180},
#   "output_alpha136": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":187.5},
#   "output_alpha137": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":195},
#   "output_alpha138": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":202.5},
#   "output_alpha139": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":210},
#   "output_alpha140": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":217.5},
#   "output_alpha141": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":225},
#   "output_alpha142": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":232.5},
#   "output_alpha143": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":240},
#   "output_alpha144": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":247.5},
#   "output_alpha145": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":255},
#   "output_alpha146": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":262.5},
#   "output_alpha147": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":270},
#   "output_alpha148": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":277.5},
#   "output_alpha149": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":285},
#   "output_alpha150": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":292.5},
#   "output_alpha151": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":300},
#   "output_alpha152": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":307.5},
#   "output_alpha153": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":315},
#   "output_alpha154": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":322.5},
#   "output_alpha155": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":330},
#   "output_alpha156": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":337.5},
#   "output_alpha157": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":345},
#   "output_alpha158": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":352.5},
#   "output_beta1": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta2": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta3": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta4": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_beta5": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":65},
#   "output_beta6": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67},
#   "output_beta7": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_beta8": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":68},
#   "output_beta9": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":70},
#   "output_beta10": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_beta11": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta12": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta13": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta14": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":60},
#   "output_beta15": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":65},
#   "output_beta16": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_beta17": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":70},
#   "output_beta18": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":90},
#   "output_beta19": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta20": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta21": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta22": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":60},
#   "output_beta23": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":65},
#   "output_beta24": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_beta25": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":70},
#   "output_beta26": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":90},
#   "output_beta27": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta28": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta29": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta30": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":60},
#   "output_beta31": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":65},
#   "output_beta32": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_beta33": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":70},
#   "output_beta34": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":90},
#   "output_beta35": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta36": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta37": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta38": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":60},
#   "output_beta39": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":65},
#   "output_beta40": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_beta41": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":70},
#   "output_beta42": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":90},
#   "output_beta43": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":0},
#   "output_beta44": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":30},
#   "output_beta45": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":45},
#   "output_beta46": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":60},

#   "output_delta1": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":0},
#   "output_delta2": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":7.5},
#   "output_delta3": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":15},
#   "output_delta4": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":22.5},
#   "output_delta5": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":30},
#   "output_delta6": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":37.5},
#   "output_delta7": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":45},
#   "output_delta8": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":52.5},
#   "output_delta9": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_delta10": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67},
#   "output_delta11": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_delta12": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":68},
#   "output_delta13": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":75},
#   "output_delta14": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":82.5},
#   "output_delta15": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_delta16": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":97.5},
#   "output_delta17": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":105},
#   "output_delta18": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":112.5},
#   "output_delta19": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":120},
#   "output_delta20": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":127.5},
#   "output_delta21": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":180},

#   "output_gamma1": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma2": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma3": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma4": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma5": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma6": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma7": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma8": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma9": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma10": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma11": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma12": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma13": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma14": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma15": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma16": {"name":"正三角形", "x/j": 0.2, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma17": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma18": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma19": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma20": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma21": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma22": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma23": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma24": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma25": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma26": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma27": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma28": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma29": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma30": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma31": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma32": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma33": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma34": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma35": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma36": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma37": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma38": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma39": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma40": {"name":"正三角形", "x/j": 2, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma41": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma42": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma43": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma44": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma45": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma46": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma47": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma48": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":90},
#   "output_gamma49": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":0},
#   "output_gamma50": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":15},
#   "output_gamma51": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":30},
#   "output_gamma52": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":45},
#   "output_gamma53": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":60},
#   "output_gamma54": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":67.5},
#   "output_gamma55": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":75},
#   "output_gamma56": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":90},

#   "output_lambda1": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":0},
#   "output_lambda2": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":30},
#   "output_lambda3": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":60},
#   "output_lambda4": {"name":"正三角形", "x/j": 1, "input":'1,0,1,0,...', "ξ":90},
#   "output_lambda5": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":0},
#   "output_lambda6": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":30},
#   "output_lambda7": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":60},
#   "output_lambda8": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":90},
#   "output_lambda9": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":0},
#   "output_lambda10": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":30},
#   "output_lambda11": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":60},
#   "output_lambda12": {"name":"正三角形", "x/j": 10, "input":'1,0,1,0,...', "ξ":90},
#   "output_lambda13": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":0},
#   "output_lambda14": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":30},
#   "output_lambda15": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":60},
#   "output_lambda16": {"name":"正三角形", "x/j": 0.1, "input":'1,0,1,0,...', "ξ":90},
#   "output_lambda17": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":0},
#   "output_lambda18": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":30},
#   "output_lambda19": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":60},
#   "output_lambda20": {"name":"正三角形", "x/j": 0.5, "input":'1,0,1,0,...', "ξ":90},
  "output_lambda21": {"name":"正三角形", "x/j": 5, "input":'1,0,1,0,...', "ξ":120},
}

def get_sources(edge_log_cols, source):
    return [edge_log_col for edge_log_col in edge_log_cols if re.match(f"[0-9]+,[0-9]+->({'|'.join(source)}):[a-z\+\-]*", edge_log_col) is not None]

def get_sinks(edge_log_cols, sink):
    return [edge_log_col for edge_log_col in edge_log_cols if re.match(f"[0-9]+,[0-9]+->({'|'.join(sink)}):[a-z\+\-]*", edge_log_col) is not None]

for dir, param in params.items():

    # config読み込み
    with open(f"{dir}/config.json") as f:
        config = json.load(f)
 
    print([i for i in config["node_thetas"].values()][0].replace("np.arctan(np.sqrt(2)/", "").replace(")", "")==str(param['x/j']), [i for i in config["node_thetas"].values()][0].replace("np.arctan(np.sqrt(2)/", "").replace(")", ""), param['x/j']) 
    print(config["xi"]==str(param['ξ']), config["xi"], param['ξ']) 


sink_probs = []
for dir, param in params.items():

    # config読み込み
    with open(f"{dir}/config.json") as f:
        config = json.load(f)
    # edge_log読み込み
    edge_log = pd.read_csv(f"{dir}/edge_log.csv").applymap(complex)
    # node_log読み込み
    node_log = pd.read_csv(f"{dir}/node_log.csv")
    node_log = node_log.iloc[-1,:]

    # ネットワーク設定
    n = 21
    N = n*(n+1)/2
    peris = [np.pi*np.sqrt(2*N)*i for i in range(1,4)]
    convs = [np.log10(N)*N, np.log(N)*N]
    convs2 = int(np.log(N)*N)//2 * 2

    if n==5:
        target_sink = ["5,5->5,6:v+"]
    elif n==11:
        target_sink = ["11,11->11,12:v+"]
    elif n==21:
        target_sink = ["21,21->21,22:v+"]


    # sinkとsouceの設定
    sources = get_sources(edge_log.columns, source=config['source'])
    sinks = get_sinks(edge_log.columns, sink=config['sink'])

    # output_filenameの指定
    url = f"https://github.com/kyuki-rp/DPQW/blob/main/CalculationResult/{dir}/meta.md"
    output_filename = f"{param['name']}(xjRatio={param['x/j']};Input={param['input']};ξ={param['ξ']})"

    # # sink位置での相対振幅
    # if param['input']=='1,0,1,0,...':
    #     sinks_inedge = edge_log.loc[:,sinks].iloc[-2]
    #     sources_inedge = edge_log.loc[:,sources].iloc[-2]
    # else:
    #     sinks_inedge = edge_log.loc[:,sinks].iloc[-1]
    #     sources_inedge = edge_log.loc[:,sources].iloc[-1]
        
    sinks_inedge = edge_log.loc[:,sinks].iloc[-2:]
    sources_inedge = edge_log.loc[:,sources].iloc[-2:]

    sinks_prob = sinks_inedge.values * sinks_inedge.values.conjugate()
    sources_prob = sources_inedge.values * sources_inedge.values.conjugate()
    recent_range = 300
    # sink_recent_max_prob_sum = (edge_log.loc[:,sinks].iloc[-recent_range:].values * edge_log.loc[:,sinks].iloc[-recent_range:].values.conjugate()).sum(axis=1).max()
    sink_recent_max_prob_sum = (edge_log.loc[:,target_sink].iloc[-recent_range:].values * edge_log.loc[:,target_sink].iloc[-recent_range:].values.conjugate()).sum(axis=1).max()
    sink_probs.append([param['name'], param['x/j'], param['ξ'], param['input'], sinks_prob.sum().real, sources_prob.sum().real, sinks_prob.sum().real+sources_prob.sum().real, sink_recent_max_prob_sum.real, url])

    # graph設定
    graph = Network()
    graph.custom(node_identifiers=config['node_identifiers'],
                sink=config['sink'],
                source=config['source'],
                source_cycles=config['source_cycles'],
                node_thetas=config['node_thetas']
                )

    # overwrite
    for node in graph.nodes:
        node.data_update(key='state',val=node_log[f"{node.identifier}"])

    # 出力
    ovserver = Observer(graph)
    ovserver.gv_plot(f"{output_filename}_graph.png")

    ### sinkでの時間発展
    if param['input']=='1,0,1,0,...':
        edge_log_ = edge_log[edge_log.reset_index()['index'].apply(lambda x: x%2)==0].copy()
    else:
        edge_log_ = edge_log.copy()
    edge_log_['sink'] = (edge_log_[target_sink].values*edge_log_[target_sink].values.conjugate()).sum(axis=1) / n
    x_max = edge_log_['sink'].max()
    plt.plot(edge_log_.index, edge_log_['sink'], label='sink')

    plt.xlabel('Step', fontsize=18)
    plt.xticks(fontsize=18, rotation=0)
    plt.ylabel('Probability', fontsize=18)
    plt.yticks(fontsize=18)
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=15)
    plt.axvspan(10000-recent_range,10000,alpha=1.0,color="#ffcdd2")
    plt.savefig(f"output/{output_filename}_evolve.png", bbox_inches="tight")
    plt.close(None)
    plt.clf()


    # 初期ステップのみ
    plt.plot(edge_log_.index[:convs2], edge_log_['sink'].iloc[:convs2], label='sink')

    for peri in peris:
        plt.vlines(peri,0,x_max, color="red", linestyles='dotted')

    for conv in convs:
        plt.vlines(conv,0,x_max, color="green", linestyles='dotted')

    plt.xlabel('Step', fontsize=18)
    plt.xticks(fontsize=18, rotation=0)
    plt.ylabel('Probability', fontsize=18)
    plt.yticks(fontsize=18)
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=15)
    plt.savefig(f"output/{output_filename}_evolve(初期ステップ).png", bbox_inches="tight")
    plt.close(None)
    plt.clf()

df = pd.DataFrame(sink_probs, columns=["name", "x/j", "ξ", "input", "sink_prob", "sources_prob_sum", "sink_prob + sources_prob_sum", "sink_recent_max_prob", "url"])
df.to_csv("output/sink_recent_max_probs.csv", index=False, encoding='utf_8_sig')

calam_dif = pd.DataFrame([['name','グラフ型名'],['x/j','x/jの値'],['ξ','ξの値'],['input','入力時系列'],['sink_prob','sinkへの流入の相対確率（エッジの2乗）'],['sources_prob_sum','sourcesへの流入の相対確率（エッジの2乗の和）'],['sink_prob + sources_prob_sum','「sink_prob」と「sources_prob_sum」の和'],['sink_recent_max_prob','sinkへの流入の相対確率の直近最大値（エッジの2乗）'],['url','github上にアップロードしたデータのurl']], columns=['列名', '説明'])
calam_dif.to_csv("output/カラム定義.csv", index=False, encoding='utf_8_sig')

sink_probs = pd.read_csv('output/sink_recent_max_probs.csv')
sink_probs = sink_probs.sort_values(["name", "x/j", "ξ"])

plt.figure(figsize=(10,4))
for name in sink_probs['name'].drop_duplicates():
    df = sink_probs[sink_probs['name']==name]



# 3D plot
sink_probs = pd.read_csv('output/sink_recent_max_probs.csv')
sink_probs = sink_probs.sort_values(["name", "x/j", "ξ"])
x, y, z = sink_probs["ξ"], sink_probs["x/j"], sink_probs["sink_recent_max_prob"]/n
xi = np.linspace(min(x), max(x),100)
yi = np.linspace(min(y), max(y),100)
grid_x, grid_y = np.meshgrid(xi, yi)
xy = np.array([[X,Y] for X,Y in zip(x,y)])
Z = griddata(xy, z, (grid_x, grid_y),method="nearest")

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# ax.plot_surface(grid_x, grid_y, Z, cmap = "winter")
ax.scatter(x, np.log(y)/np.log(10), z)
ax.set_xlabel("ξ")
ax.set_ylabel("log(x/j)")
ax.set_zlabel("sink_recent_max_prob")
plt.savefig(f"output/sink_recent_max_probs.png", bbox_inches="tight")
plt.close(None)
plt.clf()

# 2D plot
fig, ax1 = plt.subplots()
ax1.tricontour(x, y, z, 14, linewidths=0.5, linestyles='dotted', colors='black')
ax1.set_xlabel("ξ")
ax1.set_ylabel("x/j")
ax1.set_yscale('log')
cntr = ax1.tricontourf(x, y, z, 14, cmap='RdBu_r')
fig.colorbar(cntr, ax=ax1)
ax1.plot(x,y,'ko',ms=3)   # marker='ko' (kuro, circle), markersize=3
plt.savefig(f"output/sink_recent_max_probs_contour.png", bbox_inches="tight")
plt.close(None)
plt.clf()


# # # χ/J
# #     plt.plot(df['x/j'], df['sink_recent_max_prob'], marker='o', label=name)
# # plt.xlabel('χ/J', fontsize=18)
# # plt.xticks(fontsize=18, rotation=0)
# # plt.xscale('log')

# # ξ
#     plt.plot(df['ξ'], df['sink_recent_max_prob'], marker='o', label=name)

# plt.grid(linestyle='dotted')
# plt.xlabel('ξ', fontsize=18)
# plt.xticks(np.arange(0, 360 + 1, 30), fontsize=18, rotation=0)
# plt.ylabel('Probability', fontsize=18)
# plt.yticks(fontsize=18)
# plt.yscale('log')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=15)
# plt.savefig(f"output/sink_recent_max_probs.png", bbox_inches="tight")
# plt.close(None)
# plt.clf()


# sink_probs = pd.read_csv("output(8')/sink_recent_max_probs.csv")
# sink_probs = sink_probs[sink_probs['x/j']==1][['name','sink_prob']].set_index("name")
# sink_probs = sink_probs.loc[['二等辺三角形型（鋭角）','3段テーパ型', '非対称型（左側切欠き）','非対称型（右側切欠き）']]
# sink_probs.plot(linestyle='None', marker='o')
# plt.xlabel('グラフ型', fontsize=18)
# plt.xticks(fontsize=18, rotation=90)
# plt.ylabel('Probability', fontsize=18)
# plt.yticks(fontsize=18)
# plt.ylim(10**(-12),10**(-9))
# plt.yscale('log')
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=15)
# plt.savefig(f"sink_recent_max_probs.png", bbox_inches="tight")
# plt.close(None)
# plt.clf()


# for y in ['-2,2','-1,2','0,2','1,2','2,2']:
    # plt.scatter(x=df['index'], y=df[y], s=1, label=y)
# df[['-2,2','-1,2','0,2','1,2','2,2']].plot()
# plt.xlim([0.00000000001,1])

# plt.xlabel('step',size=12)
# plt.ylabel('probability',size=12)
# plt.legend()



# for i, coordinate in enumerate(['2,-2', '2,0', '2,2', '0,-2', '0,0', '0,2', '-2,-2', '-2,0', '-2,2']):
#     plt.subplot(3, 3, i+1)

#     plt.plot(df[coordinate])
#     plt.ylim([0.00000000000001,10])
#     plt.yscale("log")

#     plt.title(f'(x, y) = ({coordinate})', fontsize=8)
#     plt.tick_params(labelsize=5)
#     plt.xlabel('step',size=8)
#     plt.ylabel('probability',size=8)

# plt.subplots_adjust(wspace=0.2, hspace=0.3)
# plt.show()

# print(df.iloc[-1,:]['2,2'])


# df = pd.DataFrame({'theta':[1/12, 1/6, 1/3, 1/2, 2/3, 5/6, 11/12, 1],'val':[6.51*10**(-7), 3.19*10**(-7), 3.74*10**(-8),1.34*10**(-71),
#               3.74*10**(-8), 3.19*10**(-7), 6.51*10**(-7), 8.95*10**(-7)
# ]})

# plt.scatter(df['theta'], df['val'])
# plt.ylim([0.00000000000001,10])
# plt.xlim([0,1])
# plt.xlabel('θ',size=8)
# plt.ylabel('probability',size=8)
# plt.tick_params(labelsize=5)
# plt.yscale("log")
# plt.show()