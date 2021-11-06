import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import html
import os

# ##### meta.md作成 ######
# for i in list(range(20,28)) :
#     imgs_dir = f'output_add{i}'
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
  "output10": {"name":"11x5", "x/j": 0.001, "input":'1010'},
  "output11": {"name":"11x5", "x/j": 0.01, "input":'1010'},
  "output_add20": {"name":"11x5", "x/j": 0.02, "input":'1010'},
  "output_add21": {"name":"11x5", "x/j": 0.05, "input":'1010'},
  "output12": {"name":"11x5", "x/j": 0.1, "input":'1010'},
  "output13": {"name":"11x5", "x/j": 0.2, "input":'1010'},
  "output14": {"name":"11x5", "x/j": 0.5, "input":'1010'},
  "output15": {"name":"11x5", "x/j": 1, "input":'1010'},
  "output16": {"name":"11x5", "x/j": 2, "input":'1010'},
  "output17": {"name":"11x5", "x/j": 5, "input":'1010'},
  "output18": {"name":"11x5", "x/j": 10, "input":'1010'},
  "output_add22": {"name":"11x5", "x/j": 20, "input":'1010'},
  "output_add23": {"name":"11x5", "x/j": 50, "input":'1010'},
  "output19": {"name":"11x5", "x/j": 100, "input":'1010'},
  "output20": {"name":"11x5", "x/j": 1000, "input":'1010'},
  "output32": {"name":"三角格子", "x/j": 0.001, "input":'1010'},
  "output33": {"name":"三角格子", "x/j": 0.01, "input":'1010'},
  "output_add24": {"name":"三角格子", "x/j": 0.02, "input":'1010'},
  "output_add25": {"name":"三角格子", "x/j": 0.05, "input":'1010'},
  "output34": {"name":"三角格子", "x/j": 0.1, "input":'1010'},
  "output35": {"name":"三角格子", "x/j": 0.2, "input":'1010'},
  "output36": {"name":"三角格子", "x/j": 0.5, "input":'1010'},
  "output37": {"name":"三角格子", "x/j": 1, "input":'1010'},
  "output38": {"name":"三角格子", "x/j": 2, "input":'1010'},
  "output39": {"name":"三角格子", "x/j": 5, "input":'1010'},
  "output40": {"name":"三角格子", "x/j": 10, "input":'1010'},
  "output_add26": {"name":"三角格子", "x/j": 20, "input":'1010'},
  "output_add27": {"name":"三角格子", "x/j": 50, "input":'1010'},
  "output42": {"name":"三角格子", "x/j": 100, "input":'1010'},
  "output43": {"name":"三角格子", "x/j": 1000, "input":'1010'},
  "output_add1": {"name":"中間型1", "x/j": 0.1, "input":'1010'},
  "output_add2": {"name":"中間型1", "x/j": 1, "input":'1010'},
  "output_add3": {"name":"中間型1", "x/j": 10, "input":'1010'},
  "output_add4": {"name":"中間型2", "x/j": 0.1, "input":'1010'},
  "output_add5": {"name":"中間型2", "x/j": 1, "input":'1010'},
  "output_add6": {"name":"中間型2", "x/j": 10, "input":'1010'},
  "output_add7": {"name":"直角三角形", "x/j": 0.1, "input":'1010'},
  "output_add8": {"name":"直角三角形", "x/j": 1, "input":'1010'},
  "output_add9": {"name":"直角三角形", "x/j": 10, "input":'1010'},
  "output_add10": {"name":"11x5", "x/j": 0.1, "input":'0101'},
  "output_add11": {"name":"11x5", "x/j": 0.1, "input":'1111'},
  "output_add12": {"name":"三角格子", "x/j": 0.1, "input":'0101'},
  "output_add13": {"name":"三角格子", "x/j": 0.1, "input":'1111'},
  "output_add14": {"name":"中間型1", "x/j": 0.1, "input":'0101'},
  "output_add15": {"name":"中間型1", "x/j": 0.1, "input":'1111'},
  "output_add16": {"name":"中間型2", "x/j": 0.1, "input":'0101'},
  "output_add17": {"name":"中間型2", "x/j": 0.1, "input":'1111'},
  "output_add18": {"name":"直角三角形", "x/j": 0.1, "input":'0101'},
  "output_add19": {"name":"直角三角形", "x/j": 0.1, "input":'1111'}
}

