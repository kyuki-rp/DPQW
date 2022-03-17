import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import numpy as np
from scipy.interpolate import griddata
import json


# ディレクトリ指定
dir = 'output(21;sink)'

# ファイル名取得
files = os.listdir(f'../{dir}')
edge_log_files = [file for file in files if 'edge_log' in file]

# config読み込み
with open(f"../{dir}/config.json") as f:
    config = json.load(f)

# 関数定義
def get_outflow_edges(edge_log_col, assignments):
    exclude_reflect_assignments_keys = [key for key, val in assignments.items() if "reflect" != val[0]]
    inverted_assignments_keys = [f"{assignment_key.split('->')[1]}->{assignment_key.split('->')[0]}" for assignment_key in exclude_reflect_assignments_keys]
    return [col for col in edge_log.columns if col.split(':')[0] in inverted_assignments_keys]

def get_input(assignments):
    exclude_reflect_assignments_vals = [val for key, val in assignments.items() if "reflect" != val[0]]
    return np.array(exclude_reflect_assignments_vals).sum()

# ネットワーク設定
input_n = get_input(assignments=config['assignments'])

if input_n==5:
    target_sink = ["5,5->5,6:v+"]
elif input_n==11:
    target_sink = ["11,11->11,12:v+"]
elif input_n==21:
    target_sink = ["21,21->21,22:v+"]


probs = []
for edge_log_file in edge_log_files:

    # Read xjRatio and xi
    m = re.match(r'.*xjRatio=([0-9.]*);xi=([0-9.]*).*', edge_log_file)
    xjRatio = float(m.group(1))
    xi = float(m.group(2))

    # Load edge_log file
    edge_log = pd.read_csv(f'../{dir}/{edge_log_file}').applymap(complex)
    convergence_step = edge_log['Unnamed: 0'].iloc[-1].real
   
    # Calculate outflow_prob
    outflow_edge_cols = get_outflow_edges(edge_log_col=edge_log.columns, assignments=config['assignments'])
    outflow_edges = edge_log[outflow_edge_cols].iloc[-1]
    outflow_prob = (outflow_edges.values * outflow_edges.values.conjugate()).sum().real

    target_sink_edges = edge_log[target_sink].iloc[-1]
    target_sink_prob = (target_sink_edges.values * target_sink_edges.values.conjugate()).sum().real
    normalized_target_sink_prob = target_sink_prob / input_n

    # Append df
    probs.append(['正三角形', input_n, convergence_step, xjRatio, xi, outflow_prob, target_sink_prob, normalized_target_sink_prob])

# Create DF
probs_df = pd.DataFrame(probs, columns=["名前", "入力ノード数", "収束ステップ数", "x/j", "ξ", "流出の相対確率（エッジの2乗）の和", "ターゲット位置への流出の相対確率（エッジの2乗）", "規格化したターゲット位置への流出の相対確率（エッジの2乗）"])
probs_df = probs_df.sort_values(["名前", "x/j", "ξ"])
probs_df.to_csv(f"../{dir}/prob.csv", index=False, encoding='utf_8_sig')

# 3D plot
x, y, z = probs_df["ξ"], probs_df["x/j"], probs_df["規格化したターゲット位置への流出の相対確率（エッジの2乗）"]
xi = np.linspace(min(x), max(x), 100)
yi = np.linspace(min(y), max(y), 100)
grid_x, grid_y = np.meshgrid(xi, yi)
xy = np.array([[X,Y] for X,Y in zip(x,y)])
Z = griddata(xy, z, (grid_x, grid_y),method="nearest")

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# ax.plot_surface(grid_x, grid_y, Z, cmap = "winter")
ax.scatter(x, np.log(y)/np.log(10), z)
ax.set_xlabel("ξ")
ax.set_ylabel("log(x/j)")
ax.set_zlabel("normalized_target_sink_prob")
plt.savefig(f"../{dir}/sink_probs_3D.png", bbox_inches="tight")
plt.close(None)
plt.clf()

# 2D contour plot
fig, ax1 = plt.subplots()
ax1.tricontour(x, y, z, 14, linewidths=0.5, linestyles='dotted', colors='black')
ax1.set_xlabel("ξ")
ax1.set_ylabel("x/j")
ax1.set_yscale('log')
cntr = ax1.tricontourf(x, y, z, 14, cmap='RdBu_r')
fig.colorbar(cntr, ax=ax1)
ax1.plot(x,y,'ko',ms=3)   # marker='ko' (kuro, circle), markersize=3
plt.savefig(f"../{dir}/sink_probs_contour.png", bbox_inches="tight")
plt.close(None)
plt.clf()

# 2D cross-section plot
for xjRatio in [1,5]:
    df = probs_df[probs_df["x/j"]==xjRatio]
    # df = df[df["ξ"].isin([0,7,8,15,22,23,30,37,38,45,52,53,60,67,68,75,82,83])]

    x, y = df["ξ"], df["規格化したターゲット位置への流出の相対確率（エッジの2乗）"]
    plt.plot(x, y, label=f"x/j={xjRatio}", marker='o')
    plt.yscale('log')
    plt.legend()
    plt.savefig(f"../{dir}/sink_probs_cross_section(xjRatio={xjRatio}).png", bbox_inches="tight")
    plt.close(None)
    plt.clf()
