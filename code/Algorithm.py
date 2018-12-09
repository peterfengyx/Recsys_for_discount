import numpy as np
import math

from code.DataLoader import create_output
import config


def sigmoid(x, derivative=False):
    sigm = 1. / (1. + np.exp(-x))
    if derivative:
        return sigm * (1. - sigm)
    return sigm


def calculate_discount():
    lambda_cons = 0.1
    p_i = 10  # product price
    p_max = 50 # category max price
    c_i = 100  # inventory quantity
    adoption_prob = lambda_cons * (1.5 - sigmoid(4 * p_i / p_max))

    discount = (- p_i + c_i * math.log(adoption_prob)) / (p_i * math.log(adoption_prob))
    return discount


def calculate_profit():
    p_i = 10  # product price
    p_max = 50 # category max price
    c_i = 100  # inventory quantity
    d_i = 0.4  # discount
    revenue = p_i * d_i - c_i
    lambda_cons = 0.1
    rating = 3
    rating_max = 5
    adoption_prob = math.pow(lambda_cons * (1.5 - sigmoid(4 * p_i / p_max)), d_i)
    norm_rating = rating / rating_max

    profit = revenue * adoption_prob * norm_rating
    return profit


def check():
    x = create_output()
    print(x.max_price)
    print(x.price_dict)
    print(x.cate_dict[1])


check()