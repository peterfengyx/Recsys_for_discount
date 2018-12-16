import pickle

import numpy as np, random
import matplotlib.pyplot as plt


def draw_histogram(labels, values, values_2, x_labels, y_labels, file_name, baseline):
    indexes = np.arange(len(labels))

    width = 0.27
    color_arr = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(1, 2 * len(labels) + 1):
        color_arr.append('#' + "%06x" % random.randint(0, 0xFFFFFF)) # generate random colurs for each bar

    # plt.bar(indexes, values, width, color=color_arr[:len(labels)])
    # plt.bar(indexes + width, baseline, width, color=color_arr[len(labels):])

    a = plt.bar(indexes + width, values, width, color='r')
    b = plt.bar(indexes + width * 2, values_2, width, color='g')
    c = plt.bar(indexes, baseline, width, color='b')

    plt.gca().legend(loc='upper left')
    ax.legend((a[0], b[0], c[0]), ('With Trust(global)', 'With Trust(category)', 'Without Trust'))
    plt.xticks(indexes + width, labels)
    plt.xlabel(x_labels, fontsize=18)
    plt.ylabel(y_labels, fontsize=18)
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.title("Quantity vs Profit", fontsize=16)
    plt.show()
    fig.savefig(file_name, bbox_inches='tight')
# quantity 200, global trust vary from 4, 5, 6, 7


def create_graph():
    loader_obj = pickle.load(open("../feature/data_loader.p", "rb"))
    quants = [100, 200, 300, 400]
    profit_trust_global_all = []
    trust_all = []
    profit_only_all = []
    profit_trust_cat_all = []
    for quan in quants:
        ds = pickle.load(open("../feature/profit_feature_1_" + str(quan) + "_0.5_0.1.p", "rb"))
        ob = pickle.load(open("../feature/algo_output_1_" + str(quan) + "_0.5_0.1_4.p", "rb"))


        print(len(ob['trust_global']))
        print(ob['trust_global'][0])
        print(ob['profit_only'][0])

        profit_trust_global = 0
        profit_only = 0
        profit_trust_category = 0
        # for i in range(len(ob['trust_global'])):
        #     for j, val in enumerate(ob['trust_global'][i]):
        #         profit_trust_global += ds['profit_predict'][i][val]
        # profit_trust_global_all.append(profit_trust_global/10000)
        #
        # for i in range(len(ob['trust_category'])):
        #     for j, val in enumerate(ob['trust_category'][i]):
        #         profit_trust_category += ds['profit_predict'][i][val]
        # profit_trust_cat_all.append(profit_trust_category/10000)

        for i in range(len(ob['profit_only'])):
            for j, val in enumerate(ob['profit_only'][i]):
                profit_only += ds['profit_predict'][i][val]
        profit_only_all.append(profit_only/10000)
        print("all vals ", quan, profit_trust_global, profit_only)
        trust_all.append(ob['global_trust_kept'])
        # print("global trus ", profit_trust_global)
        # print("profit only ", profit_only)
        # print("kept trust for ", ob['global_trust_kept'])
    print(quants)
    print(profit_trust_global_all)

    print(profit_trust_cat_all)
    print(" profit only all ", profit_only_all)

    # draw_histogram(quants, profit_trust_global_all, profit_trust_cat_all, 'Quantity', 'Average Profit($)', "profit_all_4.pdf", profit_only_all)
    # draw_histogram(quants, trust_all, 'Quantity', 'Trust Kept')


create_graph()
# draw_histogram([100, 200, 300, 400], [2000, 3000, 4000, 5000],'Quantity', 'Average Profit', [3000, 4000, 5000, 6000])