sink_position = {
  "11x5":"5,5->5,6",
  "三角格子":"5,5->5,6",
  "中間型1":"5,3->5,4",
  "中間型2":"5,4->5,5",
  "直角三角形":"0,5->0,6",
}

sink_probs = []
for dir, param in params.items():

    # config読み込み
    with open(f"{dir}/config.json") as f:
        config = json.load(f)
    # edge_log読み込み
    edge_log = pd.read_csv(f"{dir}/edge_log.csv")
    # node_log読み込み
    node_log = pd.read_csv(f"{dir}/node_log.csv")
    node_log = node_log.iloc[-1,:]

    # output_filenameの指定
    url = f"https://github.com/kyuki-rp/DPQW/blob/main/CalculationResult/{dir}/meta.md"
    output_filename = f"{param['name']}(xjRatio={param['x/j']};Input={param['input']})"

    # sinkでの相対振幅
    if param['input']=='1010':
        sink_inedge = edge_log.loc[:,sink_position[param['name']]].iloc[-2]
    else:
        sink_inedge = edge_log.loc[:,sink_position[param['name']]].iloc[-1]
    sink_prob = sink_inedge*sink_inedge
    sink_probs.append([param['name'], param['x/j'], param['input'], sink_inedge, sink_prob, url])
  
    # # sink付近のノード分布
    # df = pd.read_csv(f"{dir}/node_log.csv")
    # df = df.iloc[-1,:].loc[["0,5","1,5","2,5","3,5","4,5","5,5","6,5","7,5","8,5","9,5","10,5"]]
    # df.reset_index().rename(columns={'index':'Node',9999:'Value'}).to_csv(f"output/{output_filename}_values.csv", index=False)
    # df.plot.bar()
    # plt.xlabel('Node', fontsize=18)
    # plt.xticks(fontsize=18, rotation=0)
    # plt.ylabel('Value', fontsize=18)
    # plt.yticks(fontsize=18)
    # plt.ylim(0,6)
    # plt.savefig(f"output/{output_filename}_bar.png", bbox_inches="tight")
    # plt.close(None)
    # plt.clf()

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
    edge_log_ = edge_log[edge_log.reset_index()['index'].apply(lambda x: x%2)==0]
    sink_inedge_col = ''.join([col for col in edge_log_.columns if sink_position[param['name']]in col])
    (edge_log_[sink_inedge_col]**2).plot()
    plt.xlabel('Step', fontsize=18)
    plt.xticks(fontsize=18, rotation=0)
    plt.ylabel('Probability', fontsize=18)
    plt.yticks(fontsize=18)
    plt.yscale('log')
    plt.savefig(f"output/{output_filename}_evolve.png", bbox_inches="tight")
    plt.close(None)
    plt.clf()

df = pd.DataFrame(sink_probs, columns=["name", "x/j", "input", "sink_inedge", "sink_prob", "url"])
df['input'] = df['input'].apply(lambda x: f"{x[0]},{x[1]},{x[2]},{x[3]}, ...")
df.to_csv("output/sink_probs.csv", index=False, encoding='utf_8_sig')

calam_dif = pd.DataFrame([['name','グラフ型名'],['x/j','x/jの値'],['input','入力時系列'],['sink_inedge','sinkへの入力エッジの値'],['sink_prob','sinkの相対確率'],['url','github上にアップロードしたデータのurl']], columns=['列名', '説明'])
calam_dif.to_csv("output/カラム定義.csv", index=False, encoding='utf_8_sig')

sink_probs = pd.read_csv('output/sink_probs.csv')
for name in sink_probs['name'].drop_duplicates():
    df = sink_probs[(sink_probs['input']=='1,0,1,0, ...') & (sink_probs['name']==name)]
    plt.plot(df['x/j'], df['sink_prob'], marker='o', label=name)
plt.xlabel('χ/J', fontsize=18)
plt.xticks(fontsize=18, rotation=0)
plt.xscale('log')
plt.ylabel('Probability', fontsize=18)
plt.yticks(fontsize=18)
plt.yscale('log')
plt.legend()
plt.savefig(f"output/sink_probs.png", bbox_inches="tight")
plt.close(None)
plt.clf()



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