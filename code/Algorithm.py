import numpy as np
import math

from code.DataLoader import create_output

loader_obj = None
quantity = {}
inv_cost = {}
profit_predict = []
ranking_profit = []

def sigmoid(x, derivative=False):
    sigm = 1. / (1. + np.exp(-x))
    if derivative:
        return sigm * (1. - sigm)
    return sigm


def calculate_discount(p_i, p_max, c_i):
    lambda_cons = 0.1
    adoption_prob = lambda_cons * (1.5 - sigmoid(4 * p_i / p_max))

    discount = (- p_i + c_i * math.log(adoption_prob)) / (p_i * math.log(adoption_prob))
    return discount


def calculate_profit():
    global loader_obj, quantity, inv_cost, profit_predict
    # p_i = 10  # product price
    # p_max = 50 # category max price
    # c_i = 100  # inventory quantity
    # d_i = 0.4  # discount
    lambda_cons = 0.1

    # for each user
    for i in range(len(loader_obj.ratings_predict)):
        profit = []
        for j in range(len(loader_obj.ratings_predict[i])):
            rating = loader_obj.ratings_predict[i]
            p_i = loader_obj.price_dict[i]
            c_i = inv_cost[i]
            for key in loader_obj.new_price_dict:
                obj = loader_obj.new_price_dict[key]
                if j in obj:
                    p_max = loader_obj.max_price[key]
                    break
            d_i = calculate_discount(p_i, p_max, c_i)
            revenue = p_i * d_i - c_i
            rating = loader_obj.ratings_predict[i][j]
            rating_max = 5
            adoption_prob = math.pow(lambda_cons * (1.5 - sigmoid(4 * p_i / p_max)), d_i)
            norm_rating = rating / rating_max

            profit_ind = revenue * adoption_prob * norm_rating
            profit.append(profit_ind)
        profit_predict.append(profit)
    return


def calculate_ranking():
    global profit_predict, ranking_profit
    for i in range(len(profit_predict)):
        profit = list(profit_predict[i])
        ranking = np.zeros(len(profit))
        rank = 1
        while rank <= len(profit):
            index = profit.index(max(profit))
            ranking[index] = rank
            rank += 1
            profit[index] = -1
        ranking_profit.append(ranking)
    return


def create_obj():
    global loader_obj
    loader_obj = create_output()
    print(loader_obj.max_price)
    print(loader_obj.price_dict)

    # for key in x.new_price_dict:
    #     print(key)
    #     print(x.new_price_dict[key])
    #     print(len(x.new_price_dict[key]))
    # print("........")
    count = 0
    for key in loader_obj.ratings_predict:
        print(key)
        print(len(key))
        count += 1
        if count == 2:
            break
    count = 0
    for key in loader_obj.ranking:
        print(key)
        print(len(key))
        count += 1
        if count == 2:
            break

    return


def create_quantity():
    global loader_obj, quantity
    for i in range(len(loader_obj.price_dict)):
        quantity[i] = 200
    print("quantity initialized")
    return


def create_inventory_cost():
    global loader_obj, inv_cost
    for key in loader_obj.price_dict:
        inv_cost[key] = loader_obj.price_dict[key] / 2
    print("inventory cost initialized")
    return






create_obj()
# create_quantity()