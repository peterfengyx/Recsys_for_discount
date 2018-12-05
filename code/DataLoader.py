# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 11:50:08 2018

@author: peternapolean
"""

import scipy.sparse as sp
from scipy.sparse.linalg import svds
import numpy as np
import pandas as pd
import os
import gzip
import pickle
from scipy.sparse import csr_matrix as sparse_matrix

def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

class DataLoader(object):
    def __init__(self,category,save_path):
        self.category=category
        self.price_dict={}
        self.cate_dict={}
        self.top_value=15
        if not os.path.isfile(save_path):
            self.load_data()
            self.create_user_item_matrix()
            self.create_ratings(self.top_value)
            self.save_data(save_path)
        else:
            self.load(save_path)
        
    
    def load_ratings(self, filename):
        with open(os.path.join("..", "data", filename), "rb") as f:
            ratings = pd.read_csv(f,names=("user","item","rating","timestamp"))
        return ratings
    
    def load_prices(self,filename):
        price_dict = {}
        num_no_price=0
        for review in parse(os.path.join("..", "data", filename)):
            try:
                price=review['price']
                asin=review['asin']
                price_dict[asin]=price
            except:
                num_no_price+=1
                continue
        print("filename:",filename)
        print("length of price dict:", len(price_dict))
        print("# of items without price", num_no_price)
        return price_dict
    
    def load_data(self):
        print("Loading data:")
        for i in self.category:
            ratings_name= "ratings_"+i+".csv"
            price_name="meta_"+i+".json.gz"
            ratings_temp=self.load_ratings(ratings_name)
            print(len(ratings_temp))
            price_temp=self.load_prices(price_name)
            ratings_temp=ratings_temp[ratings_temp['item'].isin(price_temp.keys())]
            print(len(ratings_temp))
            self.price_dict.update(price_temp)
            cate_temp=dict(zip(price_temp.keys(),i))
            self.cate_dict.update(cate_temp)
            try:
                self.ratings=pd.merge(self.ratings,ratings_temp, how='outer')
            except:
                self.ratings=ratings_temp
        
        
    def create_user_item_matrix(self, user_key="user",item_key="item"):
        n = len(set(self.ratings[user_key]))
        d = len(set(self.ratings[item_key]))
        self.user_mapper = dict(zip(np.unique(self.ratings[user_key]), list(range(n))))
        self.item_mapper = dict(zip(np.unique(self.ratings[item_key]), list(range(d))))

        self.user_inverse_mapper = dict(zip(list(range(n)), np.unique(self.ratings[user_key])))
        self.item_inverse_mapper = dict(zip(list(range(d)), np.unique(self.ratings[item_key])))

        user_ind = [self.user_mapper[i] for i in self.ratings[user_key]]
        item_ind = [self.item_mapper[i] for i in self.ratings[item_key]]

        self.ratings_matrix = sparse_matrix((self.ratings["rating"], (user_ind, item_ind)), shape=(n,d))
        print("user-item matrix generated.")
        
    def create_ratings(self,top_value):
        C=MBRecsys(self.ratings_matrix,top_value)
        self.ratings_predict=C.predict()
        print("predicted ratings generated.")
        
    def save_data(self,save_path):
        self.dict_all={'prices':self.price_dict,'raw_ratings':self.ratings_matrix,
                           'new_ratings':self.ratings_predict,'cate':self.cate_dict,
                           'user_mapper':self.user_mapper, 'item_mapper':self.item_mapper, 
                           'user_inverse_mapper':self.user_inverse_mapper, 'item_inverse_mapper':self.item_inverse_mapper}
        with open(save_path,'wb') as f:
            pickle.dump(self.dict_all, f)
        print("data saved in ", save_path)
            
    def load(self,save_path):
        with open(save_path,'rb') as f:
            self.dict_all=pickle.load(f)
        self.ratings_matrix =self.dict_all['raw_ratings']
        self.ratings_predict=self.dict_all['new_ratings']
        self.price_dict=self.dict_all['prices']
        self.cate_dict=self.dict_all['cate']
        self.user_mapper=self.dict_all['user_mapper']
        self.item_mapper=self.dict_all['item_mapper']
        self.user_inverse_mapper=self.dict_all['user_inverse_mapper']
        self.item_inverse_mapper=self.dict_all['item_inverse_mapper']
        del self.dict_all
        print("Saved data loaded.")

class MBRecsys(object):
    def __init__(self,train_R,top_value):
        self.train_R=train_R
        self.top_value=top_value
        
    def predict(self):
        U, s, VT = svds(self.train_R, k = self.top_value)  #select top 15 sigular value
        S=np.diag(s)
        self.out_R= np.dot(np.dot(U, S), VT)
        return self.out_R
    