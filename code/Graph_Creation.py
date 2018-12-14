import pickle

import numpy as np, random
import matplotlib.pyplot as plt





def draw_histogram(labels, values, x_labels, y_labels):
    indexes = np.arange(len(labels))
    width = 0.7
    color_arr = []
    for i in range(1, len(labels) + 1):
        color_arr.append('#' + "%06x" % random.randint(0, 0xFFFFFF)) # generate random colurs for each bar
    plt.bar(indexes, values, width, color=color_arr)
    plt.xticks(indexes, labels)
    plt.xlabel(x_labels, fontsize=18)
    plt.ylabel(y_labels, fontsize=18)
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.show()

# quantity 200, global trust vary from 4, 5, 6, 7





def create_graph():
    loader_obj = pickle.load(open("../feature/data_loader.p", "rb"))
    ds = pickle.load(open("../feature/profit_feature_1_200_0.5_0.1.p", "rb"))
    ob = pickle.load(open("../feature/algo_output_1_200_0.5_0.1_4.p", "rb"))

    print(len(ob['trust_global']))
    print(ob['trust_global'][0])
    print(ob['profit_only'][0])

    profit_trust_global = 0
    profit_only = 0
    for i in range(len(ob['trust_global'])):
        for j, val in enumerate(ob['trust_global'][i]):
            profit_trust_global += ds['profit_predict'][i][val]

    for i in range(len(ob['profit_only'])):
        for j, val in enumerate(ob['profit_only'][i]):
            profit_only += ds['profit_predict'][i][val]

    print("global trus ", profit_trust_global)
    print("profit only ", profit_only)
    print("kept trust for ", ob['global_trust_kept'])


# draw_histogram(['hello', 'world'], [10, 20], 'Quantity', 'Profit')
create_graph()
