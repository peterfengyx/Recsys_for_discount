import pickle, copy
from code.DataLoader import create_output
import numpy as np


loader_obj = None
quantity = {}
inv_cost = {}
profit_predict = []
ranking_profit = []
REC_ITEM = 10
global_threshold = 4 # 4 from vanilla must be in the profit RS
rec_items_vanilla = []
rec_item_only_profit = []
rec_item_cat_thres = []
rec_item_cat_glob = []


def create_recommendation_vanilla():
    global loader_obj, rec_items_vanilla
    for i in range(len(loader_obj.ranking)):
        ranking = loader_obj.ranking[i]
        rec_item = []
        x = sorted(ranking)
        for j in range(REC_ITEM):

            product_id = list(ranking).index(j+1)  # j starts with 0, we want 1...10
            rec_item.append(product_id)
        rec_items_vanilla.append(rec_item)

    print("rec items vanilla ", i)
    return


def create_recommendation_only_profit():
    global ranking_profit, profit_predict, rec_item_only_profit, quantity
    quan_copy = copy.deepcopy(quantity)

    for i in range(len(ranking_profit)):

        top = 1
        rec_prod = []
        profit = 0
        while len(rec_prod) < REC_ITEM:
            top_index = list(ranking_profit[i]).index(top)
            if quan_copy[top_index] > 0:
                rec_prod.append(top_index)
                profit += profit_predict[i][top_index]
                quan_copy[top_index] -= 1
            top += 1

        # print("user ", i)
        # print("rec product ", rec_prod)
        # print("profit ", profit)
        rec_item_only_profit.append(rec_prod)
        print("rec items only profit ", i)
    return


def within_category_threshold(user_id, product_id):
    cat_len = -1
    for key in loader_obj.new_price_dict:
        obj = loader_obj.new_price_dict[key]
        if product_id in obj:
            cat_len = len(loader_obj.new_price_dict[key])
            break
    threshold = cat_len / 2 # threshold initialized as half of total number of items in a category
    user_ranked = loader_obj.ranking[user_id][product_id]  # get user ranking from vanilla RS
    #print("user id , product id , threshold , user ranked ", user_id, product_id, threshold, user_ranked)
    if user_ranked < threshold:
        return True
    return False


def create_recommendation_cat_threshold():

    global profit_predict, ranking_profit, quantity, rec_item_cat_thres
    quan_copy = copy.deepcopy(quantity)

    for i in range(len(ranking_profit)):
        top = 1
        rec_prod = []
        profit = 0
        while len(rec_prod) < REC_ITEM and top <= len(ranking_profit[i]):
            top_index = list(ranking_profit[i]).index(top)   # this is the product id
            if within_category_threshold(i, top_index) and quan_copy[top_index] > 0:
                rec_prod.append(top_index)
                profit += profit_predict[i][top_index]
                quan_copy[top_index] -= 1  # decrement quantity
            top += 1
        rec_item_cat_thres.append(rec_prod)
        print("rec item cat thres ", i)
    return


def create_recommendation_global_threshold():
    global profit_predict, ranking_profit, quantity, loader_obj, rec_items_vanilla, rec_item_cat_glob
    quan_copy = copy.deepcopy(quantity)

    for i in range(len(ranking_profit)):
        top = 1
        rec_prod = []
        profit = 0
        rec_van = rec_items_vanilla[i]
        ob_prod_prof = []
        for j in range(len(rec_van)):
            ob = {
                'id': rec_van[j],
                'prof': profit_predict[i][rec_van[j]]
            }
            ob_prod_prof.append(ob)
        sorted_ob_prod_prof = sorted(ob_prod_prof, key=lambda x: x['prof'], reverse=True)

        for j in range(len(sorted_ob_prod_prof)):
            if len(rec_prod) == global_threshold:
                break
            if quan_copy[sorted_ob_prod_prof[j]['id']] > 0:
                rec_prod.append(sorted_ob_prod_prof[j]['id'])
                profit += sorted_ob_prod_prof[j]['prof']
                quan_copy[sorted_ob_prod_prof[j]['id']] -= 1

        while len(rec_prod) < REC_ITEM and top <= len(ranking_profit[i]):
            product_id = list(ranking_profit[i]).index(top)
            if quan_copy[product_id] > 0 and product_id not in rec_prod:
                rec_prod.append(product_id)
                profit += profit_predict[i][product_id]
                quan_copy[product_id] -= 1
            top += 1
        rec_item_cat_glob.append(rec_prod)
        print("rect item cat glob ", i)
    return


def create():
    global quantity, inv_cost, profit_predict, ranking_profit, loader_obj
    # loader_obj = create_output()
    # van_ranking = []
    # print("old ranking ", sorted(loader_obj.ranking[0]))
    # for i in range(len(loader_obj.ratings_predict)):
    #     rating = list(loader_obj.ratings_predict[i])
    #     ranking_ind = np.zeros(len(rating))
    #
    #     rank = 1
    #     while rank <= len(rating):
    #         index = list(rating).index(max(rating))
    #         ranking_ind[index] = rank
    #         rank += 1
    #         rating[index] = -1
    #     van_ranking.append(ranking_ind)
    #     print("van ranking for user ", i)
    # loader_obj.ranking = van_ranking   # previous van ranking was wrong
    # pickle.dump(loader_obj, open("../feature/data_loader.p", "wb"))
    loader_obj = pickle.load(open("../feature/data_loader.p", "rb"))
    ob = pickle.load(open("../feature/profit_feature.p", "rb"))
    quantity = ob['quantity']
    inv_cost = ob['inv_cost']
    profit_predict = ob['profit_predict']
    ranking_profit = ob['profit_ranking']
    return


def save_file():
    global rec_items_vanilla, rec_item_only_profit, rec_item_cat_glob, rec_item_cat_thres
    ob = {
        'vanilla': rec_items_vanilla,
        'profit_only': rec_item_only_profit,
        'trust_category': rec_item_cat_thres,
        'trust_global': rec_item_cat_glob
    }
    pickle.dump(ob, open("../feature/algo_output_10_4_half.p", "wb"))


create()
create_recommendation_vanilla()
create_recommendation_only_profit()
create_recommendation_cat_threshold()
create_recommendation_global_threshold()
save_file()